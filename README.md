# Universal Framework OS

> The always-on operating system for Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, and beyond.

**One skill to rule them all.** Universal Framework OS fires on every single message — coding, writing, research, math, scraping, planning, debugging, analysis, or conversation — and applies battle-tested frameworks from 30+ repositories, 3 reference books, and 12 community skill packages to every response.

---

## What It Does

Instead of loading dozens of individual skills, Universal Framework OS gives your AI agent a single foundational layer that covers:

| Domain | Frameworks Integrated |
|--------|----------------------|
| **Development** | GSD (spec-driven), Superpowers (agentic skills), ECC (agent harness), Ruflo (multi-agent swarms) |
| **Web Scraping** | Scrapling, Crawl4AI, Firecrawl, Scrapy, Crawlee, Exa, lightnovel-crawler |
| **Intelligence** | Crucix (27-source OSINT), AutoResearch (Karpathy), MiroFish (swarm prediction) |
| **Knowledge** | GraphRAG (Manning 2025), knowledge graph construction, 5 retrieval strategies |
| **Security** | HexStrike (150+ tools), MoltGuard (guardrails), OWASP patterns |
| **Token Optimization** | Context Mode (98% reduction), jCodeMunch (95% code savings), self-improving agent |
| **Memory** | Supermemory (#1 on all benchmarks), claude-mem, Planning-with-Files |
| **Deployment** | GitHub CLI, Supabase, Vercel, CLI-Anything, Docker |
| **Research** | Maltego, theHarvester, SpiderFoot, Hunter.io, intelligence cycle |
| **Agent Ecosystem** | 1,326+ skills catalog, 500+ MCP servers, Nacos A2A registry, ValueCell finance |
| **Math & Physics** | Schaum's Math Handbook, Physics Vol. 2 (Springer 2023), computational verification |

## 8 Core Operating Principles

Every response is shaped by these principles:

1. **Think Before You Act** — UNDERSTAND → PLAN → EXECUTE → VERIFY
2. **Context Engineering** — File-based working memory, anti-drift, Planning-with-Files
3. **Research-First** — Editable assets + scalar metrics + program documents
4. **Structured Knowledge** — Entity-relationship thinking, RAG pipeline patterns
5. **Precision & Rigor** — Show work, verify computationally, cite sources
6. **Graceful Degradation** — Never leave the user with nothing
7. **Security by Default** — Env vars, sanitize, OWASP, ethical boundaries
8. **Token Economy** — 2X efficiency via compression, precision retrieval, progressive disclosure

---

## Installation

### Claude Code (Recommended)

```bash
# Option 1: Clone as a skill
git clone https://github.com/TELLEBO/universal-framework-os.git ~/.claude/skills/universal-framework-os

# Option 2: Copy the .skill file
# Download universal-framework-os.skill from Releases
# Unzip into ~/.claude/skills/universal-framework-os/
```

### Cursor

```bash
git clone https://github.com/TELLEBO/universal-framework-os.git .cursor/skills/universal-framework-os
```

### Codex CLI

```bash
git clone https://github.com/TELLEBO/universal-framework-os.git ~/.codex/skills/universal-framework-os
```

### Gemini CLI / Antigravity

```bash
git clone https://github.com/TELLEBO/universal-framework-os.git ~/.gemini/skills/universal-framework-os
```

### OpenCode / OpenClaw

```bash
git clone https://github.com/TELLEBO/universal-framework-os.git ~/.openclaw/skills/universal-framework-os
```

### Manual Install (Any Agent)

Copy the `SKILL.md` file and the `references/` folder into your agent's skills directory.

---

## File Structure

```
universal-framework-os/
├── SKILL.md                           ← 499 lines — Core operating principles + domain summaries
├── references/
│   ├── dev-methodology.md             ← 570 lines — GSD, Superpowers, ECC, Ruflo, TDD, subagents
│   ├── scraping-patterns.md           ← 297 lines — Decision tree for 8 scraping frameworks
│   ├── intelligence-patterns.md       ← 863 lines — Crucix, AutoResearch, MiroFish, GraphRAG, Nacos, ValueCell
│   ├── osint-research-patterns.md     ← 656 lines — Maltego, theHarvester, SpiderFoot, intelligence cycle
│   ├── token-optimization.md          ← 554 lines — Context Mode, jCodeMunch, self-improving, Supermemory
│   └── ecosystem-directory.md         ← 324 lines — 1,326+ skills + 500+ MCPs + quick lookup table
├── scripts/
│   └── ufos.py                        # the integrity verifier — zero dependencies
└── tests/
    └── test_ufos.py                   # stdlib unittest suite
```

**Total: 3,763 lines of concentrated knowledge across 7 files.**

Only those 7 files are *payload* — text that can enter a model's context. `scripts/`
and `tests/` are tooling: they cost zero tokens at inference time and exist purely to
keep the payload honest.

---

## How It Works

Universal Framework OS uses **progressive disclosure** — the skill architecture that Claude Code uses natively:

1. **Metadata scan** (~100 tokens): Claude sees the skill name and description, decides if it's relevant
2. **SKILL.md loads** (~7.5K tokens): Core principles and domain summaries enter context
3. **References load on demand**: Only when a specific domain is needed (e.g., scraping, OSINT, token optimization)

This means the skill is always available but doesn't bloat your context window until you actually need deep knowledge in a specific domain.

---

## What's Integrated

### Repositories (30+)

**Core Development**: GSD (get-shit-done), Superpowers (obra), ECC (everything-claude-code), Ruflo (ruvnet), GitHub CLI, Supabase, Vercel, CLI-Anything

**Web Scraping**: Scrapling (D4Vinci), Crawl4AI, Firecrawl MCP, Scrapy, Crawlee (JS + Python), Exa MCP, lightnovel-crawler, OpenClaw Ultra

**Intelligence & Research**: Crucix (calesthio), AutoResearch (karpathy), MiroFish (666ghj), claude-mem, HexStrike AI, ValueCell (financial agents), Nacos (Alibaba A2A)

**Token Optimization**: Context Mode (mksglu), jCodeMunch MCP, self-improving-agent (pskoett + ivangdavila), MoltGuard, ccusage (ryoppippi), Claude Code Usage Monitor, Planning-with-Files, Web Search Plus, Supermemory

**Ecosystem**: Antigravity Awesome Skills (1,326+), awesome-mcp-servers (500+), awesome-claude-code (200+)

### Books

- **Essential GraphRAG** (Bratanič & Hane, Manning 2025)
- **Physics Vol. 2** (Wan Hassan et al., Springer 2023)
- **Schaum's Math Handbook** (Spiegel et al., McGraw-Hill 2018)

### Community Skill Packages (12)

self-improving, moltguard, data-analysis, planning-with-files, web-search-plus, scrapling-web-scraping, nano-pdf, pdf-extract, pdf-text-extractor, openclaw-token-memory-optimizer, seo-optimizer, pymupdf-pdf-parser

---

## Token Efficiency

This skill is designed to make your agent **2X more token-efficient**:

| Technique | Savings |
|-----------|---------|
| Output compression (Context Mode pattern) | 90-98% |
| Precision retrieval (jCodeMunch pattern) | 93-95% |
| Progressive disclosure | 50-75% |
| Structured over verbose | 60-75% |
| Code precision edits | 80-90% |
| Self-improvement (no repeated mistakes) | Cumulative |

---

## Self-Verification

A framework that preaches computational verification and test-driven development
should not ask you to take its own numbers on faith. It doesn't.

```bash
python3 scripts/ufos.py check     # verify integrity — exit 1 on any failure
python3 scripts/ufos.py budget    # measure the context cost of the payload
python3 scripts/ufos.py info      # print the machine-readable specification
```

Every command accepts `--json`, so an agent can consume the output directly. There
are no dependencies to install — the skill ships as a git clone into five different
agent runtimes, so verifying it must never require a package manager.

`check` enforces six invariants, each one a principle from SKILL.md turned back on
the framework itself:

| Check | Invariant | Principle |
|-------|-----------|-----------|
| `frontmatter` | Valid skill contract; description within the 50–150 word rule | Skill authoring |
| `references` | Every cited reference exists; every reference on disk is reachable | Graceful degradation |
| `stats` | Every line count printed in this README matches the file on disk | Precision & rigor |
| `claims` | Countable claims are true; cross-document claims agree | Research-first |
| `budget` | Always-on payload stays under 500 lines and 10,000 tokens | Token economy |
| `secrets` | No hardcoded credentials anywhere in the payload | Security by default |

Claims split into two kinds. **Verifiable** claims — the number of principles, the
number of reference files, every line count — are recomputed from the repository and
compared to what the prose asserts. **Consistency** claims — how many repositories
were synthesized, how many books — have no ground truth in the tree, so the verifier
instead proves that SKILL.md, README.md and CHANGELOG.md never contradict each other.

Token figures are estimates (`characters / 4`); line and character counts are exact,
and the tool labels which is which rather than implying a precision it doesn't have.

Run on this repository, the first version of `check` found four defects that had
shipped in v1.0.0: SKILL.md announced "7 principles" above eight of them, claimed
19 source repositories where README and CHANGELOG claimed 30+, CHANGELOG counted 7
reference files where 6 exist, and this README advertised the always-on cost at ~5K
tokens when the measured figure was ~7.5K — a 51% understatement of the tax the skill
levies on every single message. All four are fixed, and none can silently return.

---

## Contributing

Contributions welcome! To add a new framework or pattern:

1. Fork the repo
2. Add content to the appropriate `references/*.md` file (or create a new one)
3. Update `SKILL.md` with a summary pointing to your reference
4. Ensure SKILL.md body stays under 500 lines
5. Run `python3 scripts/ufos.py check` and `python3 -m unittest discover -s tests` — CI runs both on every push
6. Submit a PR

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Credits

Built by synthesizing frameworks from 30+ open-source repositories, 3 academic references, and 12 community skill packages. Full attribution in SKILL.md and reference files.

Special thanks to the creators of: GSD, Superpowers, ECC, Ruflo, Scrapling, Crucix, AutoResearch, Context Mode, jCodeMunch, Supermemory, Antigravity Awesome Skills, awesome-mcp-servers, awesome-claude-code, and all other integrated projects.
