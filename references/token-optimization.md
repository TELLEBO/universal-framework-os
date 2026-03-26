# Token Optimization — 2X Efficiency Patterns

## The Token Economy Mindset

Every token has an opportunity cost. The 200K context window is not a
bucket to fill — it's a budget to spend wisely. These patterns, extracted
from 7 specialized tools, compound together to deliver 2X+ token efficiency.

**The three pillars**:
1. **Don't generate what isn't needed** (output compression)
2. **Don't retrieve what isn't relevant** (precision retrieval)
3. **Don't repeat what was already learned** (self-improvement)

---

## Pillar 1: Output Compression (from Context Mode)

### The Problem

Every tool call dumps raw data into the context window:
- Playwright snapshot: 56 KB
- 20 GitHub issues: 59 KB
- One access log: 45 KB
- After 30 minutes: 40% of context is consumed by raw tool output

### The Context Mode Pattern

**Principle**: Process data in a sandbox, return only summaries to context.

```
Raw tool output (315 KB)
  → Sandbox processing (extract, summarize, index)
    → Clean summary (5.4 KB) enters context
      = 98% reduction
```

**How to apply this WITHOUT the tool** (in every Claude response):

1. **Summarize before quoting**: When referencing search results, documents,
   or code, extract the key insight rather than reproducing the raw content.

2. **Answer, then evidence**: Lead with the answer/conclusion, follow with
   supporting evidence. Don't make the reader wade through data to find the point.

3. **Structured extraction over raw dumps**: When presenting data, transform
   it into a structured format (table, key-value pairs, bullet summary) rather
   than dumping raw text.

4. **Window extraction**: When only part of a document is relevant, extract
   the relevant window (the paragraphs where key terms appear) rather than
   returning the whole thing.

### Context Mode Search Architecture

Three-layer search for indexed content (applicable to any retrieval system):
- **Layer 1 — Porter stemming**: "caching" matches "cached", "caches"
- **Layer 2 — Trigram substring**: "useEff" finds "useEffect"
- **Layer 3 — Fuzzy correction**: "kuberntes" → "kubernetes"
- **RRF (Reciprocal Rank Fusion)**: Merges results from all layers into
  a single ranked list. Documents ranking well in multiple layers surface higher.

### Installation (for Claude Code users)

```bash
# Plugin install (recommended)
/plugin marketplace add mksglu/claude-context-mode
/plugin install context-mode@claude-context-mode

# Diagnostics
/context-mode:stats     # Per-tool savings breakdown
/context-mode:doctor    # Validate setup
```

---

## Pillar 2: Precision Retrieval (from jCodeMunch)

### The Problem

Agents read entire files to find one function. A 700-line file costs ~6,000
tokens. The function body is 30 lines (~400 tokens). That's 93% waste.

### The jCodeMunch Pattern

**Principle**: Index once. Retrieve by symbol. Never read whole files.

```
Index repository (tree-sitter AST parsing)
  → Extract symbols: functions, classes, methods, constants
  → Store: signature + summary + byte offset
  → Retrieve on demand: exact symbol source via byte offset
    = 95%+ token savings on code retrieval
```

**How to apply this WITHOUT the tool**:

1. **Cite specific functions, not files**: When referencing code, name the
   function/class/method. Don't paste entire files.

2. **Outline before depth**: Describe the structure first (what files exist,
   what functions they contain), then dive into specific implementations only
   when needed.

3. **Scope edits narrowly**: When suggesting code changes, show only the
   function being modified with minimal surrounding context. Don't reproduce
   the entire file.

4. **Use grep patterns, not file reads**: When searching for something in a
   codebase, suggest targeted grep/ripgrep commands rather than reading
   multiple full files.

### jCodeMunch Tool Surface

| Tool | What It Does | Token Impact |
|------|-------------|--------------|
| `search_symbols` | Find symbols by name across repo | Replaces multi-file grep |
| `get_symbol` | Retrieve exact function/class source | 400 tokens vs 6,000 |
| `get_repo_outline` | Repository structure overview | Orientation without reading files |
| `get_file_outline` | File structure (all symbols) | See what's in a file without reading it |
| `find_importers` | Who imports this symbol? | Structural query impossible without tooling |

### Installation (for Claude Code users)

```bash
# Add as MCP server
claude mcp add jcodemunch uvx jcodemunch-mcp

# CRITICAL: Add CLAUDE.md instructions (without this, agent won't use it)
# In your project's CLAUDE.md:
# "Use jcodemunch-mcp for all code lookups. Never read full files when MCP is available."
```

---

## Pillar 3: Self-Improvement (from Self-Improving Agent Skills)

### The Problem

AI agents have no persistent memory. Every session starts fresh. Users
repeat the same corrections. The agent rediscovers the same dead ends.

### The Self-Improving Pattern

**Principle**: Log corrections → promote to persistent knowledge → never repeat the same mistake.

```
Error/correction occurs in session
  → Log to .learnings/LEARNINGS.md (structured: problem, solution, area, priority)
  → Link related entries with "See Also"
  → Promote high-value learnings to CLAUDE.md (persists across sessions)
  → Agent reads CLAUDE.md at session start → avoids known mistakes
```

**Structured learning entry format**:
```markdown
## [Area Tag] Brief title
- **Problem**: What went wrong
- **Solution**: What fixed it
- **Root Cause**: Why it happened
- **Priority**: high/medium/low
- **See Also**: Links to related learnings
```

**How to apply this in conversations** (without the tool):

1. **Track corrections within the conversation**: When the user corrects you,
   explicitly acknowledge the correction and adjust behavior for the rest
   of the session.

2. **Summarize learned preferences**: Periodically note what you've learned
   about the user's preferences (formatting, level of detail, code style).

3. **Don't repeat failed approaches**: If an approach didn't work earlier
   in the conversation, remember that and try a different angle.

4. **Front-load corrections**: If you notice you're about to do something
   the user previously corrected, catch yourself before making the mistake.

### The MoltGuard Pattern (Boundary Enforcement)

From clawhub/thomaslwang/moltguard — enforce boundaries on what the
self-improving system can and cannot do:
- Never store secrets or credentials in learning files
- Require explicit consent before modifying workspace files
- Provide export/wipe controls for all persisted state
- Audit trail for all learning promotions

### Hook System (for Claude Code users)

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "command": ".learnings/hooks/activator.sh" }
    ],
    "PostToolUse": [
      { "matcher": "Bash",
        "command": ".learnings/hooks/error-detector.sh" }
    ]
  }
}
```

Token overhead: ~50-100 tokens per prompt for the activator hook. Negligible
compared to the savings from not repeating mistakes.

---

## Usage Tracking & Cost Awareness

### ccusage — Token Usage Analysis

Track exactly where your tokens are going:

```bash
npx ccusage@latest              # Daily report (default)
npx ccusage@latest daily        # Daily token usage and costs
npx ccusage@latest monthly      # Monthly aggregated report
npx ccusage@latest session      # Usage by conversation session
npx ccusage@latest blocks       # 5-hour billing windows
npx ccusage@latest blocks --live # Real-time monitoring
npx ccusage@latest -j           # JSON export for automation
```

**Key metrics to watch**:
- Cache creation vs cache read ratio (high cache reads = efficient reuse)
- Input vs output token split (high output = verbose responses)
- Per-session cost trends (identify expensive patterns)
- Model breakdown (Opus vs Sonnet vs Haiku — right model for right task?)

### Claude Code Usage Monitor — Real-Time Predictions

```bash
pip install claude-code-usage-monitor
python -m claude_code_usage_monitor
```

**Features**: Real-time burn rate tracking, session limit predictions,
multi-level warning system, plan-aware limits (Pro 44K, Max5 88K, Max20 220K).

**Burn rate intelligence**:
- Tracks tokens consumed per minute across sessions
- Predicts when current session will hit limits
- Alerts at configurable thresholds (50%, 75%, 90%)

---

## Token Optimization Techniques for Every Interaction

### Technique 1: Progressive Disclosure

Structure every response in layers:

```
Layer 0 — TL;DR (1-2 sentences, ~50 tokens)
Layer 1 — Key details (1-2 paragraphs, ~200 tokens)
Layer 2 — Full depth (full explanation, code, examples — only if needed)
```

Don't generate Layer 2 unless the question demands it. Most questions
are fully answered at Layer 1.

### Technique 2: Structured Over Verbose

Instead of:
```
The function takes a user ID as a parameter and queries the database
to find the user record. It then checks if the user has admin privileges
by comparing the role field against the ADMIN constant. If they do, it
returns true, otherwise false. The function also handles the case where
the user is not found by returning false.
```

Write:
```
isAdmin(userId): Queries DB for user → checks role === ADMIN → returns boolean.
Returns false if user not found.
```

Same information, ~75% fewer tokens.

### Technique 3: Code Precision

Instead of reproducing a 50-line function to change one line, show:
```
In `auth.py`, function `validate_token()`, line 23:
- Change: `token.expires > datetime.now()` → `token.expires > datetime.utcnow()`
```

~30 tokens vs ~500 tokens for the full function.

### Technique 4: Reference Don't Repeat

If you've already explained something in the conversation, reference it
rather than re-explaining:
- "As discussed above, use the same auth pattern for this endpoint."
- NOT: [entire re-explanation of the auth pattern]

### Technique 5: Smart Defaults

When the user's intent is clear, don't list every option. Pick the best
default and explain why. Offer alternatives only if the choice is
genuinely ambiguous.

### Technique 6: Batch Responses

When multiple related questions need answering, batch them into one
structured response rather than handling each one separately. This avoids
repeated context-setting overhead.

---

## Compound Effect: 2X Token Efficiency

Applied together, these techniques compound:

| Technique | Savings | Where It Applies |
|-----------|---------|-----------------|
| Output compression | 90-98% | Tool outputs, data dumps |
| Precision retrieval | 93-95% | Code reading, file access |
| Progressive disclosure | 50-75% | Every response |
| Structured over verbose | 60-75% | Explanations, descriptions |
| Code precision | 80-90% | Code edits, suggestions |
| Reference don't repeat | 50-100% | Long conversations |
| Self-improvement | Cumulative | Avoiding repeated mistakes |

**Net effect**: 2X or more token efficiency when these patterns become
habitual across all interactions.

---

## Integration with Framework Patterns

- **GSD context engineering** + token economy = split work into tasks
  to prevent context rot, AND make each task's context usage efficient
- **Ruflo 3-tier model routing** + token economy = use cheap models for
  simple retrieval tasks, expensive models only for complex reasoning
- **AutoResearch experiment loop** + token economy = each experiment runs
  in fresh context with minimal overhead
- **GraphRAG retrieval strategies** + precision retrieval = pull specific
  subgraph paths, not entire knowledge base dumps

---

## Planning-with-Files — File-Based Working Memory

From the planning-with-files skill (v2.26.1). Manus-style pattern where
persistent markdown files serve as "working memory on disk."

### The Three Files

| File | Purpose | When Updated |
|------|---------|-------------|
| `task_plan.md` | Phases, tasks, status tracking | Created at plan start, updated per phase |
| `findings.md` | Research context, discovered info | During collection/analysis |
| `progress.md` | Completed work log | After each task/phase completion |

### Session Recovery

These files survive `/clear` and session restarts. On session start:
1. Check if `task_plan.md` exists
2. Read all three files to restore context
3. Run `session-catchup.py` for unsynced context
4. Run `git diff --stat` to see code changes since last session
5. Update planning files, then proceed

### Hook Integration

```json
{
  "hooks": {
    "UserPromptSubmit": [{ "command": "head -50 task_plan.md; tail -20 progress.md" }],
    "PostToolUse": [{ "matcher": "Write|Edit", "command": "echo 'Update progress.md'" }],
    "Stop": [{ "command": "scripts/check-complete.sh" }]
  }
}
```

### Token Impact

Instead of re-explaining context after `/clear`, the agent reads 3 small
files (~500 tokens total) and has full context. Without this, restoring
context manually costs 2,000-5,000 tokens of back-and-forth.

---

## Web Search Plus — 7-Provider Intelligent Auto-Routing

From web-search-plus (v2.9.0). Instead of choosing a search provider,
the skill analyzes your query and routes to the best one automatically.

### Provider Selection Matrix

| Provider | Free Tier | Best For |
|----------|-----------|----------|
| **Serper** | 2,500/mo | Shopping, prices, local, news, Google results |
| **Tavily** | 1,000/mo | Research, explanations, academic content |
| **Querit** | Varies | Multilingual AI search, international |
| **Exa** | 1,000/mo | Neural search, "similar to X", startups, papers |
| **Perplexity** | Via Kilo | Direct answers with citations |
| **You.com** | Limited | Real-time info, AI/RAG context |
| **SearXNG** | **FREE** | Privacy-first, multi-source, self-hosted |

### Auto-Routing Signals

The router analyzes query features to select the best provider:
- Shopping terms (price, buy, cost) → Serper
- Research terms (how, why, explain, study) → Tavily
- Similarity queries ("like X", "similar to") → Exa
- Direct answer needed → Perplexity
- Privacy-sensitive → SearXNG
- Non-English query → Querit
- Real-time/breaking → You.com

### Token Impact

Smart routing returns higher-quality results on the first try, reducing
the need for follow-up searches. One good search result vs three mediocre
ones saves ~2,000 tokens per research cycle.

---

## Supermemory — State-of-the-Art AI Memory Engine

From supermemoryai/supermemory. #1 on all three major memory benchmarks.

### Memory vs RAG (Critical Distinction)

```
RAG:     Document chunks → vector search → stateless retrieval
         Same results for every user. No temporal understanding.

Memory:  Fact extraction → temporal tracking → contradiction resolution
         "I moved to SF" supersedes "I live in NYC"
         Auto-forgets expired information
         Builds user profiles from behavior over time

Supermemory: Runs BOTH together in every query.
```

### Architecture

```
Your AI app
  ↓
Supermemory
  ├── Memory Engine: Extract facts, track updates, resolve contradictions
  ├── User Profiles: Static facts + dynamic context (~50ms)
  ├── Hybrid Search: RAG + Memory in one query
  ├── Connectors: Google Drive, Gmail, Notion, GitHub (real-time sync)
  └── File Processing: PDFs, images, videos, code → searchable chunks
```

### API Pattern

```python
import requests

SM_KEY = os.environ["SUPERMEMORY_API_KEY"]

# Add a memory
requests.post("https://api.supermemory.ai/v3/add",
    headers={"Authorization": f"Bearer {SM_KEY}"},
    json={"content": "User prefers dark mode", "containerTags": ["project_x"]})

# Search (returns memories + user profile)
results = requests.post("https://api.supermemory.ai/v3/search",
    headers={"Authorization": f"Bearer {SM_KEY}"},
    json={"q": "user preferences", "containerTags": ["project_x"]})
```

### MCP Installation

```bash
# One-line install for any MCP client
npx -y install-mcp@latest https://mcp.supermemory.ai/mcp --client claude --oauth=yes
# Replace claude with: cursor, windsurf, vscode, etc.
```

### Token Impact

Instead of re-explaining your preferences every session, Supermemory
injects your profile automatically (~200 tokens). Without persistent
memory, context-setting costs 500-2,000 tokens per session start.
Over 10 sessions, that's 5,000-20,000 tokens saved.

---

## Data Analysis Methodology

From the data-analysis skill (v1.0.2). Decision-driven analysis framework.

### Core Principle

**Analysis without a decision is just arithmetic.**

Before touching data, answer:
1. What **decision** is this analysis supporting?
2. What would **change your mind**? (the real question)
3. What data do you **actually have** vs what you wish you had?
4. What **timeframe** is relevant?

### Statistical Rigor Checklist

- [ ] Sample size sufficient? (small N = wide confidence intervals)
- [ ] Comparison groups fair? (same time period, similar conditions)
- [ ] Multiple comparisons? (20 tests = 1 "significant" by chance)
- [ ] Effect size meaningful? (statistically significant ≠ practically important)
- [ ] Uncertainty quantified? ("12-18% lift" not just "15% lift")

### Reference Files (from the skill)

| Topic | Use When |
|-------|----------|
| Metric contracts | Defining KPIs — what counts, what doesn't, known caveats |
| Chart selection | Choosing the right visualization — includes anti-patterns |
| Decision briefs | Stakeholder-facing output format — answer + evidence + recommendation |
| Pitfalls | Common analytical failure modes to catch early |

---

## PDF Processing Patterns

From 3 complementary PDF skills (nano-pdf, pdf-extract, pdf-text-extractor):

| Need | Tool | Pattern |
|------|------|---------|
| Edit PDF with natural language | nano-pdf | `nano-pdf edit file.pdf 1 "Change title to X"` |
| Extract text (CLI) | pdf-extract | `pdftotext` via poppler-utils |
| Extract with OCR | pdf-text-extractor | Tesseract.js, multi-language, batch processing |
| Parse programmatically | PyMuPDF (fitz) | Image extraction, metadata, page rendering |

**Token-efficient PDF pattern**: Extract text first (cheap, ~200-400 tokens/page). Only rasterize pages with charts/figures that need visual understanding (~1,600 tokens/page).

---

## Scrapling MCP Integration Pattern

From scrapling-web-scraping skill (v1.2.0). Strategy + MCP execution split:

**Guidance layer** (this skill): Which fetcher to use, anti-bot escalation, spider recipes

**Execution layer** (MCP server): `mcporter call scrapling fetch_page --url URL`

### Anti-Bot Escalation Ladder

```
Level 0: Fetcher (HTTP)          → Static pages, fastest
Level 1: DynamicFetcher          → JS-rendered SPAs
Level 2: StealthyFetcher         → Cloudflare, Turnstile
Level 3: StealthyFetcher + proxy → Enterprise anti-bot
```

Always start at Level 0 and escalate only when blocked.
