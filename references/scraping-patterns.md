# Web Scraping Patterns — Complete Decision Tree & Code Reference

## Decision Tree: Which Tool for Which Job

```
What do you need?
│
├─ LLM-friendly markdown (RAG/GPT pipelines)?
│  ├─ Via Claude MCP tool call → Firecrawl MCP Server
│  └─ Via Python code → Crawl4AI
│
├─ Adaptive selectors (survive site redesigns)?
│  └─ → Scrapling (parser learns from changes, auto-relocates elements)
│
├─ Anti-bot bypass (Cloudflare, Akamai, DataDome)?
│  ├─ Cloudflare Turnstile → Scrapling StealthyFetcher
│  ├─ Enterprise anti-bot → Scrapling + Hyper Solutions API
│  ├─ General headless stealth → Scrapling DynamicFetcher or Crawlee Playwright
│  └─ Agent-based adaptive → OpenClaw Ultra Scraping
│
├─ Production-scale distributed crawling?
│  ├─ Python → Scrapy (middleware pipeline, extensions, Scrapyd)
│  └─ Node.js → Crawlee JS (auto-scaling, Apify cloud)
│
├─ Browser automation + scraping combined?
│  ├─ Python → Crawlee Python (Parsel, BeautifulSoup, Playwright)
│  └─ Node.js → Crawlee JS (Cheerio, JSDOM, Puppeteer, Playwright)
│
├─ Semantic/neural web search?
│  └─ → Exa MCP Server
│
├─ Download ebooks/light novels?
│  └─ → lightnovel-crawler
│
└─ Simple single-page fetch?
   └─ → Scrapling Fetcher (lightweight, fast, no browser)
```

## Scrapling — Adaptive Web Scraping (Python)

**Install**: `pip install "scrapling[fetchers]"` then `scrapling install`

**Fetcher hierarchy** (use the simplest one that works):
1. `Fetcher` / `AsyncFetcher` — lightweight HTTP, no browser overhead
2. `DynamicFetcher` — Chromium-based, for JS-rendered pages
3. `StealthyFetcher` — full fingerprint masking, anti-bot bypass

**Adaptive parsing** (selectors survive redesigns):
```python
from scrapling.fetchers import StealthyFetcher

StealthyFetcher.adaptive = True
page = StealthyFetcher.fetch('https://example.com', headless=True, network_idle=True)
products = page.css('.product', auto_save=True)  # Learns selector patterns
for p in products:
    print(p.css('h2::text').get(), p.css('.price::text').get())
```

**Spider framework** (v0.4+ for full crawls):
```python
from scrapling.spiders import Spider, Response

class ProductSpider(Spider):
    name = "products"
    start_urls = ["https://store.example.com/"]

    async def parse(self, response: Response):
        for product in response.css('.product-card'):
            yield {
                "name": product.css('h2::text').get(),
                "price": product.css('.price::text').get(),
                "url": product.css('a::attr(href)').get(),
            }
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

# Streaming mode for long crawls
async for item in ProductSpider().stream():
    process(item)
```

**Proxy rotation**:
```python
from scrapling import ProxyRotator
rotator = ProxyRotator(["http://proxy1:8080", "http://proxy2:8080"])
page = Fetcher.get(url, proxy_rotator=rotator)
```

**Key features**: Interactive IPython shell, CLI mode (`scrapling fetch <url>`),
auto CSS/XPath selector generation, DOM navigation (parent/sibling/child),
pause/resume checkpoints, real-time stats, built-in MCP server.

---

## Crawl4AI — LLM-Friendly Crawler (Python)

**Install**: `pip install crawl4ai` then `crawl4ai-setup`

**Core pattern**:
```python
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun(url="https://example.com")
    print(result.markdown)            # Clean LLM-ready markdown
    print(result.extracted_content)   # Structured data
```

**LLM extraction** (structured data via any LLM):
```python
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: str = Field(description="Product name")
    price: str = Field(description="Product price")

strategy = LLMExtractionStrategy(
    provider="openai/gpt-4o",
    schema=Product.schema(),
    instruction="Extract all products"
)
result = await crawler.arun(url=url, extraction_strategy=strategy)
```

**CSS extraction** (no LLM needed):
```python
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
schema = {
    "name": "Product Extractor",
    "baseSelector": ".product-card",
    "fields": [
        {"name": "title", "selector": "h2", "type": "text"},
        {"name": "price", "selector": ".price", "type": "text"},
    ]
}
strategy = JsonCssExtractionStrategy(schema)
```

**Key features**: Fit Markdown (heuristic noise removal), BM25 filtering,
cosine similarity chunking, multi-browser support, Docker deployment
(port 11235), REST API + playground UI, streaming via WebSocket.

---

## Firecrawl MCP Server — Claude-Native Scraping

**MCP config**:
```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": { "FIRECRAWL_API_KEY": "your-key" }
    }
  }
}
```

**Tools**: `scrape` (single URL → markdown), `map` (discover all URLs on domain),
`crawl` (full site with depth control), `search` (web search + content extraction).

---

## Scrapy — Production-Scale Python Crawling

```python
import scrapy

class ProductSpider(scrapy.Spider):
    name = "products"
    start_urls = ["https://store.example.com/"]
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0.5,
        'ROBOTSTXT_OBEY': True,
    }

    def parse(self, response):
        for product in response.css('.product'):
            yield {
                'name': product.css('h2::text').get(),
                'price': product.css('.price::text').get(),
            }
        yield from response.follow_all(response.css('a.next'), callback=self.parse)
```

**When to use**: Need middleware pipelines, item pipelines, extensions, distributed
execution via Scrapyd or Scrapy Cloud.

---

## Crawlee — Multi-Runtime Crawler (JS + Python)

**JavaScript** (Puppeteer/Playwright/Cheerio):
```javascript
import { PlaywrightCrawler } from 'crawlee';

const crawler = new PlaywrightCrawler({
    maxConcurrency: 10,
    requestHandler: async ({ page, request, enqueueLinks }) => {
        const title = await page.title();
        const data = await page.$$eval('.product', els =>
            els.map(el => ({
                name: el.querySelector('h2')?.textContent,
                price: el.querySelector('.price')?.textContent,
            }))
        );
        await enqueueLinks({ globs: ['https://store.example.com/**'] });
    },
});
await crawler.run(['https://store.example.com/']);
```

**Python** (Parsel/BeautifulSoup/Playwright):
```python
from crawlee.playwright_crawler import PlaywrightCrawler

crawler = PlaywrightCrawler(max_concurrency=10)

@crawler.router.default_handler
async def handler(context):
    data = await context.page.query_selector_all('.product')
    for item in data:
        title = await item.inner_text()
        context.log.info(f"Found: {title}")

await crawler.run(["https://store.example.com/"])
```

---

## Exa MCP Server — Semantic Web Search

Neural search + keyword search + content retrieval. Find content by meaning,
not just keywords.

---

## OpenClaw Ultra Scraping — Agent-Based Adaptive Scraping

Designed for OpenClaw agents. Bypasses anti-bot, survives site redesigns.
Part of the 339+ skill collection from OpenClaw Master Skills.

---

## lightnovel-crawler — Ebook Generation

Generate and download ebooks from online novel sources. Specialized for
light novel and web fiction platforms.

---

## Mandatory Patterns for ALL Scraping Code

### 1. Graceful Degradation
```python
async def fetch_source(url):
    try:
        response = await fetcher.get(url)
        return {"status": "success", "data": parse(response)}
    except (ConnectionError, TimeoutError) as e:
        return {"status": "unavailable", "data": [], "error": str(e)}
    except Exception as e:
        return {"status": "error", "data": [], "error": str(e)}
```

### 2. Rate Limiting Config
```python
SCRAPING_CONFIG = {
    "concurrent_requests": 8,
    "download_delay": 1.0,      # seconds between same-domain requests
    "per_domain_limit": 4,
    "retry_times": 3,
    "retry_delay": 5,
    "timeout": 30,
    "respect_robots_txt": True,
}
```

### 3. Consistent Output Schema
```python
{
    "source": "source_name",
    "timestamp": "ISO-8601",
    "url": "https://...",
    "status": "success|unavailable|error",
    "items": [{"id": "...", "title": "...", "content": "...", "metadata": {}}],
    "pagination": {"current_page": 1, "total_pages": 10, "next_url": "..."}
}
```

### 4. Proxy Rotation (always for production)
### 5. Checkpoint/Resume (for crawls > 100 pages)
### 6. Streaming (for long-running crawls: `async for item in spider.stream()`)
