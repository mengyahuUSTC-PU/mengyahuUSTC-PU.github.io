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
    ("Meta AI Blog", "https://ai.meta.com/blog/rss/"),
    ("Mistral AI", "https://mistral.ai/feed.xml"),
    ("CAIS Newsletter", "https://newsletter.safe.ai/feed"),
    ("Import AI", "https://importai.substack.com/feed"),
    ("Don't Worry About the Vase", "https://thezvi.substack.com/feed"),
    ("Simon Willison", "https://simonwillison.net/atom/everything/"),
    ("Schneier on Security", "https://www.schneier.com/feed/atom/"),
    ("Krebs on Security", "https://krebsonsecurity.com/feed/"),
    ("Google Project Zero", "https://googleprojectzero.blogspot.com/feeds/posts/default"),
    ("Stanford HAI", "https://hai.stanford.edu/rss.xml"),
    ("EU AI Act Newsletter", "https://artificialintelligenceact.eu/feed/"),
    # Anthropic has no official RSS; community mirror first, page-scrape fallback in fetcher.
    ("Anthropic News", "https://www.anthropic.com/rss.xml"),
]

# How many days back an item may be dated and still enter the pool.
MAX_AGE_DAYS = 3
