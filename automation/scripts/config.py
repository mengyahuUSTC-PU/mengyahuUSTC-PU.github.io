"""Source configuration for the daily fetch pipeline."""

# Keywords that mark an arXiv paper / HN story as relevant.
# Checked case-insensitively against title + abstract/summary.
SAFETY_KEYWORDS = [
    "alignment",
    "jailbreak",
    "red team",
    "red-team",
    "safety eval",
    "safety evaluation",
    "content moderation",
    "interpretability",
    "watermark",
    "guardrail",
    "hallucination",
    "prompt injection",
    "adversarial",
    "responsible ai",
    "ai governance",
    "ai regulation",
    "ai policy",
]

# Broader AI/tech keywords for Hacker News (brand scope: AI-first, not safety-only).
HN_KEYWORDS = SAFETY_KEYWORDS + [
    "llm",
    "gpt",
    "claude",
    "gemini",
    "openai",
    "anthropic",
    "deepmind",
    "language model",
    "transformer",
    "agent",
    "ai ",
    " ai",
    "machine learning",
    "security",
    "vulnerability",
    "exploit",
]

ARXIV_CATEGORIES = ["cs.AI", "cs.CL", "cs.CR", "cs.CY"]
ARXIV_MAX_RESULTS = 200

HN_TOP_LIMIT = 30

# RSS/Atom feeds. Every entry: (source name, feed url).
# A failing feed is skipped and noted in the output, never fatal.
RSS_FEEDS = [
    ("OpenAI Blog", "https://openai.com/news/rss.xml"),
    ("Google DeepMind Blog", "https://deepmind.google/blog/rss.xml"),
    ("Mistral AI", "https://mistral.ai/rss.xml"),
    ("CAIS Newsletter", "https://newsletter.safe.ai/feed"),
    # Substack blocks Azure datacenter IPs; both authors mirror on WordPress.
    ("Import AI", "https://jack-clark.net/feed/"),
    ("Don't Worry About the Vase", "https://thezvi.wordpress.com/feed/"),
    ("Simon Willison", "https://simonwillison.net/atom/everything/"),
    ("Schneier on Security", "https://www.schneier.com/feed/atom/"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/"),
    ("Google Project Zero", "https://googleprojectzero.blogspot.com/feeds/posts/default"),
    ("EU AI Act Newsletter", "https://artificialintelligenceact.eu/feed/"),
    # Big tech + industry (added 2026-07-19: broaden beyond safety-lab circle)
    ("Google AI Blog", "https://blog.google/technology/ai/rss/"),
    ("NVIDIA Blog", "https://blogs.nvidia.com/feed/"),
    ("TechCrunch AI", "https://techcrunch.com/category/artificial-intelligence/feed/"),
]

# Sources with no working feed (verified 2026-07): scrape the index page and
# extract article links. Fragile by design; failures are logged and skipped.
# (name, page url, href regex, url prefix to make links absolute)
SCRAPE_SOURCES = [
    ("Anthropic News", "https://www.anthropic.com/news", r'href="(/news/[^"#?]+)"', "https://www.anthropic.com"),
    ("Meta AI Blog", "https://ai.meta.com/blog/", r'href="(/blog/[^"#?]+)"', "https://ai.meta.com"),
    ("Stanford HAI", "https://hai.stanford.edu/news", r'href="(/news/[^"#?]+)"', "https://hai.stanford.edu"),
    # Chinese labs + star startups without feeds (added 2026-07-19)
    ("Moonshot/Kimi Blog", "https://www.kimi.com/blog", r'href="(/blog/[^"#?]+)"', "https://www.kimi.com"),
    ("DeepSeek News", "https://api-docs.deepseek.com/news/", r'href="(/news/[^"#?]+)"', "https://api-docs.deepseek.com"),
    ("Thinking Machines", "https://thinkingmachines.ai/news", r'href="(/news/[^"#?][^"#?]*)"', "https://thinkingmachines.ai"),
]

# How many days back an item may be dated and still enter the pool.
MAX_AGE_DAYS = 3
