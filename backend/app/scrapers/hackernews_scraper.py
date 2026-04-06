"""
DevPulse — Hacker News Scraper
Uses the HN Algolia API for top tech stories.
"""
import logging
import httpx
from app.models import RawUpdateCreate, SourceType

logger = logging.getLogger("devpulse.scrapers.hackernews")

HN_SEARCH_URL = "https://hn.algolia.com/api/v1/search"

# Tags that signal developer-relevant content
SEARCH_QUERIES = [
    "new framework",
    "release",
    "open source tool",
    "developer tool",
    "programming language",
    "javascript",
    "python",
    "rust",
    "devops",
    "cloud",
]


def fetch_stories(max_per_query: int = 5) -> list[RawUpdateCreate]:
    """Fetch top developer-relevant stories from Hacker News."""
    updates: list[RawUpdateCreate] = []
    seen_titles: set[str] = set()

    for query in SEARCH_QUERIES:
        try:
            resp = httpx.get(
                HN_SEARCH_URL,
                params={
                    "query": query,
                    "tags": "story",
                    "hitsPerPage": max_per_query,
                    "numericFilters": "points>20",
                },
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            for hit in data.get("hits", []):
                title = hit.get("title", "").strip()
                if not title or title in seen_titles:
                    continue
                seen_titles.add(title)

                url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID', '')}"
                story_text = hit.get("story_text") or hit.get("comment_text") or ""

                updates.append(
                    RawUpdateCreate(
                        source_type=SourceType.HACKERNEWS,
                        title=title,
                        raw_content=story_text[:2000] if story_text else title,
                        source_url=url,
                    )
                )
        except httpx.HTTPError as e:
            logger.error(f"HN request error for query '{query}': {e}")
            continue

    logger.info(f"HN scraper fetched {len(updates)} stories")
    return updates
