# Intelligence, Research & Prediction Patterns — Full Reference

## Crucix — Multi-Source Intelligence Agent

### Architecture
- **Runtime**: Node.js 22+ (native fetch, top-level await, ESM)
- **Deployment**: Docker Compose with health checks, port 3117
- **Real-time**: SSE (Server-Sent Events) for auto-refresh every 15 min
- **Persistence**: Volume-mounted `./runs/` directory
- **Config**: `.env` for all API keys (never hardcoded)

### Source Module Pattern
Each of 27+ sources is a standalone ESM module in `apis/sources/`:

```
apis/sources/
├── acled.mjs       # Armed Conflict data
├── adsb.mjs        # Flight tracking (ADS-B)
├── bls.mjs         # Bureau of Labor Statistics
├── firms.mjs       # NASA fire detection (FIRMS)
├── fred.mjs        # Federal Reserve economic data
├── gdelt.mjs       # Global events database
├── noaa.mjs        # Weather/climate
├── ofac.mjs        # OFAC sanctions lists
├── opensanctions.mjs # Open Sanctions
├── opensky.mjs     # Air traffic (OpenSky)
├── reddit.mjs      # Social sentiment
├── reliefweb.mjs   # Humanitarian data (UN)
├── safecast.mjs    # Radiation monitoring
├── ships.mjs       # Maritime AIS tracking
└── ...             # 27+ total
```

**Module contract**:
```javascript
// apis/sources/example.mjs
export async function fetchExampleData(config) {
  const { API_KEY } = config;
  try {
    const res = await fetch('https://api.example.com/data', {
      headers: { 'Authorization': `Bearer ${API_KEY}` }
    });
    if (!res.ok) return { status: 'unavailable', data: [] };
    const raw = await res.json();
    return {
      status: 'success',
      data: raw.items.map(item => ({
        id: item.id,
        type: 'example_signal',
        title: item.title,
        timestamp: item.created_at,
        location: item.coords ? { lat: item.coords.lat, lng: item.coords.lng } : null,
        confidence: calculateConfidence(item),
        metadata: { source: 'example' },
      })),
      timestamp: new Date().toISOString(),
    };
  } catch (error) {
    console.error(`[example] Error: ${error.message}`);
    return { status: 'error', data: [] };
  }
}
```

### Briefing Orchestrator
```javascript
// apis/briefing.mjs — run all sources in parallel
export async function runSweep(config) {
  const results = await Promise.allSettled(
    sources.map(source => source.fetch(config))
  );
  const data = results.map((r, i) => ({
    source: sourceNames[i],
    ...(r.status === 'fulfilled' ? r.value : { status: 'error', data: [] }),
  }));
  const alerts = correlateSignals(data);
  return { data, alerts, timestamp: new Date().toISOString() };
}
```

### Alert System
| Tier | Color | Meaning | Example |
|------|-------|---------|---------|
| FLASH | Red | Immediate action required | Major conflict escalation |
| PRIORITY | Yellow | Important, time-sensitive | Unusual flight patterns near border |
| ROUTINE | Blue | Informational | New sanctions designation |

Each alert: signal details + confidence score + cross-domain correlations.

### Cross-Domain Correlation
```javascript
function correlateSignals(allData) {
  const alerts = [];
  const fires = getSourceData(allData, 'firms');
  const flights = getSourceData(allData, 'adsb');

  for (const fire of fires) {
    const nearby = flights.filter(f => distanceKm(fire.location, f.location) < 50);
    if (nearby.length > 3) {
      alerts.push({
        tier: 'PRIORITY',
        type: 'fire_response_activity',
        confidence: 0.7 + (nearby.length * 0.05),
        sources: ['firms', 'adsb'],
        location: fire.location,
      });
    }
  }
  return alerts;
}
```

### Dashboard Features
- 3D WebGL globe (Globe.gl) + flat map toggle
- 9 marker types across both views
- Live market data (Yahoo Finance, no API key needed)
- Risk gauges (VIX, high-yield spread, supply chain index)
- OSINT feed from 17+ Telegram channels
- News ticker (RSS + GDELT + Telegram, auto-scrolling)

### Bot Integration
- Telegram: polling every 5s, slash commands (/brief, /sweep)
- Discord: slash commands + rich embed alerts (color-coded sidebars)
- Discord webhook fallback for lightweight setup

### Security
- Never render untrusted content with innerHTML unless sanitized
- Only safe URL schemes (http, https)
- All API keys via .env
- Token impersonation warnings

---

## AutoResearch — Autonomous Experiment Loops (Karpathy)

### Core Philosophy
Give an AI agent a small but real setup and let it experiment autonomously.
It modifies code, runs experiments, checks if results improved, keeps or
discards, and repeats.

### Three Primitives
1. **Editable Asset** (`train.py`): The single file the agent can modify.
   Confining changes here keeps the search space interpretable and every
   hypothesis reviewable as a diff.

2. **Scalar Metric** (`val_bpb`): The single number that determines success.
   Vocabulary-size-independent, allowing architecture changes between runs.
   Must be directly comparable across all experiments.

3. **Program Document** (`program.md`): Structured prose that carries
   instructions (what to search for), constraints (what must not change),
   and stopping criteria (when to stop). Markdown sits at the intersection
   of human editability and agent parseability.

### Experiment Loop
```
1. Check out a fresh branch
2. Modify train.py with an experimental idea
3. Run: `uv run train.py > run.log 2>&1`
4. Read results: `grep "^val_bpb:\|^peak_vram_mb:" run.log`
5. If val_bpb improved (lower) → advance branch (keep commit)
6. If val_bpb equal or worse → git reset (discard)
7. Record in results.tsv
8. Repeat
```

### Design Decisions
- Fixed 5-minute training budget per experiment (comparable regardless of changes)
- ~12 experiments/hour, ~100 overnight
- Self-contained: one GPU, one file, one metric
- prepare.py is read-only (data, tokenizer, eval)
- train.py is the ONLY editable file (model, optimizer, hyperparameters)

### Generalizable Pattern
This applies beyond ML training:
- Any optimization problem with an editable config + measurable metric
- Performance tuning (edit config → benchmark → keep/discard)
- Prompt engineering (edit prompt → evaluate → keep/discard)
- System configuration (edit params → test → keep/discard)

---

## MiroFish — Swarm Intelligence Prediction Engine

### Architecture
Multi-agent prediction engine powered by OASIS simulation:

```
Seed Input (news, data, policy drafts)
  → Knowledge Graph Construction (entity/relationship extraction, GraphRAG)
  → Environment Setup (persona generation, simulation parameters)
  → Parallel Simulation (thousands of agents with memory + personality)
  → Report Generation (ReportAgent with rich tool access)
  → Interactive Exploration (talk to any agent in the simulation)
```

### Key Concepts
- **Seed information**: Real-world data (breaking news, financial signals, policy drafts) extracted and structured
- **Digital parallel world**: High-fidelity simulation with thousands of agents
- **Agent properties**: Independent personality, long-term memory, behavioral logic
- **God's-eye view**: Dynamically inject variables to simulate scenarios
- **Emergence capture**: Collective patterns from individual interactions
- **Dual-platform simulation**: Parallel execution for speed

### Applications
- Financial direction prediction
- Political/policy impact forecasting
- Public opinion simulation
- Creative scenarios (novel ending prediction)
- Risk assessment and decision rehearsal

---

## GraphRAG — Knowledge Graph-Enhanced RAG

### From "Essential GraphRAG" (Bratanič & Hane, Manning 2025)

**Core insight**: Traditional RAG uses only unstructured data (text chunks + vector search).
GraphRAG adds structured knowledge graphs, enabling multi-hop reasoning across
connected entities and relationships.

### RAG Pipeline
```
Question → Retriever → Question + Relevant Documents → Generator (LLM) → Grounded Answer
            ↓
    Smart lookup in
    knowledge base
```

### Retrieval Strategies
| Strategy | Best For | How It Works |
|----------|----------|-------------|
| Vector similarity search | Broad topic matching | Embed chunks, cosine similarity |
| Hybrid search (vector + BM25) | Specific terms + semantics | Combine keyword and vector |
| Text-to-Cypher | Structured data questions | Generate graph queries from NL |
| Graph traversal | Multi-hop reasoning | Walk knowledge graph relationships |
| Agentic RAG | Mixed query types | LLM decides which strategy per query |

### Knowledge Graph Construction with LLMs
1. **Entity extraction**: LLM identifies entities from text
2. **Relationship mapping**: LLM identifies connections between entities
3. **Graph storage**: Neo4j or similar graph database
4. **Query interface**: Cypher queries generated from natural language

### When to Use GraphRAG
- Questions requiring connected information across documents
- Multi-hop reasoning ("Who worked with the person who invented X?")
- Queries mixing structured data (dates, numbers) with unstructured context
- Domain-specific systems (healthcare, finance, legal, technical support)

### Microsoft's GraphRAG Implementation
- Community detection on knowledge graphs
- Hierarchical summarization of communities
- Both local search (specific entities) and global search (themes across corpus)

### Key Design Patterns
- Bridge structured and unstructured data in a single system
- Use knowledge graphs for relationship-rich domains
- Vector search alone fails for queries requiring reasoning across connections
- Evaluation: measure retrieval precision, answer accuracy, hallucination rate

---

## HexStrike AI — Cybersecurity MCP Agents

### Overview
Advanced MCP server providing AI agents access to 150+ cybersecurity tools:
- Automated pentesting
- Vulnerability discovery
- Bug bounty automation
- Security research

### Integration
Works with Claude, GPT, Copilot via standard MCP protocol.
Bridges LLMs with real-world offensive security capabilities.

### Ethical Guidelines
- Always operate within authorized scope
- Obtain explicit permission before testing
- Follow responsible disclosure practices
- Reference OWASP, NIST, CIS benchmarks for defensive recommendations
- Never use for unauthorized access

---

## MCP Server Patterns (Cross-Cutting)

### Standard Structure
```
mcp-server/
├── src/
│   ├── index.ts          # Entry, server setup
│   ├── tools/            # Tool definitions
│   ├── utils/            # Shared utilities
│   └── types.ts          # Type definitions
├── package.json
└── README.md
```

### Tool Definition
```typescript
{
  name: "tool_name",
  description: "Clear description of what and when",
  inputSchema: {
    type: "object",
    properties: {
      url: { type: "string", description: "URL to process" },
      options: {
        type: "object",
        properties: {
          depth: { type: "number", default: 1 },
          format: { type: "string", enum: ["markdown", "html", "text"] }
        }
      }
    },
    required: ["url"]
  }
}
```

### Best Practices
1. Minimize token usage — extract/filter before sending to LLM
2. Structured error responses (JSON, not stack traces)
3. Auth via environment variables only
4. Support both SSE and stdio transports
5. Every tool needs clear description + JSON schema
6. Rate limiting server-side

---

## Ruflo — Self-Learning Agent Intelligence

### Learning Architecture

Ruflo implements a continuous self-learning loop that improves agent
coordination over time:

```
RETRIEVE — HNSW vector search finds relevant past patterns (150x faster, O(log n))
  ↓
JUDGE — Verdicts score each pattern as success or failure
  ↓
DISTILL — LoRA fine-tuning reinforces successful patterns
  ↓
CONSOLIDATE — EWC++ (Elastic Weight Consolidation) prevents catastrophic forgetting
```

### Memory Intelligence (AgentDB v3)

Three-tier memory with biological decay modeling:

```
Working Memory (hot, fast, ephemeral)
  ↓ consolidation after task completion
Episodic Memory (session-level, time-tagged)
  ↓ pattern extraction over time
Semantic Memory (long-term, concept-level)
```

Ebbinghaus forgetting curves + spaced repetition determine what gets
retained vs forgotten. Memories accessed frequently get promoted;
rarely-used memories decay naturally.

### Intelligent Model Routing

3-tier routing saves up to 75% on API costs:

| Tier | Model Class | Used For |
|------|-------------|----------|
| Strategic | Strong (Opus) | Planning, architecture, complex decisions |
| Tactical | Mid-tier (Sonnet) | Code generation, execution, implementation |
| Operational | Lightweight (Haiku) | Research, verification, simple lookups |

The router learns which model tier produces the best results for each
task type and adjusts routing automatically.

### ReasoningBank WASM

Rust-compiled WASM kernels power the intelligence layer:
- Hash-based embeddings (no external API keys needed)
- Pattern-based reasoning with semantic understanding
- 4-factor Maximal Marginal Relevance scoring:
  - 40% Semantic Similarity
  - 20% Recency
  - 20% Importance
  - 20% Diversity
- 2-3ms query latency

### SONA (Self-Organizing Neural Architecture)

Q-learning + neural reinforcement for agent selection:
- Agents that succeed at certain task types get higher selection scores
- Failed agents get lower scores for that task type
- Over time, the system learns optimal agent-task assignments

### Integration with Existing Intelligence Patterns

Ruflo complements the other intelligence frameworks:
- **Crucix** provides external intelligence (27 OSINT sources) → Ruflo orchestrates agents that process and act on that intelligence
- **AutoResearch** provides the experiment loop → Ruflo provides the multi-agent swarm to run experiments in parallel
- **MiroFish** provides swarm prediction → Ruflo provides the orchestration layer to coordinate prediction agents
- **GraphRAG** provides knowledge graph retrieval → Ruflo's AgentDB provides the vector memory backend
- **claude-mem** provides session capture → Ruflo's ReasoningBank provides persistent cross-session memory

---

## Multi-Objective Optimization — Optuna/TPE Patterns

### Core Concept

When tuning any system with parameters that affect competing metrics, use
automated Bayesian optimization rather than manual search or grid search.
This pattern generalizes from Heretic's TPE-based parameter optimizer and
applies to any domain: ML hyperparameters, system configs, prompt engineering,
pipeline tuning, build optimization.

### TPE (Tree-structured Parzen Estimator)

TPE is a Bayesian optimization method that models the search space using
two density estimators rather than a Gaussian process:

```
For each trial:
  1. Split all previous trials into "good" (top γ%) and "bad" (rest)
  2. Fit kernel density estimator l(x) to "good" trial params
  3. Fit kernel density estimator g(x) to "bad" trial params
  4. Sample candidates from l(x)
  5. Pick the candidate that maximizes l(x) / g(x)
  6. Evaluate, record, repeat
```

**Why TPE over alternatives**:
- Handles tree-structured (conditional) search spaces natively
- Scales better than Gaussian Processes for high-dimensional spaces
- Supports categorical, integer, and continuous parameters in the same search
- Robust default — works well without tuning the optimizer itself

### Single-Objective Pattern

```python
import optuna

def objective(trial):
    # Suggest parameters from search space
    learning_rate = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
    batch_size = trial.suggest_categorical("batch_size", [16, 32, 64, 128])
    n_layers = trial.suggest_int("n_layers", 1, 8)

    # Build and evaluate system with these params
    score = train_and_evaluate(learning_rate, batch_size, n_layers)
    return score  # Optuna minimizes by default

study = optuna.create_study(
    sampler=optuna.samplers.TPESampler(multivariate=True),
    pruner=optuna.pruners.HyperbandPruner(),  # Kill bad trials early
)
study.optimize(objective, n_trials=100)
print(study.best_params)
```

### Multi-Objective / Dual-Objective Pattern

Co-minimize two competing metrics. This yields a Pareto front — a set of
solutions where improving one metric necessarily worsens the other. The user
then picks their preferred trade-off from the front.

```python
import optuna

def dual_objective(trial):
    param_a = trial.suggest_float("param_a", 0.0, 1.0)
    param_b = trial.suggest_int("param_b", 1, 100)

    # Two competing metrics
    task_performance = evaluate_task(param_a, param_b)     # Minimize
    baseline_divergence = measure_kl_divergence(param_a, param_b)  # Minimize

    return task_performance, baseline_divergence

study = optuna.create_study(
    directions=["minimize", "minimize"],  # Co-minimize both
    sampler=optuna.samplers.TPESampler(),
)
study.optimize(dual_objective, n_trials=200)

# Get Pareto-optimal solutions (best trade-offs)
pareto_trials = study.best_trials
for trial in pareto_trials:
    print(f"Task: {trial.values[0]:.4f}, KL Div: {trial.values[1]:.4f}, "
          f"Params: {trial.params}")
```

### Pruning for Efficiency

Kill unpromising trials early to save 3-5x compute:

| Pruner | Best For | How It Works |
|--------|----------|-------------|
| MedianPruner | General use | Prune if below median of completed trials |
| HyperbandPruner | Neural networks | Multi-fidelity successive halving |
| SuccessiveHalvingPruner | Budget-constrained | Allocate more resources to promising trials |

```python
# Report intermediate values during trial
for epoch in range(100):
    metric = train_one_epoch()
    trial.report(metric, epoch)
    if trial.should_prune():
        raise optuna.TrialPruned()  # Stop this trial early
```

### When to Apply This Pattern

- **ML hyperparameter tuning**: Learning rate, architecture, optimizer params
- **System configuration**: Thread pools, cache sizes, timeout values
- **Prompt engineering**: Temperature, top-p, system prompt variants (use metric as score)
- **Pipeline optimization**: Chunk size, concurrency, retry strategy
- **Build optimization**: Compiler flags, bundle splitting strategy
- **Any A/B testing with measurable metrics**: Define objective, let TPE search

### Visualization

```python
optuna.visualization.plot_pareto_front(study)           # Multi-obj trade-offs
optuna.visualization.plot_param_importances(study)       # Which params matter most
optuna.visualization.plot_optimization_history(study)    # Convergence over trials
optuna.visualization.plot_slice(study)                   # Per-parameter effects
```

---

## KL Divergence as a Quality Preservation Metric

### Core Principle

When modifying any system, you want to improve a target metric WITHOUT
degrading the system's baseline capabilities. KL divergence (Kullback-Leibler
divergence) quantifies how much the modified system's behavior distribution
has drifted from the original.

**The dual-objective formula**:
```
minimize: task_metric(modified_system)
minimize: KL(modified_system || original_system)
```

This ensures modifications are surgical — improving the target while
preserving everything else.

### Mathematical Definition

KL(P || Q) = Σ P(x) · log(P(x) / Q(x))

Where P is the modified distribution and Q is the original baseline.
- KL = 0 means identical behavior
- Higher KL means more drift from baseline
- It's asymmetric: KL(P||Q) ≠ KL(Q||P)

### Practical Applications

**Model modification**: When fine-tuning, adapting, or modifying any ML model,
track KL divergence from the base model to ensure capabilities are preserved.

**Config changes**: When changing system configuration, compare output
distributions before and after to catch unintended behavioral shifts.

**Pipeline migration**: When rewriting or migrating a pipeline, KL divergence
between old and new output distributions validates functional equivalence.

**Prompt iteration**: When refining prompts, measure output distribution
similarity to ensure improvements in one area haven't degraded others.

### Implementation Pattern

```python
import torch
import torch.nn.functional as F

def measure_kl_divergence(original_logits, modified_logits):
    """Measure how much the modified system has drifted from baseline."""
    original_probs = F.softmax(original_logits, dim=-1)
    modified_log_probs = F.log_softmax(modified_logits, dim=-1)
    kl_div = F.kl_div(modified_log_probs, original_probs, reduction="batchmean")
    return kl_div.item()
```

### Synergy with AutoResearch

AutoResearch's scalar metric pattern (one number determines success) can
be extended to a dual metric using the KL divergence approach:
- **Primary metric**: task-specific score (val_bpb, accuracy, latency)
- **Guard metric**: KL divergence from baseline (ensures no regression)
- **Decision rule**: Accept change only if primary improves AND KL stays below threshold

---

## Auto-Benchmarking — System Profiling Before Optimization

### Core Pattern

Before running any expensive optimization or training loop, benchmark
the system to find the optimal operating point. This ensures all
subsequent experiments run at maximum efficiency and are directly comparable.

### The Pattern (from Heretic, generalized)

```
1. PROFILE: Detect available hardware (GPU VRAM, CPU cores, memory)
2. PROBE: Run progressively larger workloads until resource limits are hit
3. SET: Lock the optimal batch size / concurrency for all subsequent runs
4. RUN: All experiments use the same resource allocation (fair comparison)
```

### Implementation

```python
def auto_benchmark(workload_fn, resource_range):
    """Find optimal resource allocation by progressive probing."""
    best_throughput = 0
    best_config = None

    for config in resource_range:
        try:
            throughput = workload_fn(config)
            if throughput > best_throughput:
                best_throughput = throughput
                best_config = config
        except (RuntimeError, MemoryError):
            break  # Hit resource ceiling, use previous best

    return best_config
```

### When to Apply

- Before ML training loops (find max batch size for VRAM)
- Before crawling campaigns (find max concurrency before rate limiting)
- Before parallel agent swarms (find max agents before coordination overhead)
- Before load testing (find system saturation point)
- Before any experiment loop where resource allocation affects results

---

## Transformer Interpretability Techniques

### Residual Stream Analysis

Transformers build representations through a residual stream — each layer
adds its contribution to a running total. Analyzing these intermediate
representations reveals how the model processes information.

**Compute hidden states per layer**:
```python
outputs = model(input_ids, output_hidden_states=True)
hidden_states = outputs.hidden_states  # Tuple of (batch, seq_len, hidden_dim)
# hidden_states[0] = embeddings
# hidden_states[i] = output of layer i
# hidden_states[-1] = final layer output
```

**Compare representations between input categories**:
```python
def compute_mean_residuals(model, tokenizer, prompts):
    """Get mean hidden state per layer across a set of prompts."""
    all_hidden = []
    for prompt in prompts:
        inputs = tokenizer(prompt, return_tensors="pt", padding=True)
        outputs = model(**inputs, output_hidden_states=True)
        # Take first token's hidden state at each layer
        layer_states = [h[:, 0, :] for h in outputs.hidden_states]
        all_hidden.append(torch.stack(layer_states))
    return torch.stack(all_hidden).mean(dim=0)  # (n_layers, hidden_dim)
```

### Directional Analysis in Activation Space

To understand which dimensions of the hidden state encode specific behaviors,
compute the difference vector between two categories of inputs:

```python
mean_category_a = compute_mean_residuals(model, tokenizer, category_a_prompts)
mean_category_b = compute_mean_residuals(model, tokenizer, category_b_prompts)
direction_vector = mean_category_a - mean_category_b
# This vector points in the direction that distinguishes A from B
# Useful for: understanding what the model has learned, debugging behavior,
# identifying which layers are most discriminative
```

### Practical Applications

- **Debugging model behavior**: Find which layers contribute most to unexpected outputs
- **Feature attribution**: Understand what representations drive specific predictions
- **Layer importance**: Identify which layers matter most for specific capabilities
- **Representation drift**: Track how fine-tuning changes internal representations by comparing hidden states before and after

### Integration with AutoResearch

These interpretability techniques combine naturally with the AutoResearch
experiment loop: modify the model → measure hidden state changes → understand
WHY the modification helped or hurt → inform the next experiment.

---

## Skill Ecosystem & Library Patterns

### Antigravity Awesome Skills (1,326+ skills)

The largest installable skill library for AI coding agents. Key architectural patterns:

**Installation**: `npx antigravity-awesome-skills` auto-detects your tool and copies skills to the right location.

```bash
npx antigravity-awesome-skills --claude    # → ~/.claude/skills/
npx antigravity-awesome-skills --cursor    # → .cursor/skills/
npx antigravity-awesome-skills --codex     # → ~/.codex/skills/
npx antigravity-awesome-skills --gemini    # → ~/.gemini/antigravity/skills/
npx antigravity-awesome-skills --claude --codex  # Multi-tool
```

**Bundles** (curated skill sets by role):
- Web Dev Essentials, Backend Starter, Security Auditor, DevOps Pipeline
- Use bundles to bootstrap, then add individual skills as needed

**Workflows** (step-by-step playbooks):
- Design-DDD-Core-Domain, Security-Audit-Pipeline, Deploy-Kubernetes
- Each workflow chains multiple skills in sequence

**Invocation**: `@skill-name` syntax in agent prompt. Chain: `@brainstorming → @react-patterns → @tdd`

**Plugin marketplace** (Claude Code):
```
/plugin marketplace add sickn33/antigravity-awesome-skills
/plugin install antigravity-awesome-skills
```

### Awesome MCP Servers (appcypher — curated catalog)

500+ MCP servers organized by category:

| Category | Examples |
|----------|---------|
| Databases | PostgreSQL, MongoDB, Redis, SQLite, Supabase |
| Dev Tools | GitHub, GitLab, Jira, Linear, Sentry |
| Cloud | AWS, GCP, Azure, Cloudflare, Vercel |
| AI/ML | Hugging Face, Replicate, Weights & Biases |
| Scraping | Firecrawl, Scrapling, Crawl4AI, Exa |
| Productivity | Notion, Slack, Gmail, Google Drive, Obsidian |
| Finance | Stripe, Plaid, Yahoo Finance, Coinbase |
| Security | Snyk, SonarQube, OWASP ZAP, HexStrike |

**Discovery pattern**: Browse catalog → pick server → `claude mcp add <name>` → use immediately.

### Awesome Claude Code (hesreallyhim — curated resources)

Curated skills, hooks, slash-commands, agent orchestrators, and plugins:
- Skills: 200+ community skills with quality ratings
- Hooks: Pre/post tool-use hooks for automation
- Orchestrators: Ruflo, Superpowers, GSD, and more
- Best practices for skill authoring and hook integration

---

## Nacos — Dynamic Service & Agent Registry (Alibaba, 32K stars)

### Architecture

Nacos provides three core capabilities for distributed systems:

1. **Service Discovery**: Services register + discover each other via DNS/HTTP
2. **Dynamic Configuration**: Centralized config management across all environments
3. **Service Management**: Health checks, weighted routing, load balancing

### Agent-to-Agent (A2A) Protocol

Nacos v3.1+ supports A2A registry for AI agents:

```
Agent publishes AgentCard to Nacos registry
  → Other agents discover by name/skills/tags
  → Direct agent-to-agent communication
  → No central orchestrator needed
```

**AgentCard**: Describes agent capabilities, endpoints, skills, and tags.
Discovery is currently by name, with skills/tags/descriptions planned.

### MCP Server Registry

Nacos can serve as a centralized MCP server registry:
- Import MCP servers into Nacos console
- Enable/disable servers dynamically
- Health check endpoints
- Batch registration of agent endpoints
- `overrideExisting` option for version updates

### Nacos Copilot

AI-powered assistant integrated into Nacos console:
- Optimize and create Prompts/Skills
- Intelligently discover existing skills from registry
- Auto-suggest configurations

### Key Patterns for the Framework

- **Dynamic config**: No redeployment for config changes — applies to agent skill loading, model routing, API key rotation
- **Health checks**: Real-time monitoring of service/agent health — prevents routing to dead endpoints
- **Weighted routing**: Load balance across multiple agent instances or LLM providers
- **Provider fallback**: If primary provider fails, auto-switch to next — same pattern as ValueCell's fallback chain

---

## ValueCell — Multi-Agent Financial Platform

### Architecture

```
ValueCell Platform
  ├── DeepResearch Agent — fundamental analysis, document retrieval, data insights
  ├── Strategy Agent — multi-asset, multi-strategy smart trading
  ├── News Retrieval Agent — personalized scheduled news with alerts
  ├── Exchange Connectors — OKX, Binance, HyperLiquid, Coinbase (with guardrails)
  └── Provider System — multi-LLM with automatic fallback
```

### Provider Fallback Chain Pattern

When the primary LLM provider fails, ValueCell automatically tries fallbacks:

```yaml
models:
  primary:
    model_id: "anthropic/claude-haiku-4.5"
    provider: "openrouter"
  provider_models:
    siliconflow: "zai-org/GLM-4.6"
    google: "gemini-2.5-flash"
```

**Resolution order**: Environment variables → .env file → defaults.yaml
**Auto-detection**: `AUTO_DETECT_PROVIDER=true` finds providers from available API keys.

### Trading Guardrails

- Exchange connectivity with built-in safety limits
- Virtual trading mode for strategy testing (no real money)
- All sensitive credentials stored locally only
- Connection testing before live trading

### A2A Protocol Integration

ValueCell supports LangChain and Agno via A2A protocol:
- Agents from different frameworks can communicate
- Research agents feed findings to Strategy agents
- Strategy agents send signals to Exchange connectors
- Community agent marketplace for contributed agents

### Generalizable Patterns

- **Provider fallback chains** apply to any multi-provider system (LLMs, APIs, databases)
- **Agent guardrails** apply to any automated system touching real resources
- **Local-first data security** is the right default for sensitive operations
- **Virtual/sandbox mode** for testing before production is essential for any consequential automation
