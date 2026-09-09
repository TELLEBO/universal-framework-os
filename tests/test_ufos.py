"""Tests for the Universal Framework OS integrity verifier.

Stdlib only — the verifier must run anywhere the skill is installed,
without a package manager. Run: python3 -m unittest discover -s tests
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import ufos  # noqa: E402


def write(root: Path, rel: str, text: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def minimal_repo(root: Path, **overrides) -> ufos.Repo:
    """A synthetic, internally consistent framework repo."""
    skill = overrides.get(
        "skill",
        "---\n"
        "name: demo-framework\n"
        "description: >\n"
        "  " + " ".join(["word"] * 60) + "\n"
        "---\n"
        "\n"
        "## CORE OPERATING PRINCIPLES\n"
        "\n"
        "These 2 principles govern every interaction:\n"
        "\n"
        "### 1. First\n"
        "\n"
        "### 2. Second\n"
        "\n"
        "## REFERENCES\n"
        "\n"
        "- `references/alpha.md` - alpha\n"
        "Built from 5 repositories.\n",
    )
    alpha = overrides.get("alpha", "# Alpha\n\nbody\n")
    write(root, "SKILL.md", skill)
    write(root, "references/alpha.md", alpha)
    skill_lines = len(skill.splitlines())
    alpha_lines = len(alpha.splitlines())
    readme = overrides.get(
        "readme",
        "## 2 Core Operating Principles\n"
        "```\n"
        "demo/\n"
        f"|-- SKILL.md              <- {skill_lines} lines - core\n"
        f"    |-- alpha.md          <- {alpha_lines} lines - alpha\n"
        "```\n"
        f"**Total: {skill_lines + alpha_lines} lines across 2 files.**\n"
        f"2. **SKILL.md loads** (~{ufos.estimate_tokens(skill)} tokens): core\n"
        "Built from 5 repositories.\n",
    )
    write(root, "README.md", readme.replace("<-", "←"))
    return ufos.Repo(root)


def errors(findings):
    return [f for f in findings if f.severity == ufos.ERROR]


class TokenEstimateTests(unittest.TestCase):
    def test_estimate_is_chars_over_four(self):
        self.assertEqual(ufos.estimate_tokens("a" * 8), 2)
        self.assertEqual(ufos.estimate_tokens("a" * 4001), 1000)

    def test_empty_text_costs_nothing(self):
        self.assertEqual(ufos.estimate_tokens(""), 0)


class FrontmatterTests(unittest.TestCase):
    def test_parses_scalar_and_folded_block(self):
        fm = ufos.parse_frontmatter(
            "---\nname: thing\ndescription: >\n  one two\n  three\n---\nbody\n"
        )
        self.assertEqual(fm["name"], "thing")
        self.assertEqual(fm["description"], "one two three")

    def test_returns_none_without_frontmatter(self):
        self.assertIsNone(ufos.parse_frontmatter("# Just a doc\n"))


class FrontmatterCheckTests(unittest.TestCase):
    def test_clean_repo_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = minimal_repo(Path(tmp))
            self.assertEqual(errors(ufos.check_frontmatter(repo)), [])

    def test_missing_name_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = minimal_repo(
                Path(tmp),
                skill="---\ndescription: >\n  " + " ".join(["w"] * 60) + "\n---\n",
            )
            self.assertTrue(errors(ufos.check_frontmatter(repo)))

    def test_description_outside_word_band_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = minimal_repo(
                Path(tmp), skill="---\nname: demo\ndescription: too short\n---\n"
            )
            found = errors(ufos.check_frontmatter(repo))
            self.assertTrue(any("word" in f.message for f in found))


class ReferenceIntegrityTests(unittest.TestCase):
    def test_dangling_citation_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = minimal_repo(root)
            write(root, "SKILL.md", repo.read("SKILL.md") + "\n`references/ghost.md`\n")
            repo = ufos.Repo(root)
            found = errors(ufos.check_references(repo))
            self.assertTrue(any("ghost.md" in f.message for f in found))

    def test_uncited_reference_file_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            minimal_repo(root)
            write(root, "references/orphan.md", "# Orphan\n")
            found = errors(ufos.check_references(ufos.Repo(root)))
            self.assertTrue(any("orphan.md" in f.message for f in found))


class StatsAccuracyTests(unittest.TestCase):
    def test_stale_line_count_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = minimal_repo(root)
            import re
            stale = re.sub(r"← \d+ lines", "← 999 lines", repo.read("README.md"), count=1)
            write(root, "README.md", stale)
            found = errors(ufos.check_stats(ufos.Repo(root)))
            self.assertTrue(any("alpha.md" in f.message or "SKILL.md" in f.message for f in found))

    def test_accurate_stats_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = minimal_repo(Path(tmp))
            self.assertEqual(errors(ufos.check_stats(repo)), [])


class ClaimConsistencyTests(unittest.TestCase):
    def test_principle_count_must_match_headings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = minimal_repo(root)
            wrong = repo.read("SKILL.md").replace("These 2 principles", "These 7 principles")
            write(root, "SKILL.md", wrong)
            found = errors(ufos.check_claims(ufos.Repo(root)))
            self.assertTrue(any("principle" in f.message.lower() for f in found))

    def test_repo_count_must_agree_across_documents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = minimal_repo(root)
            write(root, "README.md", repo.read("README.md").replace("5 repositories", "30+ repositories"))
            found = errors(ufos.check_claims(ufos.Repo(root)))
            self.assertTrue(any("repositor" in f.message.lower() for f in found))

    def test_consistent_claims_pass(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = minimal_repo(Path(tmp))
            self.assertEqual(errors(ufos.check_claims(repo)), [])


class BudgetTests(unittest.TestCase):
    def test_oversized_skill_file_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = minimal_repo(root)
            bloat = repo.read("SKILL.md") + "\n".join("filler" for _ in range(ufos.MAX_SKILL_LINES))
            write(root, "SKILL.md", bloat)
            found = errors(ufos.check_budget(ufos.Repo(root)))
            self.assertTrue(any("line" in f.message for f in found))

    def test_understated_token_claim_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = minimal_repo(root)
            measured = ufos.estimate_tokens(repo.read("SKILL.md"))
            understated = repo.read("README.md").replace(
                f"(~{measured} tokens)", f"(~{int(measured * 0.4)} tokens)"
            )
            write(root, "README.md", understated)
            found = errors(ufos.check_budget(ufos.Repo(root)))
            self.assertTrue(any("claim" in f.message.lower() for f in found))

    def test_budget_report_separates_always_on_from_on_demand(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = ufos.budget_report(minimal_repo(Path(tmp)))
            self.assertGreater(report["always_on"]["est_tokens"], 0)
            self.assertIn("on_demand", report)
            self.assertEqual(
                report["total"]["est_tokens"],
                report["always_on"]["est_tokens"] + report["on_demand"]["est_tokens"],
            )


class SecretTests(unittest.TestCase):
    def test_hardcoded_key_is_an_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            minimal_repo(root)
            write(root, "references/alpha.md", 'api_key = "abcd1234abcd1234abcd"\n')
            found = errors(ufos.check_secrets(ufos.Repo(root)))
            self.assertTrue(found)

    def test_environment_lookup_is_not_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            minimal_repo(root)
            write(root, "references/alpha.md", 'API_KEY = os.environ["API_KEY"]\nkey: "your_api_key_here"\n')
            self.assertEqual(errors(ufos.check_secrets(ufos.Repo(root))), [])


class CliTests(unittest.TestCase):
    def run_cli(self, *args, cwd=REPO_ROOT):
        return subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "ufos.py"), *args],
            capture_output=True, text=True, cwd=str(cwd),
        )

    def test_info_emits_machine_readable_spec(self):
        proc = self.run_cli("info", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        spec = json.loads(proc.stdout)
        self.assertIn("checks", spec)
        self.assertIn("limits", spec)

    def test_budget_json_is_parseable(self):
        proc = self.run_cli("budget", "--json")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("always_on", json.loads(proc.stdout))

    def test_unknown_subcommand_fails_loudly(self):
        proc = self.run_cli("teleport")
        self.assertNotEqual(proc.returncode, 0)

    def test_check_exits_nonzero_on_a_broken_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = minimal_repo(root)
            write(root, "SKILL.md", repo.read("SKILL.md").replace("These 2", "These 9"))
            proc = self.run_cli("check", "--root", str(root))
            self.assertEqual(proc.returncode, 1)


class RealRepositoryTests(unittest.TestCase):
    """The invariant that guards this repository forever."""

    def test_this_repository_passes_every_check(self):
        findings = ufos.run_checks(ufos.Repo(REPO_ROOT))
        failures = errors(findings)
        self.assertEqual(
            failures, [], "\n" + "\n".join(f.render() for f in failures)
        )


if __name__ == "__main__":
    unittest.main()
