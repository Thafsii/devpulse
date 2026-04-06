"""
DevPulse — Product Hunt GraphQL Client
Uses the official PH GraphQL API to fetch new product launches.
"""
import logging
import httpx
from app.config import settings
from app.models import RawUpdateCreate, SourceType

logger = logging.getLogger("devpulse.scrapers.producthunt")

PH_API_URL = "https://api.producthunt.com/v2/api/graphql"

QUERY = """
query GetPosts($first: Int!, $topic: String) {
  posts(first: $first, topic: $topic, order: RANKING) {
    edges {
      node {
        id
        name
        tagline
        votesCount
        createdAt
        url
        description
        topics {
          edges {
            node {
              name
            }
          }
        }
      }
    }
  }
}
"""

DEVELOPER_TOPICS = [
    "developer-tools",
    "open-source",
    "artificial-intelligence",
    "saas",
    "devops",
    "web-development",
]


def fetch_launches(posts_per_topic: int = 5) -> list[RawUpdateCreate]:
    """Fetch new developer-oriented product launches from Product Hunt."""
    if not settings.PRODUCTHUNT_TOKEN:
        logger.warning("PRODUCTHUNT_TOKEN not set — skipping Product Hunt scraper")
        return []

    headers = {
        "Authorization": f"Bearer {settings.PRODUCTHUNT_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    updates: list[RawUpdateCreate] = []
    seen_ids: set[str] = set()

    for topic in DEVELOPER_TOPICS:
        try:
            resp = httpx.post(
                PH_API_URL,
                json={"query": QUERY, "variables": {"first": posts_per_topic, "topic": topic}},
                headers=headers,
                timeout=15,
            )
            resp.raise_for_status()
            data = resp.json()

            posts = data.get("data", {}).get("posts", {}).get("edges", [])
            for edge in posts:
                node = edge.get("node", {})
                post_id = node.get("id", "")
                if post_id in seen_ids:
                    continue
                seen_ids.add(post_id)

                name = node.get("name", "")
                tagline = node.get("tagline", "")
                description = node.get("description", "") or tagline
                url = node.get("url", "")
                votes = node.get("votesCount", 0)

                raw_text = f"{name}: {tagline}. {description} (Votes: {votes})"

                updates.append(
                    RawUpdateCreate(
                        source_type=SourceType.PRODUCTHUNT,
                        title=f"{name} — {tagline}",
                        raw_content=raw_text[:2000],
                        source_url=url,
                    )
                )
        except httpx.HTTPError as e:
            logger.error(f"PH request error for topic '{topic}': {e}")
            continue

    logger.info(f"Product Hunt client fetched {len(updates)} launches")
    return updates
