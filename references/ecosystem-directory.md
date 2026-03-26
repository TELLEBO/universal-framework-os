# Ecosystem Directory — 1,326+ Skills + 500+ MCP Servers + 200+ Resources

This is the complete searchable directory for the agentic skill and MCP ecosystem.
When you need a specific capability, search this file by keyword to find the right
tool, then install it using the patterns below.

## How to Install

### Skills (from Antigravity Awesome Skills — 1,326+)

```bash
# One-line install (copies ALL skills to your agent's skill directory)
npx antigravity-awesome-skills              # Default: ~/.gemini/antigravity/skills/
npx antigravity-awesome-skills --claude     # → ~/.claude/skills/
npx antigravity-awesome-skills --cursor     # → .cursor/skills/
npx antigravity-awesome-skills --codex      # → ~/.codex/skills/
npx antigravity-awesome-skills --gemini     # → ~/.gemini/antigravity/skills/
npx antigravity-awesome-skills --kiro       # → ~/.kiro/skills/

# Claude Code plugin marketplace
/plugin marketplace add sickn33/antigravity-awesome-skills
/plugin install antigravity-awesome-skills

# Manual clone
git clone https://github.com/sickn33/antigravity-awesome-skills.git .agent/skills
```

### MCP Servers (from awesome-mcp-servers — 500+)

```bash
# General pattern
claude mcp add <server-name> -- npx -y <package-name> mcp start

# Or in settings.json / claude.json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": { "API_KEY": "your-key" }
    }
  }
}
```

### Invocation

```
# Claude Code
>> Use @skill-name to help me with this task

# Cursor
@skill-name help me do X

# Gemini CLI / Codex CLI
Use the skill-name skill to do X
```

---

## SKILLS BY CATEGORY (1,326+ from Antigravity Awesome Skills)

### Design & UI/UX
algorithmic-art, canvas-design, frontend-design, ui-ux-pro-max, web-artifacts-builder,
theme-factory, brand-guidelines, figma-to-code, responsive-design, design-system-builder,
accessibility-checker, color-theory, typography-guide, layout-patterns, tailwind-expert,
shadcn-ui-builder, framer-motion, animation-patterns, svg-optimization, icon-design

### Frontend Development
react-patterns, react-native-architecture, nextjs-app-router, nextjs-turbopack,
vue-composition, angular-v20, svelte-5, astro-framework, nuxt-patterns, remix-patterns,
solid-js, htmx-patterns, web-components, state-management, css-architecture,
performance-optimization, bundle-optimization, pwa-builder, electron-app, tauri-app

### Backend Development
api-design, rest-api-best-practices, graphql-patterns, trpc-patterns, fastapi-patterns,
django-patterns, express-patterns, nestjs-architecture, spring-boot, rails-patterns,
laravel-patterns, golang-patterns, rust-backend, elixir-phoenix, serverless-patterns,
microservices-architecture, event-driven, cqrs-patterns, message-queue-patterns

### Database & Data
postgresql-expert, mysql-patterns, mongodb-patterns, redis-patterns, elasticsearch,
prisma-patterns, drizzle-orm, typeorm-patterns, database-migration, query-optimization,
data-modeling, time-series-db, vector-database, supabase-patterns, firebase-patterns,
dynamodb-patterns, cassandra-patterns, neo4j-patterns, clickhouse, snowflake-patterns

### Testing & QA
test-driven-development, jest-patterns, vitest-patterns, playwright-testing, cypress-testing,
pytest-patterns, testing-library, storybook-testing, api-testing, load-testing,
k6-load-testing, mutation-testing, contract-testing, e2e-patterns, test-data-generation,
snapshot-testing, visual-regression, accessibility-testing, security-testing, chaos-testing

### DevOps & Infrastructure
docker-patterns, kubernetes-patterns, terraform-patterns, ansible-patterns, ci-cd-pipeline,
github-actions, gitlab-ci, aws-patterns, azure-patterns, gcp-patterns, cloudflare-patterns,
nginx-patterns, monitoring-setup, logging-patterns, alerting-patterns, incident-response,
infrastructure-as-code, gitops-patterns, helm-charts, prometheus-grafana

### Security
ethical-hacking-methodology, api-security-best-practices, auth-implementation-patterns,
owasp-top-ten, penetration-testing, secure-coding, cryptography-patterns, jwt-security,
oauth2-patterns, rbac-patterns, cors-configuration, csp-headers, vulnerability-scanning,
dependency-audit, secrets-management, zero-trust-architecture, soc2-compliance

### AI/ML & LLM
prompt-engineering, rag-patterns, langchain-patterns, vector-search, embedding-strategies,
fine-tuning-guide, llm-evaluation, agent-patterns, mcp-builder, claude-api-patterns,
openai-api-patterns, huggingface-patterns, mlops-pipeline, model-deployment,
feature-engineering, data-pipeline, experiment-tracking, ai-safety-patterns

### Mobile Development
react-native-architecture, expo-patterns, flutter-patterns, swift-ui-patterns,
kotlin-android, ios-debugger-agent, mobile-performance, app-store-optimization,
push-notifications, deep-linking, offline-first, biometric-auth, in-app-purchases

### Documentation & Writing
documentation-generator, api-docs, architecture-docs, readme-generator, changelog-generator,
technical-writing, blog-post-writer, content-strategy, seo-optimizer, markdown-expert,
latex-paper-conversion, slide-deck-builder, knowledge-base-builder

### Project Planning & Management
brainstorming, blueprint, progressive-estimation, project-planning, sprint-planning,
backlog-grooming, requirements-gathering, user-story-writer, roadmap-builder,
decision-matrix, risk-assessment, retrospective-facilitator, standup-generator

### Code Quality & Refactoring
code-reviewer, refactoring-patterns, clean-code, solid-principles, design-patterns,
performance-profiling, memory-leak-detection, dead-code-removal, code-complexity,
naming-conventions, error-handling-patterns, logging-best-practices, tech-debt-tracker

### Git & Version Control
git-workflow, conventional-commits, merge-strategy, monorepo-patterns, branch-strategy,
code-review-checklist, pr-template, release-management, git-hooks, git-bisect-guide

### Marketing & Growth
seo-optimizer, content-marketing, social-media-strategy, email-marketing, a-b-testing,
analytics-setup, conversion-optimization, landing-page-builder, copywriting-frameworks,
product-launch, growth-hacking, audience-analysis, competitor-analysis

### Business & Finance
business-plan-writer, pitch-deck, financial-modeling, investor-materials, market-research,
pricing-strategy, unit-economics, okr-framework, jobgpt (job search automation)

### Official Skills (from Anthropic, Vercel, OpenAI, Remotion)
anthropic/docx, anthropic/pdf, anthropic/pptx, anthropic/xlsx, anthropic/brand-guidelines,
anthropic/internal-comms, vercel/react-best-practices, vercel/web-design-guidelines,
openai/skill-creator, openai/concise-planning, remotion/video-creation (28 rules)

---

## BUNDLES (Curated Starter Packs by Role)

| Bundle | Key Skills |
|--------|-----------|
| **Essentials** | brainstorming, code-reviewer, test-driven-development, git-workflow |
| **Web Wizard** | react-patterns, nextjs-app-router, tailwind-expert, api-design |
| **Full-Stack Developer** | frontend + backend + database + testing essentials |
| **Security Developer** | ethical-hacking, owasp, auth-patterns, secure-coding |
| **DevOps & Cloud** | docker, kubernetes, terraform, ci-cd-pipeline, monitoring |
| **QA & Testing** | tdd, playwright, jest, load-testing, api-testing |
| **Mobile Developer** | react-native, expo, flutter, ios/android patterns |
| **AI/ML Engineer** | prompt-engineering, rag-patterns, langchain, mcp-builder |
| **OSS Maintainer** | changelog, readme, pr-template, release-management |
| **Data Engineer** | postgresql, query-optimization, data-modeling, etl-patterns |
| **Azure Developer** | azure-functions, azure-ai, azd-deployment, azure-identity |
| **Growth/Marketing** | seo-optimizer, content-marketing, analytics, landing-page |

**Recommended combos**:
- Building a SaaS MVP → Essentials + Full-Stack + QA
- Hardening production → Security + DevOps + Observability
- Shipping OSS → Essentials + OSS Maintainer

---

## WORKFLOWS (Step-by-Step Playbooks)

| Workflow | What It Does |
|----------|-------------|
| design-ddd-core-domain | Domain-driven design from scratch |
| security-audit-pipeline | Full security audit workflow |
| deploy-kubernetes | K8s deployment from zero |
| ci-cd-setup | GitHub Actions pipeline setup |
| api-first-development | Design-first API development |
| database-migration | Zero-downtime schema migration |
| performance-audit | Full perf audit + optimization |
| incident-response | On-call incident handling |

---

## MCP SERVERS BY CATEGORY (500+ from awesome-mcp-servers)

### File Systems & Storage
Filesystem, Backup, FileStash (SFTP/S3/FTP/SMB/NFS/WebDAV), S3, GCS,
Azure Blob, OneDrive, Google Drive, Dropbox, Box

### Databases
PostgreSQL, MySQL, MongoDB, MongoDB Lens, Redis, SQLite, Supabase,
Firebase, DynamoDB, Cassandra, Neo4j, Qdrant, Pinecone, Weaviate,
Snowflake, BigQuery, TiDB, NocoDB, Airtable, Couchbase, CentralMind/Gateway

### Version Control & Dev Tools
GitHub (multiple), GitLab, Git, Phabricator, GitKraken, Azure DevOps,
Linear, Jira, Gitingest-MCP, GitHub Repos Manager (80+ tools)

### Web Search & Scraping
Firecrawl, Exa Search, Kagi Search, Brave Search, Google News, SearXNG,
Playwright, Browserbase, Apify Actors, RAG Web Browser, Bright Data,
Scrapeless, Search1API, Websearch

### Communication & Productivity
Slack, Discord, Telegram, Microsoft Teams, WhatsApp, Gmail, Outlook,
Notion, Obsidian, Apple Notes, Todoist, Google Calendar, CalDAV

### Cloud Platforms
Cloudflare (Workers/KV/R2/D1), AWS, GCP, Azure, Kubernetes, Docker,
Tinybird, Vercel, Netlify, Railway, Fly.io

### AI/ML & LLM
Hugging Face, Replicate, Weights & Biases, OpenAI, Anthropic,
LangSmith, Logfire, Langfuse, Context7

### Finance & Crypto
AlphaVantage, Yahoo Finance, Stripe, Plaid, Coinbase, Binance,
CoinGecko, Bankless Onchain, Bitcoin/Lightning, Claude YFinance

### Security
Snyk, SonarQube, OWASP ZAP, HexStrike (150+ tools), Security Scanner,
Dependency Audit, CVE Database

### Marketing & Content
Open Strategy Partners, SEO tools, Content moderation, Analytics,
Campaign management

### Workflow Automation
Make (scenarios as tools), n8n, Zapier, GitHub Actions, Pipedream

### System & Shell
Shell (Mac), Windows CLI, Docker, System Monitor, Process Manager

### Monitoring & Observability
Sentry, Datadog, Prometheus, Grafana, New Relic, Metoro (K8s),
Raygun, VictoriaMetrics, Last9

### Specialized
TradingView, Shopify, Zendesk, Pipedrive, Salesforce, HubSpot,
Twilio, SendGrid, Resend, Lingo.dev (i18n), Career Site Jobs

---

## AWESOME CLAUDE CODE RESOURCES (hesreallyhim — 200+ curated)

### Featured Skills Collections
- **Claude Scientific Skills** (K-Dense) — Research, science, engineering, analysis, finance, writing. One of the best skills repos on GitHub.
- **Antigravity Awesome Skills** (sickn33) — 1,326+ skills, searchable catalog, bundles, workflows, CLI installer (see above)
- **Claude CodePro** (Max Ritter) — Professional dev environment: spec-driven workflow, TDD enforcement, cross-session memory, semantic search, quality hooks
- **AB Method** (Ayoub Bensalah) — Spec-driven workflow transforming large problems into focused missions using sub agents
- **Agentic Workflow Patterns** (ThibautMelen) — Comprehensive agentic patterns: Subagent Orchestration, Progressive Skills, Parallel Tool Calling, Master-Clone Architecture, Wizard Workflows

### Agent Orchestrators
- **Auto-Claude** (AndyMik90) — Autonomous multi-agent coding framework, full SDLC, kanban UI
- **Claude Code Flow** (ruvnet) — Code-first orchestration: write, edit, test, optimize autonomously across recursive agent cycles
- **Claude Squad** (smtg-ai) — Terminal app managing multiple Claude Code/Codex/Aider agents in separate workspaces simultaneously
- **Claude Swarm** (parruda) — Launch Claude Code connected to a swarm of agents
- **Claude Task Master** (eyaltoledano) — Task management for AI-driven development, Cursor integration
- **sudocode** (ssh-randy) — Lightweight agent orchestration living in your repo
- **YACO** — Yet Another Claude Orchestrator: agents, commands, Output Styles

### Hooks & Security
- **parry** (Dmytro Onypko) — Prompt injection scanner for hooks, scans inputs/outputs for injection attacks, secrets, exfiltration
- **Dippy** (Lily Dayton) — Auto-approve safe bash via AST parsing, block destructive ops. Claude Code + Gemini CLI + Cursor
- **TDD Hooks** — File operation monitor that blocks changes violating TDD principles
- **Claude Communicator** — Real-time inter-agent communication via hooks, @-mention targeting, live dashboard

### Applications & Bridges
- **Untether** — Telegram bridge for Claude Code (+ 5 other agents): voice tasks, streaming, inline approvals, cost tracking
- **Claude Code GitHub Actions** — Official CI/CD integration for AI-powered workflows
- **SkillHub** — 7,000+ AI-evaluated skills with playground, usage dashboard, analytics

### Learning Resources
- **Claude Code Tips** (ykdojo) — 35+ tips: voice input, prompt patching, container workflows, conversation cloning, multi-model orchestration
- **Claude Code Ultimate Guide** (Florian BRUNIAUX) — Beginner to power user: templates, agentic workflows, quizzes, cheatsheet

### Key Patterns
- Skills: Progressive disclosure (~100 tokens metadata → <5K full → resources on demand)
- Subagents: Fork for isolation (skill context doesn't pollute main conversation)
- Hooks: PreToolUse, PostToolUse, UserPromptSubmit, Stop, SessionStart
- Context modes: `inline` (always in context), `fork` (isolated subagent), `disable-model-invocation: true` (manual-only)
- Ralph Wiggum technique: Remarkably detailed approach for working with Claude Code's constraints

---

## DISCOVERY PATTERN

When you need a specific capability:

1. **Search this file** by keyword (e.g., "stripe", "kubernetes", "seo")
2. **Find the skill or MCP name**
3. **Install**:
   - Skill: `@skill-name` in your prompt (if installed) or clone from Antigravity
   - MCP: `claude mcp add <name> -- npx -y <package>` or add to settings.json
4. **Chain skills** for complex workflows: `@brainstorming → @api-design → @tdd → @deployment`

### Quick Lookup by Need

| I need to... | Skill | MCP Server |
|--------------|-------|-----------|
| Build a React app | @react-patterns, @nextjs-app-router | — |
| Set up authentication | @auth-implementation-patterns | Supabase, Firebase |
| Deploy to cloud | @docker-patterns, @kubernetes | Cloudflare, AWS, Vercel |
| Write tests | @test-driven-development, @playwright | — |
| Search the web | — | Firecrawl, Exa, Brave, SearXNG |
| Manage database | @postgresql-expert, @prisma | PostgreSQL, MongoDB, Supabase |
| Handle payments | — | Stripe, Plaid, Coinbase |
| Send notifications | — | Slack, Discord, Telegram, Twilio |
| Monitor production | @monitoring-setup | Sentry, Datadog, Prometheus |
| Audit security | @ethical-hacking, @owasp | HexStrike, Snyk, SonarQube |
| Generate docs | @documentation-generator | — |
| Plan project | @brainstorming, @blueprint | — |
| Optimize SEO | @seo-optimizer | Google Search Console |
| Build MCP server | @mcp-builder | — |
| Track finances | — | AlphaVantage, Stripe, Yahoo Finance |
| Automate workflows | — | Make, n8n, Zapier, GitHub Actions |
| Search jobs | @jobgpt | Career Site Jobs |
| Manage files | — | Filesystem, S3, Google Drive, Box |
