# Changelog

## [1.1.0] - 2026-09-09

### Added

**Self-verification** — `scripts/ufos.py`, a zero-dependency CLI that holds the
framework to its own rules: `check` (integrity), `budget` (context cost), `info`
(machine-readable spec). Every command supports `--json` and fails loudly, per the
CLI-Anything design rules the skill itself prescribes.

**Test suite** — `tests/test_ufos.py`, stdlib `unittest`, including an integration
test asserting this repository passes every check. CI runs both on every push.

### Fixed

Four defects present in 1.0.0, each found by the verifier on its first run:

- SKILL.md announced "These 7 principles" directly above eight of them.
- SKILL.md claimed 19 source repositories; README and CHANGELOG claimed 30+.
- CHANGELOG counted 7 reference files where 6 exist.
- README advertised the always-on load at ~5K tokens; measured ~7.5K — a 51%
  understatement of the context cost paid on every message.

None of the four can silently return.

## [1.0.0] - 2026-03-26

### Initial Release

**8 Core Operating Principles**: Think Before You Act, Context Engineering, Research-First, Structured Knowledge, Precision & Rigor, Graceful Degradation, Security by Default, Token Economy.

**6 Reference Files** (3,264 lines; 3,763 including SKILL.md):
- `dev-methodology.md` — GSD, Superpowers, ECC, Ruflo, GitHub CLI, Supabase, Vercel, CLI-Anything
- `scraping-patterns.md` — Scrapling, Crawl4AI, Firecrawl, Scrapy, Crawlee, Exa, lightnovel-crawler
- `intelligence-patterns.md` — Crucix, AutoResearch, MiroFish, GraphRAG, Nacos, ValueCell, A2A protocol
- `osint-research-patterns.md` — Maltego, theHarvester, SpiderFoot, Hunter.io, intelligence cycle
- `token-optimization.md` — Context Mode, jCodeMunch, self-improving agent, ccusage, Supermemory
- `ecosystem-directory.md` — 1,326+ skills, 500+ MCP servers, 200+ resources, quick lookup table

**Integrated**: 30+ repositories, 3 academic books, 12 community skill packages.
