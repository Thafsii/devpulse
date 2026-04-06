"""
DevPulse — GitHub Releases Scraper
Authenticated GitHub REST API with retry/backoff.
"""
import hashlib
import time
import logging
import httpx
from app.config import settings
from app.models import RawUpdateCreate, SourceType

logger = logging.getLogger("devpulse.scrapers.github")

TRACKED_REPOS = [
    "facebook/react",
    "vercel/next.js",
    "sveltejs/svelte",
    "vitejs/vite",
    "denoland/deno",
    "oven-sh/bun",
    "tailwindlabs/tailwindcss",
    "withastro/astro",
    "supabase/supabase",
    "django/django",
    "pallets/flask",
    "fastapi/fastapi",
    "pytorch/pytorch",
    "langchain-ai/langchain",
    "docker/compose",
    "kubernetes/kubernetes",
]

MAX_RETRIES = 3
RETRY_BACKOFF = 2  # seconds, exponential


def _headers() -> dict:
    h = {"Accept": "application/vnd.github+json"}
    if settings.GITHUB_PAT:
        h["Authorization"] = f"Bearer {settings.GITHUB_PAT}"
    return h


def _request_with_retry(url: str) -> dict | list | None:
    """GET with exponential retry on 403/429."""
    for attempt in range(MAX_RETRIES):
        try:
            resp = httpx.get(url, headers=_headers(), timeout=15)

            # Check rate-limit headers
            remaining = resp.headers.get("X-RateLimit-Remaining")
            if remaining and int(remaining) < 5:
                reset_at = int(resp.headers.get("X-RateLimit-Reset", 0))
                wait = max(reset_at - int(time.time()), 1)
                logger.warning(f"Rate limit nearly exhausted, sleeping {wait}s")
                time.sleep(min(wait, 60))

            if resp.status_code == 200:
                return resp.json()
            if resp.status_code in (403, 429):
                sleep_time = RETRY_BACKOFF ** (attempt + 1)
                logger.warning(f"GitHub {resp.status_code}, retry in {sleep_time}s")
                time.sleep(sleep_time)
                continue
            resp.raise_for_status()
        except httpx.HTTPError as e:
            logger.error(f"GitHub request error: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_BACKOFF ** (attempt + 1))
    return None


def fetch_releases() -> list[RawUpdateCreate]:
    """Fetch latest releases from tracked GitHub repos."""
    updates: list[RawUpdateCreate] = []

    for repo in TRACKED_REPOS:
        url = f"https://api.github.com/repos/{repo}/releases?per_page=3"
        data = _request_with_retry(url)
        if not data or not isinstance(data, list):
            continue

        for release in data:
            tag = release.get("tag_name", "")
            name = release.get("name", "") or tag
            body = release.get("body", "") or ""
            html_url = release.get("html_url", "")

            title = f"{repo.split('/')[-1]} {name}".strip()
            updates.append(
                RawUpdateCreate(
                    source_type=SourceType.GITHUB,
                    title=title,
                    raw_content=body[:2000],
                    source_url=html_url,
                )
            )

    logger.info(f"GitHub scraper fetched {len(updates)} releases")
    return updates
