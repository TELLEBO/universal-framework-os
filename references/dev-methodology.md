# Development Methodology — Full Reference

## GSD (Get Shit Done) — Spec-Driven Development

### Philosophy
The complexity is in the system, not in your workflow. Behind the scenes: context
engineering, XML prompt formatting, subagent orchestration, state management. What
you see: a few commands that just work.

### The GSD Lifecycle

```
NEW PROJECT → DISCUSS → PLAN → EXECUTE → VERIFY → SHIP
     ↓           ↓         ↓         ↓          ↓       ↓
  Configure   Lock in    Research   Parallel   Manual    PR with
  roadmap     decisions  + plan     subagents  UAT      meaningful
              per phase  + verify              script   description
```

**Discuss phase**: Code-aware — analyzes relevant source files BEFORE asking questions.
Locks in product decisions before planning. No ambiguity moves forward.

**Plan phase**: Asks user about research instead of silently deciding. Produces tasks
with: objective, files to touch, must-have verification criteria.

**Execute phase**: One task at a time in fresh context. Atomic git commits. Parallel
waves with `--no-verify` on subagent commits; hooks run once after each wave.

**Verify phase**: Run configured verification commands (lint, test, typecheck) with
auto-fix retries. Manual UAT script if applicable.

**Ship phase**: Create PR with meaningful description derived from task summaries.

### Context Rot Prevention
- Split work into small, checkable plans
- Run each plan in a fresh context window
- Atomic git commits per task (bisectable history)
- Externalize state into files (`.planning/` directory)
- Nyquist validation: test feedback loop BEFORE writing code

### Model Profiles
| Profile | Planning | Execution | Research |
|---------|----------|-----------|----------|
| budget | Mid-tier | Lightweight | Lightweight |
| balanced | Mid-tier | Mid-tier | Mid-tier |
| smart | Strong | Mid-tier | Mid-tier |
| genius | Strong | Mid-tier | Lightweight |
| inherit | Session model | Session model | Session model |

---

## Superpowers — Agentic Skills Methodology

### Core Workflow
1. Agent sees user is building something
2. Steps back, asks what user is really trying to do (brainstorming skill)
3. Teases out a spec, shows it in digestible chunks
4. User signs off on design
5. Agent creates implementation plan (clear enough for a junior engineer)
6. Subagent-driven development executes tasks
7. Two-stage review per task: spec compliance → code quality
8. Verification before completion

### Key Skills
| Skill | Purpose |
|-------|---------|
| brainstorming | Tease out requirements, write design doc |
| designing-before-coding | Spec-first approach |
| writing-plans | Create implementation plans from specs |
| test-driven-development | Red-Green-Refactor cycle |
| subagent-driven-development | Fast iteration with two-stage review |
| systematic-debugging | 4-phase root cause process |
| verification-before-completion | Ensure it's actually fixed |
| writing-skills | TDD for documentation/skills |

### Systematic Debugging (4-Phase)
1. **Reproduce**: Get a reliable reproduction of the bug
2. **Isolate**: Narrow down to the specific component/line
3. **Fix**: Apply the minimal change that resolves the issue
4. **Verify**: Confirm the fix works AND hasn't broken anything else

Includes sub-techniques: root-cause-tracing, defense-in-depth, condition-based-waiting.

### Plan Format
```markdown
# [Feature Name] Implementation Plan
> **For agentic workers:** Use subagent-driven-development to implement
> this plan task-by-task.

## File Map
[Which files created/modified, what each is responsible for]

## Tasks
- [ ] Task 1: [objective, files, verification criteria]
- [ ] Task 2: ...
```

---

## Everything Claude Code (ECC) — Agent Harness

### Directory Structure
```
project/
├── agents/           # Specialized subagents (planner, tdd-guide, code-reviewer...)
├── skills/           # Workflow definitions + domain knowledge
├── rules/            # Standards, conventions, checklists
│   ├── common/       # Required for all projects
│   └── [language]/   # Language-specific rules
├── commands/         # Custom slash commands
├── hooks/            # Pre/post execution hooks (hooks.json)
├── mcp-configs/      # MCP server configurations
└── CLAUDE.md         # Project-level config
```

### Rules vs Skills
- **Rules** tell you WHAT (standards, checklists): "80% test coverage", "no hardcoded secrets"
- **Skills** tell you HOW (actionable guides): "python-patterns", "golang-testing"
- Language-specific rules reference relevant skills
- When language-specific and common rules conflict, language-specific wins

### Agent Delegation
| Agent | Role |
|-------|------|
| planner | Feature implementation planning |
| architect | System design decisions |
| tdd-guide | Test-driven development |
| code-reviewer | Quality and security review |
| security-reviewer | OWASP Top 10 vulnerability analysis |
| e2e-runner | Playwright E2E testing |
| refactor-cleaner | Dead code cleanup |
| doc-updater | Documentation sync |
| build-error-resolver | Fix build/compile errors |

### Instinct System (Continuous Learning)
- Instincts are learned patterns from past sessions
- Confidence scoring determines when to apply
- `/evolve` clusters related instincts into skills
- `/promote` elevates project-level instincts to global

### Code Quality Standards (Non-Negotiable)
- No hardcoded secrets — environment variables only
- 80%+ test coverage enforced
- Immutability preferred (const, readonly, frozen objects)
- File size limits — single responsibility, small focused files
- Security-first — OWASP audit on every feature, no eval(), sanitize all input
- Type safety — full type hints (Python) or strict TypeScript, no unjustified `any`
- Atomic commits — one logical change per commit

### Skill Authoring
```yaml
---
name: skill-name
description: >
  Verb phrase. Use when [contexts]. Triggers for "phrase 1", "phrase 2",
  "phrase 3". Do NOT use for [negatives].
---
```
- 50-150 words in description
- 5+ trigger phrases
- Include negative cases
- SKILL.md body < 500 lines
- Heavy content → references/
- Test with TDD: baseline → write skill → verify improvement

---

## Session Memory Pattern (from claude-mem)

### Capture → Compress → Inject

1. **Capture**: Automatically record what Claude does during coding sessions
2. **Compress**: Use AI to extract key decisions, patterns, and context
3. **Inject**: Feed relevant compressed context back into future sessions

### Application in Conversations
- Maintain a running mental model of what's been decided
- When referencing earlier parts of conversation, summarize rather than repeat
- Prioritize recent and high-impact decisions for context
- If the conversation is long, proactively offer to summarize the state

---

## Cross-Cutting Patterns

### Git Workflow
- Atomic commits per task with meaningful messages
- Pre-commit hooks for secret detection
- Branch-per-feature with PR workflow
- `--no-verify` for parallel subagent commits; hooks run post-wave

### Testing Philosophy
- TDD is mandatory: Red → Green → Refactor
- 80%+ test coverage enforced
- Nyquist validation: test feedback loop before writing code
- E2E tests for critical user flows (Playwright)

### Documentation
- Specs: `docs/specs/YYYY-MM-DD-<topic>.md`
- Plans: `docs/plans/YYYY-MM-DD-<feature>.md`
- Design decisions in the spec, not in code comments
- Doc-updater agent keeps docs in sync

---

## Ruflo — Multi-Agent Swarm Orchestration Platform

### Overview
Ruflo (formerly Claude Flow) is an enterprise agent orchestration framework
with 5,900+ commits, 259 MCP tools, 60+ agents, and 8 AgentDB controllers.
It transforms Claude Code into a multi-agent development platform.

**Data flow**:
```
User → Ruflo (CLI/MCP) → Router → Swarm → Agents → Memory → LLM Providers
  ↑                                                              ↓
  └──────────────── Learning Loop ←─────────────────────────────┘
```

### Installation & Setup
```bash
# One-line install
curl -fsSL https://cdn.jsdelivr.net/gh/ruvnet/claude-flow@main/scripts/install.sh | bash
# Or via npx
npx ruflo@latest init --wizard
# Add MCP server to Claude Code
claude mcp add ruflo -- npx -y ruflo@latest mcp start
# System diagnostics
npx ruflo doctor --fix
```

### Swarm Topologies

Choose topology by task complexity:

| Topology | Best For | How It Works |
|----------|----------|-------------|
| **Hierarchical** | Coding tasks (anti-drift default) | Single coordinator enforces alignment |
| **Mesh** | Research, exploration | All agents communicate freely |
| **Ring** | Pipeline processing | Sequential handoff between agents |
| **Star** | Data aggregation | Central hub + spoke workers |

**Anti-drift defaults** (ALWAYS use for coding tasks):
```javascript
swarm_init({
  topology: "hierarchical",  // Single coordinator enforces alignment
  maxAgents: 8,              // Smaller team = less drift surface
  strategy: "specialized"    // Clear roles reduce ambiguity
})
```

### Swarm Orchestration Pattern
```javascript
// STEP 1: Initialize swarm via MCP
mcp__ruv-swarm__swarm_init({
  topology: "hierarchical", maxAgents: 8, strategy: "specialized"
})

// STEP 2: Spawn agents concurrently via Task tool
// ALL Task calls in SAME message for parallel execution
Task("Coordinator", "Initialize session, coordinate via memory.", "hierarchical-coordinator")
Task("Researcher", "Analyze requirements and code patterns.", "researcher")
Task("Architect", "Design implementation approach.", "system-architect")
Task("Coder", "Implement following architect's design.", "coder")
Task("Tester", "Write tests for implementation.", "tester")
```

### Agent Types (60+ across 8 categories)

Worker specializations: researcher, coder, analyst, tester, architect,
reviewer, optimizer, documenter, coordinator, monitor, specialist

```bash
npx ruflo agent spawn -t coder --name my-coder
npx ruflo agent spawn -t tester --name my-tester
npx ruflo agent spawn -t reviewer --name my-reviewer
```

### Hive Mind System
Queen-led hierarchical coordination:
```bash
npx ruflo hive-mind init --topology hierarchical-mesh --consensus byzantine
npx ruflo hive-mind spawn "Build API" --queen-type strategic --agents 8
npx ruflo hive-mind status    # Check status
npx ruflo hive-mind metrics   # Performance metrics
npx ruflo hive-mind memory    # Collective memory stats
```

### AgentDB v3 — Memory System

20+ memory controllers with 3-tier architecture:

**Memory tiers**: Working → Episodic → Semantic
- Ebbinghaus forgetting curves + spaced repetition for retention
- HNSW vector indexing: 150x faster semantic search, O(log n)
- ReasoningBank WASM: hash-based embeddings, no API keys needed
- 2-3ms query latency for semantic searches

**8 AgentDB v3 Controllers**:
1. HierarchicalMemory — tiered storage management
2. MemoryConsolidation — compress and merge memories
3. SemanticRouter — route queries to right memory tier
4. GNNService — graph neural network operations
5. RVFOptimizer — vector field optimization
6. MutationGuard — cryptographic proof-verified writes
7. AttestationLog — audit trail for memory operations
8. GuardedVectorBackend — secure vector storage

```bash
npx ruflo memory store-vector api_design "REST endpoints" \
  --namespace backend --metadata '{"version":"v2"}'
npx ruflo memory vector-search "user authentication flow" \
  --k 10 --threshold 0.7 --namespace backend
```

### Self-Learning Loop

```
RETRIEVE (HNSW, 150x faster)
  → JUDGE (verdicts: success/failure)
    → DISTILL (LoRA fine-tuning)
      → CONSOLIDATE (EWC++, prevents catastrophic forgetting)
```

Result: Agents improve over time. Successful patterns are reinforced.
Failed patterns are deprioritized.

### 3-Tier Model Routing

Intelligent routing saves up to 75% on API costs:
- **Strong model** (Opus) → planning, architecture decisions
- **Mid-tier model** (Sonnet) → execution, code generation
- **Lightweight model** (Haiku) → research, verification, simple tasks

### Spec-First Architecture (ADR + DDD)

Ruflo enforces spec-first development via:
- **ADRs** (Architecture Decision Records): Define architecture before coding
- **DDD bounded contexts**: Organize code into domain-driven modules
- **Compliance enforcement**: System validates agent output against specs

### MCP Tools (259 total, 7 categories)

| Category | Count | Examples |
|----------|-------|---------|
| Swarm Management | 16 | swarm_init, agent_spawn, task_orchestrate |
| Neural & AI | 15 | neural_train, neural_compress |
| Memory & Persistence | 10 | memory_store, memory_search, agentdb_info |
| Performance & Analytics | 10 | metrics, optimize, analyze_bottlenecks |
| GitHub Integration | 6 | PR creation, issue management |
| Dynamic Agent Architecture | 6 | Self-organizing agents, fault tolerance |
| Workflow & Automation | 8 | hooks, session management |
| System Utilities | 16 | doctor, config, daemon management |

### CLAUDE.md Rules (from Ruflo's CLAUDE.md)

When working in a Ruflo project, follow these rules:
- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary — prefer editing existing files
- NEVER proactively create docs/READMEs unless explicitly requested
- NEVER save working files to the root folder
- Never continuously poll status after spawning a swarm — wait for results
- ALWAYS use hierarchical topology for coding swarms
- Use Edit tool directly when AGENT_BOOSTER_AVAILABLE

### Hooks System

Ruflo hooks automate routing and learning:
```bash
npx ruflo hooks session-start       # Begin tracked session
npx ruflo hooks pre-command          # Pre-command validation
npx ruflo hooks post-edit            # Post-edit memory updates
```

The hooks system reads stdin JSON, enabling all learning/routing/intelligence
features. It automatically routes tasks to the right agents, learns from
successful patterns, and coordinates multi-agent work in the background.

---

## Developer Platform Stack

### GitHub CLI (gh) — Terminal-First GitHub Workflow

**Install**: `brew install gh` or `winget install GitHub.cli` or `apt install gh`

**Authentication**: `gh auth login` (OAuth flow, sets up git credential helper too)

**Core workflow**:
```bash
# Create repo and clone
gh repo create my-project --public --clone

# Branch workflow with linked issues
gh issue create --title "Add auth" --body "OAuth flow needed"
gh issue develop 42         # Creates linked branch from issue

# PR workflow
gh pr create --fill-first   # Auto-populate from first commit message
gh pr checks                # Watch CI status
gh pr merge --squash        # Merge when ready

# Actions monitoring
gh run list                 # All recent workflow runs
gh run watch                # Live-follow current run
gh run view --log-failed    # Debug failures instantly

# Scriptable API access
gh api graphql -f query='{ viewer { login } }'
gh api repos/{owner}/{repo}/issues --jq '.[].title'
```

**Automation patterns**:
```bash
# Custom aliases for repeated workflows
gh alias set review 'pr list --search "review-requested:@me"'
gh alias set deploy 'workflow run deploy.yml'

# JSON output for piping
gh pr list --json number,title,author | jq '.[] | select(.author.login=="me")'

# Bulk operations
gh issue list --state open --json number -q '.[].number' | \
  xargs -I {} gh issue close {} --comment "Closing stale issues"
```

### Supabase — Full Backend Platform

**Install**: `brew install supabase/tap/supabase`

**Local development** (mirrors production exactly):
```bash
supabase init                    # Create project structure
supabase start                   # Spin up full Docker stack
# → Postgres at localhost:54322
# → REST API at localhost:54321
# → Studio UI at localhost:54323
# → Auth, Storage, Realtime all running

supabase db diff --local         # Generate migration from schema changes
supabase migration new add_users # Create named migration
supabase db push                 # Apply migrations to remote
```

**Project structure**:
```
supabase/
├── config.toml        # Ports, auth settings, storage config
├── seed.sql           # Dev data loaded on every db reset
├── migrations/        # Schema version history (timestamped SQL)
└── functions/         # Edge Functions (TypeScript/Deno)
    ├── _shared/       # Shared utilities between functions
    └── my-function/
        └── index.ts   # Handler
```

**Edge Functions** (Deno TypeScript, globally distributed):
```typescript
import { serve } from 'https://deno.land/std/http/server.ts'
import { createClient } from 'npm:@supabase/supabase-js@2'

serve(async (req) => {
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_ANON_KEY')!,
    { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
  )

  const { data, error } = await supabase.from('posts').select('*')
  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

**Deploy**:
```bash
supabase functions deploy my-function
supabase functions serve    # Local dev with hot reload
```

**Key patterns**:
- **RLS** (Row Level Security) — security at the database layer, not the API
- **Auto-generated APIs** — every table gets REST + GraphQL endpoints automatically
- **pgvector** — store embeddings alongside your data for RAG
- **Realtime** — subscribe to `INSERT/UPDATE/DELETE` on any table via WebSocket
- **MCP integration** — Supabase has an MCP server for AI-assisted development

### Vercel — Frontend Deployment Platform

**Install**: `npm i -g vercel`

**Core workflow**:
```bash
vercel                       # Deploy from current directory
vercel --prod                # Deploy to production
vercel env pull .env.local   # Sync env vars to local
vercel dev                   # Local dev with serverless functions
vercel logs <url>            # Stream production logs
```

**Full-stack pattern** (Vercel + Supabase):
```
Vercel (frontend: Next.js, React, Svelte, etc.)
  ↕ REST/GraphQL
Supabase (backend: Postgres + Auth + Storage + Edge Functions)
```

This is the recommended stack for rapid full-stack development:
- Vercel handles frontend hosting, CDN, edge rendering, preview deploys
- Supabase handles database, auth, storage, realtime, vectors
- Both have CLIs for local development that mirror production exactly

### CLI-Anything — Making ALL Software Agent-Native (HKUDS)

**Philosophy**: "Today's software serves humans. Tomorrow's users will be agents."
CLI is the universal interface — structured, composable, deterministic, self-describing.

**Install**:
```bash
# Claude Code plugin (recommended)
/plugin marketplace add HKUDS/CLI-Anything

# Manual
git clone https://github.com/HKUDS/CLI-Anything.git
cp -r CLI-Anything/cli-anything-plugin ~/.claude/plugins/cli-anything
```

**Generate a CLI for ANY software**:
```bash
# Full 7-phase pipeline (analyze → design → implement → test → doc → validate → publish)
/cli-anything:cli-anything ./gimp

# Refine with more commands (incremental, non-destructive)
/cli-anything:refine ./gimp "batch processing and filters"

# Validate the generated CLI
/cli-anything:validate ./gimp
```

**Generated CLI structure**:
```
<software>/agent-harness/
├── cli_anything/<software>/
│   ├── __init__.py
│   ├── cli.py              # Entry point
│   ├── commands/            # Subcommands
│   ├── tests/               # Unit + E2E tests
│   ├── skills/SKILL.md      # AI-discoverable skill definition
│   └── utils/repl_skin.py   # Interactive REPL
├── <SOFTWARE>.md             # SOP document
├── setup.py
└── README.md
```

**Use generated CLI**:
```bash
cd <software>/agent-harness && pip install -e .
cli-anything-<software> --help                    # See all commands
cli-anything-<software>                           # Enter REPL mode
cli-anything-<software> --json <command>          # JSON output for agents
```

**Why this matters for the framework**:
- Every software can become agent-operable via CLI
- JSON output + `--help` = structured, self-describing interface
- REPL mode for interactive exploration
- Subcommand mode for scripting pipelines
- Works across Claude Code, OpenClaw, OpenCode, Codex, Copilot CLI
- CLI-Hub: central registry for community-contributed CLIs
