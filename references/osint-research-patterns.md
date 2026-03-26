# OSINT & Professional Research Patterns — Full Reference

## The Intelligence Cycle (Universal Methodology)

This isn't just for security — it's the gold standard for ANY structured
research: job hunting, market analysis, competitive intelligence, lead
generation, academic research, journalism.

```
1. DIRECTION    — Define exactly what you need to know
2. COLLECTION   — Gather data from multiple sources
3. PROCESSING   — Clean, deduplicate, normalize, structure
4. ANALYSIS     — Find patterns, connections, gaps, insights
5. DISSEMINATION — Present findings in actionable format
```

**Application examples**:
- Job search: Direction (target companies + roles) → Collection (harvest emails,
  map org structures) → Processing (deduplicate contacts) → Analysis (identify
  hiring managers, warm intros) → Dissemination (outreach plan)
- Market research: Direction (competitor domains) → Collection (theHarvester on
  each domain) → Processing (normalize) → Analysis (compare tech stacks,
  team sizes) → Dissemination (report)

---

## Maltego — Entity-Transform-Graph Framework (Complete)

### Core Architecture

Maltego's power comes from three primitives that chain together:

```
Entity  →  Transform  →  New Entities  →  More Transforms  →  Graph
  ↑                                                              │
  └──────────── Visual investigation map ────────────────────────┘
```

**Entity**: A typed data node. Represents one piece of information:
- Domain (company.com)
- Person (Jane Smith)
- Email Address (jane@company.com)
- Phone Number
- Company/Organization
- Location
- Social Media Profile
- IP Address, DNS Name, URL
- Custom entity types (you can create your own via inheritance)

**Transform**: A function that takes an entity as input and produces new
entities as output. This is how graphs grow — exactly like an investigation:
start with what you know, derive what you don't.

**Graph**: The visual map of all entities and their relationships. Edges
show how one entity was derived from another via transforms.

### Entity Properties & Attributes

Every entity has:
- **Type** (Domain, Person, Email, etc.)
- **Value** (the primary data point, e.g., "company.com")
- **Properties** (additional metadata, e.g., creation date, registrar)
- **Icon** (visual representation on the graph)
- **Overlay properties** (displayed on the icon for quick visual scanning)

### Transform Types

| Transform Category | What It Does | Example |
|-------------------|-------------|---------|
| DNS Transforms | Domain → DNS records, IPs, nameservers | To DNS Name [Find common DNS names] |
| Whois Transforms | Domain → registration info, admin emails, phone | To Email [From whois] |
| Email Transforms | Email → person, company, social profiles | To Person, To Phone |
| Social Media | Person/Email → social profiles, connections | To Facebook, To LinkedIn |
| Company | Domain → technologies, employees, subsidiaries | To Website Tech, To Person |
| Infrastructure | IP → geolocation, ASN, services | To Location, To Netblock |

### Transform Chaining (The Power Pattern)

This is where Maltego becomes a research superweapon. Transforms chain:

```
company.com (Domain)
  → [To DNS Name] → mail.company.com, www.company.com, vpn.company.com
  → [To IP Address] → 203.0.113.5, 203.0.113.6
  → [To Email from Whois] → admin@company.com, tech@company.com
  → [To Person] → Jane Smith (admin), Bob Jones (tech)
  → [To Social Profile] → linkedin.com/in/janesmith, twitter.com/bobjones
```

Each step expands the graph, revealing connections invisible from any
single starting point.

### Maltego Machines (Automated Transform Sequences)

Machines are pre-built chains that run multiple transforms automatically:
- **Company Stalker**: Domain → all discoverable emails + employee names
- **Footprint L1/L2/L3**: Progressive network discovery (shallow → deep)
- **Person - Email Address**: Name → email addresses across sources

You can build custom machines for your specific research workflow.

### Custom Entities

Create domain-specific entity types via inheritance:
```
Person (base entity)
  ├── Hiring Manager (custom — inherits Person transforms)
  ├── Recruiter (custom)
  └── Peer Contact (custom)
```

Custom entities inherit all transforms from their parent type, plus
you can add properties specific to your use case (e.g., "department",
"seniority level", "open headcount").

### Professional Research Workflow with Maltego

**Job hunting / company mapping**:
1. Start with target company domain entity
2. Run DNS + Whois transforms → discover infrastructure + admin contacts
3. Run email transforms → find publicly listed employee emails
4. Run social media transforms → find LinkedIn profiles
5. Run company transforms → discover subsidiaries, related domains
6. Analyze graph → identify hiring managers, warm introduction paths

**Competitive analysis**:
1. Add competitor domains as entities
2. Run technology detection transforms → see their tech stack
3. Run job posting transforms → see what roles they're hiring for
4. Compare graphs side-by-side → find gaps and opportunities

### Installation & Editions

- **Community Edition (CE)**: Free, 24 results per transform, 10,000 entities per graph, 200 credits/month
- **Pro**: Higher limits, commercial transform hub, export capabilities
- **Enterprise**: Unlimited, team collaboration, real-time graph sharing

```
# Download from maltego.com, install, create free account
# Then: Transform Hub → install free data sources
# API keys required for most data sources (many have free tiers)
```

---

## theHarvester — Multi-Source Email & Domain Intelligence (Complete)

### Overview

Python CLI tool that queries 40+ public data sources simultaneously
to gather emails, names, subdomains, IPs, and URLs for a target domain.
Essential for job prospecting and company research.

### Installation

```bash
# Via pip (recommended)
pip install theHarvester

# Via package manager (Kali)
sudo apt install theharvester

# Via git
git clone https://github.com/laramies/theHarvester.git
cd theHarvester
pip install -r requirements.txt
```

### Core Usage Patterns

**Find all emails for a company domain**:
```bash
theHarvester -d company.com -b all -l 500
```
- `-d`: target domain
- `-b`: data source (`all` = every source, or specify: `google,bing,linkedin,hunter`)
- `-l`: limit results (default 500)

**Search specific sources for better results**:
```bash
# Search engines (no API key needed)
theHarvester -d company.com -b google,bing,duckduckgo

# Professional networks (great for job hunting)
theHarvester -d company.com -b linkedin,hunter

# Certificate transparency (finds subdomains)
theHarvester -d company.com -b crtsh,certspotter

# All passive sources (comprehensive)
theHarvester -d company.com -b all -l 1000
```

**Export results**:
```bash
# JSON output
theHarvester -d company.com -b all -f results.json

# XML output
theHarvester -d company.com -b all -f results.xml
```

### Data Sources (40+)

**No API key required** (start here):
- google, bing, duckduckgo — search engines
- crtsh, certspotter — certificate transparency logs
- dnsdumpster — DNS records and relationships
- hackertarget — network intelligence
- otx — AlienVault open threat exchange
- rapiddns — DNS enumeration
- threatminer — threat intelligence data

**Free tier with API key** (register for better results):
- hunter — email pattern detection + verification (50 req/month free)
- shodan — internet device search
- censys — certificate and host search
- securitytrails — historical DNS data
- fullhunt — attack surface discovery
- bevigil — mobile app OSINT
- intelx — Intelligence X multi-index search

**Configuration**: API keys go in `/etc/theHarvester/api-keys.yaml`:
```yaml
apikeys:
  hunter:
    key: your-hunter-api-key
  shodan:
    key: your-shodan-api-key
  intelx:
    key: your-intelx-api-key
```

### Output Data Types

theHarvester returns structured data in these categories:
- **Emails**: Individual email addresses found across all sources
- **Hosts**: Subdomains and related hostnames
- **IPs**: IP addresses resolved from discovered hosts
- **URLs**: Interesting URLs found during search
- **People/Names**: Employee names found in search results

### Professional Research Workflow

**Job hunting — find who to contact**:
```bash
# Step 1: Discover company email pattern
theHarvester -d targetcompany.com -b hunter -l 100
# Hunter reveals pattern: {first}.{last}@targetcompany.com

# Step 2: Find employee names
theHarvester -d targetcompany.com -b linkedin,google -l 500
# Returns names of employees

# Step 3: Construct target emails
# Pattern + names = john.doe@targetcompany.com

# Step 4: Verify with Hunter.io
# hunter.io/verify/john.doe@targetcompany.com
```

**Company research — understand the org**:
```bash
# Full reconnaissance
theHarvester -d company.com -b all -l 1000 -f company_report

# Then analyze:
# - Email naming convention reveals organizational structure
# - Subdomains reveal product lines (app., api., dev., staging.)
# - Certificate data reveals tech stack
```

---

## Hunter.io — Email Pattern Detection & Verification

### Core Capabilities

- **Domain search**: Find all publicly known email addresses for a domain
- **Email pattern detection**: Infer `{first}.{last}@domain.com` patterns
- **Email verification**: Check if a specific address is deliverable
- **Email finder**: Given a name + domain, predict the email address

### API Usage Pattern

```python
import requests

HUNTER_API_KEY = os.environ["HUNTER_API_KEY"]

# Domain search — find all emails for a company
def find_company_emails(domain):
    resp = requests.get("https://api.hunter.io/v2/domain-search", params={
        "domain": domain,
        "api_key": HUNTER_API_KEY
    })
    data = resp.json()["data"]
    return {
        "pattern": data.get("pattern"),        # e.g. "{first}.{last}"
        "emails": [e["value"] for e in data.get("emails", [])],
        "organization": data.get("organization"),
    }

# Email finder — predict email for a specific person
def find_email(domain, first_name, last_name):
    resp = requests.get("https://api.hunter.io/v2/email-finder", params={
        "domain": domain,
        "first_name": first_name,
        "last_name": last_name,
        "api_key": HUNTER_API_KEY
    })
    return resp.json()["data"]

# Email verification — check deliverability
def verify_email(email):
    resp = requests.get("https://api.hunter.io/v2/email-verifier", params={
        "email": email,
        "api_key": HUNTER_API_KEY
    })
    return resp.json()["data"]["status"]  # "valid", "invalid", "accept_all"
```

### Free Tier: 25 searches/month, 50 verifications/month

---

## SpiderFoot — Publisher/Subscriber Module Architecture

### Architecture Pattern (applicable to any data pipeline)

SpiderFoot's 200+ modules use a publisher/subscriber model:

```
Module A produces Event Type X
  → Module B subscribes to Event Type X
    → Module B produces Event Type Y
      → Module C subscribes to Event Type Y
        → ... chain continues automatically
```

**Why this matters**: You don't manually orchestrate the pipeline. Each
module declares what it consumes and what it produces. The framework
automatically routes data between modules. This is a powerful pattern
for building any multi-source data aggregation system.

### Module Contract

```python
class SpiderFootModule:
    # What this module consumes (subscribes to)
    watchedEvents = ["DOMAIN_NAME"]

    # What this module produces (publishes)
    producedEvents = ["EMAILADDR", "HUMAN_NAME"]

    # The actual processing
    def handleEvent(self, event):
        domain = event.data
        emails = self.query_source(domain)
        for email in emails:
            self.notifyListeners("EMAILADDR", email)
```

### Target Types

SpiderFoot can start from:
- IP address, domain name, hostname, subnet, ASN
- Email address, phone number, person name, username
- Bitcoin address, company name

### Scan Modes

| Mode | Use Case | Depth |
|------|----------|-------|
| All | Maximum discovery | Every module runs |
| Footprint | External attack surface | Focus on infrastructure |
| Investigate | Deep dive on specific entity | Follow all leads |
| Passive | No direct contact with target | Only third-party sources |

### Installation

```bash
wget https://github.com/smicallef/spiderfoot/archive/v4.0.tar.gz
tar zxvf v4.0.tar.gz && cd spiderfoot-4.0
pip3 install -r requirements.txt
python3 ./sf.py -l 127.0.0.1:5001
# Web UI opens at http://127.0.0.1:5001
```

### CLI Usage

```bash
# Scan a domain for emails only (strict mode)
python3 sf.py -s company.com -t EMAILADDR -f -x -q

# Full scan with JSON output
python3 sf.py -s company.com -o json > results.json
```

---

## Sherlock — Username Profile Discovery

### Usage (for professional networking research)

```bash
# Install
pipx install sherlock-project

# Search for a username across 400+ platforms
sherlock targetusername

# Search with output to file
sherlock targetusername --output results.txt

# Export as CSV/Excel
sherlock targetusername --csv
sherlock targetusername --xlsx

# Limit to specific sites
sherlock targetusername --site LinkedIn --site GitHub --site Twitter

# Use Tor for privacy
sherlock targetusername --tor

# Search variations (replaces ? with _, -, .)
sherlock "target{?}username"
```

### Professional Applications

- Verify a recruiter's or contact's identity across platforms
- Find a hiring manager's professional profiles before outreach
- Check your own digital footprint before job applications
- Discover which platforms a company's team is active on

---

## IntelligenceX SDK — Multi-Index Search API

### Architecture

IntelligenceX indexes data across multiple source types and provides
a unified search API:

```python
import requests

IX_API_KEY = os.environ["INTELX_API_KEY"]
IX_BASE = "https://2.intelx.io"

# Search across all indexes
def search_intelx(query, max_results=10):
    # Start search
    resp = requests.post(f"{IX_BASE}/intelligent/search", json={
        "term": query,
        "maxresults": max_results,
        "media": 0,  # 0=all
        "sort": 2,   # relevance
        "terminate": []
    }, headers={"x-key": IX_API_KEY})
    search_id = resp.json()["id"]

    # Fetch results
    results = requests.get(
        f"{IX_BASE}/intelligent/search/result",
        params={"id": search_id},
        headers={"x-key": IX_API_KEY}
    )
    return results.json().get("records", [])
```

### Indexed Sources

Public web, darknet, documents, leaks, WHOIS history, DNS records,
and more — unified under one search interface.

---

## Defensive: Audit Your Own Exposure

All these tools work best when pointed at your own infrastructure:

```bash
# What does the world see about your domain?
theHarvester -d yourdomain.com -b all -l 1000

# Full automated audit of your exposure
python3 sf.py -s yourdomain.com  # SpiderFoot

# Check if your usernames are exposed
sherlock yourusername
```

This follows ECC's security-first principle: understand your own
attack surface before someone else does.

---

## Combining Tools: The Professional Research Pipeline

### Job Hunting Pipeline

```
1. DIRECTION: Identify 10 target companies by domain

2. COLLECTION (parallel — use theHarvester + Hunter.io):
   theHarvester -d company1.com -b all    # Find emails + employee names
   theHarvester -d company2.com -b all    # Repeat per company
   Hunter.io domain search                 # Get email patterns

3. PROCESSING:
   - Deduplicate emails across sources
   - Extract naming patterns ({first}.{last}@, {f}{last}@)
   - Cross-reference names with LinkedIn profiles

4. ANALYSIS (use Maltego graph):
   - Map entities: Company → Departments → People → Roles
   - Identify hiring managers and team leads
   - Find warm introduction paths (shared connections)
   - Rank companies by fit (open roles, team size, tech stack)

5. DISSEMINATION:
   - Build targeted outreach list with verified emails
   - Personalize each message using discovered context
   - Track responses and iterate
```

### Company Research Pipeline

```
1. Start with domain entity in Maltego
2. Run theHarvester for email discovery
3. Run SpiderFoot for deep infrastructure mapping
4. Run Sherlock on discovered usernames for social profiles
5. Use Hunter.io to verify email deliverability
6. Build entity-relationship graph in Maltego
7. Export findings as structured report
```

### Integration with Existing Framework Patterns

- **Crucix** provides real-time intelligence signals → combine with OSINT
  tools for deeper investigation of specific signals
- **Scrapling/Crawl4AI** can scrape additional context from discovered
  URLs and profiles
- **GraphRAG** patterns apply directly to Maltego's entity-relationship
  graphs — same knowledge graph thinking
- **SpiderFoot's pub/sub module pattern** mirrors Crucix's source module
  architecture — design your own pipelines the same way

---

## Persuasion Engineering — Cold Outreach That Wins

These are legitimate, research-backed techniques that make cold emails
genuinely compelling to both human readers and AI screening systems.
No tricks — just structural excellence that performs well under any evaluation.

### The AIDA-R Framework (Attention-Interest-Desire-Action-Research)

```
ATTENTION  — First line hooks with specific, researched context
INTEREST   — Demonstrate relevant capability in 1-2 sentences
DESIRE     — Show concrete value you bring (quantified if possible)
ACTION     — Clear, low-friction next step
RESEARCH   — Every email is grounded in real research about the recipient
```

### Structure That Performs Well Everywhere

**Subject line**: Specific and relevant, not generic. Reference something
real about the company — a recent product launch, a hiring post, a tech
decision. This signals effort and relevance.

**Opening line**: Never "I hope this finds you well." Instead, lead with
something that proves you've done research: a specific project they shipped,
a blog post they wrote, a challenge they mentioned publicly.

**Value proposition**: Not "I have 5 years of experience in X." Instead,
"I built [specific thing] that [specific result]. Here's how that maps to
[specific challenge you're facing based on my research]."

**Proof points**: Link to portfolio, GitHub, or a specific artifact. One
concrete example beats ten abstract claims.

**Call to action**: One specific, low-commitment ask. "Would a 15-minute
call on Thursday work?" not "Let me know if you're interested."

### Writing Patterns That Score Well With Any Evaluator

1. **Specificity over generality**: "Reduced API latency from 340ms to 45ms
   using connection pooling" beats "experienced in performance optimization"

2. **Evidence over claims**: Link to working code, live projects, or
   measurable results. Verifiable > impressive-sounding.

3. **Mirror their language**: If the job post says "we need someone who can
   own the data pipeline," use "own" and "data pipeline" in your email.
   This is called lexical alignment — it signals understanding, not mimicry.

4. **Conciseness**: 4-6 sentences for the body. Respect the reader's time.
   If they want more, your links provide depth.

5. **Personalization at scale**: Use theHarvester/Hunter.io data to research
   each recipient's role and recent activity. Then write a unique opening
   line per email. Template the middle, personalize the edges.

### Cold Email Template (grounded in research)

```
Subject: [Specific reference to their work/company]

Hi [First Name],

[1 sentence showing you've researched them — reference a specific project,
blog post, or public statement they made]

I'm a [role] who [1-2 sentences of relevant, specific capability with
concrete proof points]. [Link to evidence].

[1 sentence connecting your capability to their specific need — this is
where your OSINT research pays off]

Would [specific low-commitment ask] work for you?

[Your name]
[Portfolio/GitHub link]
```

### Combining OSINT Research + Persuasion

The full pipeline:
1. **theHarvester** → find the right email addresses at target company
2. **Hunter.io** → verify deliverability + discover email patterns
3. **Maltego** → map company structure, identify hiring managers
4. **Sherlock** → find hiring manager's professional content (blog, talks)
5. **Research their public output** → read their latest blog/talk/interview
6. **Write personalized opening line** using what you found
7. **Apply AIDA-R framework** with real evidence
8. **Verify email** before sending (Hunter.io verification)
9. **Track and iterate** — if no response in 5 days, follow up with NEW value

### Defensive: Making YOUR Content AI-Screening-Resilient

Rather than trying to trick AI screeners, make your content genuinely
high-quality so it scores well under any evaluation:

- **Structured clearly** — headings, bullet points, clear sections
- **Evidence-dense** — every claim has a link or proof point
- **Keyword-aligned** — naturally includes terminology from the job description
- **Concise and scannable** — respects both human attention and token budgets
- **Authentic voice** — reads like a real person, not a template

This approach works whether the evaluator is human, AI, or both — because
it optimizes for genuine quality, not system exploitation.
