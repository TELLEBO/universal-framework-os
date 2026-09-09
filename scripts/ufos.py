#!/usr/bin/env python3
"""ufos - the Universal Framework OS integrity verifier.

This framework tells every agent to verify computationally, ground claims in
evidence, and test skills before shipping them. This script is how the
framework obeys its own rules: it checks that every number the documents
assert is true, that every cross-reference resolves, and that the always-on
context payload stays inside its declared budget.

Stdlib only, by design. The skill installs into Claude Code, Cursor, Codex,
Gemini and Antigravity as a plain git clone; verifying it must never require
a package manager.

    python3 scripts/ufos.py check      # verify integrity, exit 1 on failure
    python3 scripts/ufos.py budget     # measure the context cost
    python3 scripts/ufos.py info       # emit the machine-readable spec
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# --- The specification -------------------------------------------------
# These constants are the executable form of the rules the README states in
# prose. Change them here and the documents must follow, or `check` fails.

ALWAYS_ON_FILES = ("SKILL.md",)   # loaded into every conversation
ON_DEMAND_DIRS = ("references",)  # loaded only when a domain is needed
MAX_SKILL_LINES = 500             # README contributing rule
MAX_ALWAYS_ON_TOKENS = 10_000     # ceiling on the per-message context tax
CHARS_PER_TOKEN = 4               # standard heuristic; estimates only
CLAIM_TOLERANCE = 0.25            # how far a stated token cost may drift
DESCRIPTION_WORDS = (50, 150)     # the skill-authoring rule, self-applied

ERROR = "error"
WARN = "warn"


@dataclass
class Finding:
    check: str
    severity: str
    message: str
    path: str | None = None

    def render(self) -> str:
        where = f" [{self.path}]" if self.path else ""
        label = "ERROR" if self.severity == ERROR else "warn "
        return f"  {label} {self.check}: {self.message}{where}"

    def as_dict(self) -> dict:
        return {
            "check": self.check,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


@dataclass
class Repo:
    root: Path
    _cache: dict = field(default_factory=dict, repr=False)

    def path(self, rel: str) -> Path:
        return self.root / rel

    def exists(self, rel: str) -> bool:
        return self.path(rel).is_file()

    def read(self, rel: str) -> str:
        if rel not in self._cache:
            p = self.path(rel)
            self._cache[rel] = p.read_text(encoding="utf-8") if p.is_file() else ""
        return self._cache[rel]

    def always_on_files(self) -> list[str]:
        return [f for f in ALWAYS_ON_FILES if self.exists(f)]

    def on_demand_files(self) -> list[str]:
        found: list[str] = []
        for d in ON_DEMAND_DIRS:
            base = self.root / d
            if base.is_dir():
                found += sorted(p.relative_to(self.root).as_posix()
                                for p in base.glob("*.md"))
        return found

    def payload_files(self) -> list[str]:
        return self.always_on_files() + self.on_demand_files()


def estimate_tokens(text: str) -> int:
    """Approximate token count. Exact character counts, estimated tokens."""
    return len(text) // CHARS_PER_TOKEN


def parse_frontmatter(text: str) -> dict | None:
    """Minimal YAML frontmatter reader: scalars and `key: >` folded blocks."""
    if not text.startswith("---"):
        return None
    lines = text.splitlines()
    try:
        end = next(i for i, ln in enumerate(lines[1:], 1) if ln.strip() == "---")
    except StopIteration:
        return None
    data: dict[str, str] = {}
    key: str | None = None
    folded: list[str] = []
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            if key is not None:
                data[key] = " ".join(folded).strip()
            key, value = m.group(1), m.group(2).strip()
            folded = [] if value in (">", "|", ">-", "|-") else [value]
        elif key is not None:
            folded.append(line.strip())
    if key is not None:
        data[key] = " ".join(folded).strip()
    return data


def _ints(pattern: str, text: str) -> list[int]:
    return [int(m.replace(",", "")) for m in re.findall(pattern, text)]


# --- Checks ------------------------------------------------------------

def check_frontmatter(repo: Repo) -> list[Finding]:
    """SKILL.md declares a valid, correctly sized skill contract."""
    out: list[Finding] = []
    if not repo.exists("SKILL.md"):
        return [Finding("frontmatter", ERROR, "SKILL.md is missing", "SKILL.md")]
    fm = parse_frontmatter(repo.read("SKILL.md"))
    if fm is None:
        return [Finding("frontmatter", ERROR, "no YAML frontmatter block", "SKILL.md")]
    if not fm.get("name"):
        out.append(Finding("frontmatter", ERROR, "frontmatter has no `name`", "SKILL.md"))
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm["name"]):
        out.append(Finding("frontmatter", ERROR,
                           f"`name` is not a kebab-case slug: {fm['name']}", "SKILL.md"))
    description = fm.get("description", "")
    if not description:
        out.append(Finding("frontmatter", ERROR, "frontmatter has no `description`", "SKILL.md"))
    else:
        words = len(description.split())
        low, high = DESCRIPTION_WORDS
        if not low <= words <= high:
            out.append(Finding("frontmatter", ERROR,
                               f"description is {words} words, outside the "
                               f"{low}-{high} word rule", "SKILL.md"))
        if not re.search(r"(?i)\b(not for|do not use|never use|except when)\b", description):
            out.append(Finding("frontmatter", WARN,
                               "description states no negative cases; the "
                               "skill-authoring rule asks for them", "SKILL.md"))
    return out


def check_references(repo: Repo) -> list[Finding]:
    """Every cited reference exists, and every reference on disk is cited."""
    out: list[Finding] = []
    cited: set[str] = set()
    for rel in repo.always_on_files() + ["README.md"]:
        cited |= set(re.findall(r"references/[A-Za-z0-9._-]+\.md", repo.read(rel)))
    for target in sorted(cited):
        if not repo.exists(target):
            out.append(Finding("references", ERROR,
                               f"cited but missing on disk: {target}", "SKILL.md"))
    skill_cites = set(re.findall(r"references/[A-Za-z0-9._-]+\.md", repo.read("SKILL.md")))
    for rel in repo.on_demand_files():
        if rel not in skill_cites:
            out.append(Finding("references", ERROR,
                               f"orphaned: {rel} is never cited by SKILL.md, so it "
                               "can never be loaded", rel))
    return out


def check_stats(repo: Repo) -> list[Finding]:
    """Line counts printed in README match the files on disk."""
    if not repo.exists("README.md"):
        return [Finding("stats", WARN, "README.md not found; stats unverified")]
    readme = repo.read("README.md")
    actual = {Path(rel).name: len(repo.read(rel).splitlines())
              for rel in repo.payload_files()}
    out: list[Finding] = []
    claimed_any = False
    for name, claimed in re.findall(r"([A-Za-z0-9._-]+\.md)\s*←\s*([\d,]+)\s+lines", readme):
        claimed_any = True
        n = int(claimed.replace(",", ""))
        if name not in actual:
            out.append(Finding("stats", ERROR,
                               f"README lists {name}, which is not a payload file", "README.md"))
        elif actual[name] != n:
            out.append(Finding("stats", ERROR,
                               f"{name} claims {n} lines, actually {actual[name]}", "README.md"))
    if not claimed_any:
        out.append(Finding("stats", WARN, "no per-file line counts found in README", "README.md"))
    totals = _ints(r"Total:\s*\*{0,2}\s*([\d,]+)\s+lines", readme)
    if totals and totals[0] != sum(actual.values()):
        out.append(Finding("stats", ERROR,
                           f"total claims {totals[0]} lines, actually {sum(actual.values())}",
                           "README.md"))
    counts = _ints(r"across\s+([\d,]+)\s+files", readme)
    if counts and counts[0] != len(actual):
        out.append(Finding("stats", ERROR,
                           f"claims {counts[0]} payload files, actually {len(actual)}",
                           "README.md"))
    return out


def check_claims(repo: Repo) -> list[Finding]:
    """Numbers asserted in prose are true, and agree across documents."""
    out: list[Finding] = []
    skill, readme = repo.read("SKILL.md"), repo.read("README.md")
    changelog = repo.read("CHANGELOG.md")

    # Verifiable: the principle count is countable from the headings.
    section = re.search(r"^##\s+CORE OPERATING PRINCIPLES\s*$(.*?)(?=^##\s)",
                        skill, re.M | re.S)
    if section:
        actual = len(re.findall(r"^###\s+\d+\.\s", section.group(1), re.M))
        declared = {
            "SKILL.md": _ints(r"These\s+(\d+)\s+principles", skill),
            "README.md": _ints(r"^##\s+(\d+)\s+Core Operating Principles", readme),
        }
        for path, values in declared.items():
            for value in values:
                if value != actual:
                    out.append(Finding("claims", ERROR,
                                       f"declares {value} principles, {actual} are defined",
                                       path))

    # Verifiable: the reference-file count is countable from disk.
    actual_refs = len(repo.on_demand_files())
    for value in _ints(r"(\d+)\s+Reference Files", changelog):
        if value != actual_refs:
            out.append(Finding("claims", ERROR,
                               f"declares {value} reference files, {actual_refs} exist",
                               "CHANGELOG.md"))

    # Consistency-only: no ground truth, but the documents must not disagree.
    sources = {"SKILL.md": skill, "README.md": readme, "CHANGELOG.md": changelog}
    for label, pattern in (
        ("repositories", r"(\d+)\+?\s+(?:GitHub\s+|open-source\s+)?repos(?:itories)?\b"),
        ("books", r"(\d+)\s+(?:academic\s+|reference\s+)?books?\b"),
        ("community skill packages", r"(\d+)\s+community skill packages\b"),
    ):
        seen: dict[int, list[str]] = {}
        for path, text in sources.items():
            for value in _ints(pattern, text):
                seen.setdefault(value, []).append(path)
        if len(seen) > 1:
            detail = "; ".join(f"{v} in {', '.join(sorted(set(p)))}"
                               for v, p in sorted(seen.items()))
            out.append(Finding("claims", ERROR,
                               f"documents disagree on {label}: {detail}"))
    return out


def check_budget(repo: Repo) -> list[Finding]:
    """The always-on context tax stays inside its declared budget."""
    out: list[Finding] = []
    for rel in repo.always_on_files():
        lines = len(repo.read(rel).splitlines())
        if lines > MAX_SKILL_LINES:
            out.append(Finding("budget", ERROR,
                               f"{lines} lines exceeds the {MAX_SKILL_LINES} line limit", rel))
    measured = sum(estimate_tokens(repo.read(rel)) for rel in repo.always_on_files())
    if measured > MAX_ALWAYS_ON_TOKENS:
        out.append(Finding("budget", ERROR,
                           f"always-on payload is ~{measured} tokens, over the "
                           f"{MAX_ALWAYS_ON_TOKENS} budget"))
    readme = repo.read("README.md")
    m = re.search(r"SKILL\.md loads\*{0,2}\s*\(~\s*([\d.,]+)\s*([KkMm]?)\s*tokens\)", readme)
    if m and measured:
        scale = {"": 1, "k": 1_000, "m": 1_000_000}[m.group(2).lower()]
        claimed = int(float(m.group(1).replace(",", "")) * scale)
        if abs(claimed - measured) > CLAIM_TOLERANCE * measured:
            out.append(Finding("budget", ERROR,
                               f"README claims the always-on load costs ~{claimed} tokens; "
                               f"measured ~{measured}", "README.md"))
    elif readme and not m:
        out.append(Finding("budget", WARN,
                           "README states no always-on token cost", "README.md"))
    return out


SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(api[_-]?key|secret|token|password|passwd|access[_-]?key)\b\s*[:=]\s*"
    r"[\"']([^\"']{16,})[\"']")
SECRET_LITERAL = re.compile(
    r"\b(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|AKIA[0-9A-Z]{16}|xox[baprs]-[A-Za-z0-9-]{10,})\b")
PLACEHOLDER = re.compile(
    r"(?i)your[_-]|example|placeholder|redacted|xxx|\.\.\.|<[^>]+>|\$\{|"
    r"os\.environ|getenv|process\.env|insert|change_?me")


def check_secrets(repo: Repo) -> list[Finding]:
    """Principle 7, applied to the framework itself: no hardcoded secrets."""
    out: list[Finding] = []
    for rel in repo.payload_files():
        for number, line in enumerate(repo.read(rel).splitlines(), 1):
            if PLACEHOLDER.search(line):
                continue
            if SECRET_ASSIGNMENT.search(line) or SECRET_LITERAL.search(line):
                out.append(Finding("secrets", ERROR,
                                   f"line {number} looks like a hardcoded credential", rel))
    return out


CHECKS = {
    "frontmatter": check_frontmatter,
    "references": check_references,
    "stats": check_stats,
    "claims": check_claims,
    "budget": check_budget,
    "secrets": check_secrets,
}


def run_checks(repo: Repo, only: str | None = None) -> list[Finding]:
    selected = {only: CHECKS[only]} if only else CHECKS
    findings: list[Finding] = []
    for fn in selected.values():
        findings += fn(repo)
    return findings


def budget_report(repo: Repo) -> dict:
    def group(files: list[str]) -> dict:
        entries = []
        for rel in files:
            text = repo.read(rel)
            entries.append({
                "path": rel,
                "lines": len(text.splitlines()),
                "chars": len(text),
                "est_tokens": estimate_tokens(text),
            })
        return {
            "files": entries,
            "lines": sum(e["lines"] for e in entries),
            "chars": sum(e["chars"] for e in entries),
            "est_tokens": sum(e["est_tokens"] for e in entries),
        }

    always_on = group(repo.always_on_files())
    on_demand = group(repo.on_demand_files())
    return {
        "estimator": f"characters / {CHARS_PER_TOKEN} (estimate; lines and chars are exact)",
        "always_on": always_on,
        "on_demand": on_demand,
        "total": {
            "lines": always_on["lines"] + on_demand["lines"],
            "chars": always_on["chars"] + on_demand["chars"],
            "est_tokens": always_on["est_tokens"] + on_demand["est_tokens"],
        },
        "budget": {
            "max_always_on_tokens": MAX_ALWAYS_ON_TOKENS,
            "headroom_tokens": MAX_ALWAYS_ON_TOKENS - always_on["est_tokens"],
        },
    }


def spec(repo: Repo) -> dict:
    return {
        "tool": "ufos",
        "purpose": "verify that Universal Framework OS obeys its own rules",
        "checks": [{"name": name, "description": (fn.__doc__ or "").strip()}
                   for name, fn in CHECKS.items()],
        "limits": {
            "max_skill_lines": MAX_SKILL_LINES,
            "max_always_on_tokens": MAX_ALWAYS_ON_TOKENS,
            "chars_per_token": CHARS_PER_TOKEN,
            "claim_tolerance": CLAIM_TOLERANCE,
            "description_words": list(DESCRIPTION_WORDS),
        },
        "payload": {
            "always_on": repo.always_on_files(),
            "on_demand": repo.on_demand_files(),
        },
    }


def main(argv: list[str] | None = None) -> int:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=str(Path(__file__).resolve().parents[1]),
                        help="framework root (default: this repository)")
    common.add_argument("--json", action="store_true", dest="as_json",
                        help="emit machine-readable JSON")
    parser = argparse.ArgumentParser(
        prog="ufos", description="Universal Framework OS integrity verifier")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check", parents=[common],
                           help="verify integrity; exit 1 on any error")
    check.add_argument("--only", choices=sorted(CHECKS), help="run a single check")
    check.add_argument("--strict", action="store_true", help="treat warnings as errors")
    sub.add_parser("budget", parents=[common],
                   help="measure the context cost of the payload")
    sub.add_parser("info", parents=[common],
                   help="print the machine-readable specification")

    args = parser.parse_args(argv)
    repo = Repo(Path(args.root).resolve())
    if not repo.exists("SKILL.md"):
        print(f"ufos: no SKILL.md under {repo.root}", file=sys.stderr)
        return 2

    if args.command == "info":
        payload = spec(repo)
        print(json.dumps(payload, indent=2) if args.as_json else _render_spec(payload))
        return 0

    if args.command == "budget":
        report = budget_report(repo)
        print(json.dumps(report, indent=2) if args.as_json else _render_budget(report))
        return 0

    findings = run_checks(repo, only=args.only)
    if args.strict:
        findings = [Finding(f.check, ERROR, f.message, f.path) for f in findings]
    failed = [f for f in findings if f.severity == ERROR]
    if args.as_json:
        print(json.dumps({
            "root": str(repo.root),
            "ok": not failed,
            "errors": len(failed),
            "warnings": len(findings) - len(failed),
            "findings": [f.as_dict() for f in findings],
        }, indent=2))
    else:
        for name in (args.only and [args.only]) or list(CHECKS):
            hits = [f for f in findings if f.check == name]
            status = "FAIL" if any(f.severity == ERROR for f in hits) else "ok"
            print(f"{status:>4}  {name}")
            for finding in hits:
                print(finding.render())
        print(f"\n{len(failed)} error(s), {len(findings) - len(failed)} warning(s)")
    return 1 if failed else 0


def _render_spec(payload: dict) -> str:
    lines = [f"{payload['tool']} - {payload['purpose']}", "", "checks:"]
    lines += [f"  {c['name']:<12} {c['description']}" for c in payload["checks"]]
    lines += ["", "limits:"]
    lines += [f"  {k:<24} {v}" for k, v in payload["limits"].items()]
    return "\n".join(lines)


def _render_budget(report: dict) -> str:
    lines = [report["estimator"], ""]
    for group in ("always_on", "on_demand"):
        lines.append(f"{group}:")
        for entry in report[group]["files"]:
            lines.append(f"  {entry['path']:<38} {entry['lines']:>5} lines "
                         f"{entry['est_tokens']:>7} est. tokens")
        lines.append(f"  {'subtotal':<38} {report[group]['lines']:>5} lines "
                     f"{report[group]['est_tokens']:>7} est. tokens\n")
    budget = report["budget"]
    lines.append(f"always-on budget: {budget['max_always_on_tokens']} tokens, "
                 f"headroom {budget['headroom_tokens']}")
    return "\n".join(lines)


if __name__ == "__main__":
    sys.exit(main())
