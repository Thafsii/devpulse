"""
DevPulse — Background Job Scheduler
Uses APScheduler BackgroundScheduler to run scrapers periodically.
"""
import logging
from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.triggers.interval import IntervalTrigger
from app.config import settings
from app.services.supabase_client import SupabaseNotConfiguredError

logger = logging.getLogger("devpulse.scheduler")


def _insert_raw_updates(updates):
    """Insert raw updates into Supabase, skipping duplicates via content_hash.
    
    Returns 0 silently when Supabase is not configured (no .env credentials).
    """
    if not updates:
        return 0

    from app.services.supabase_client import get_supabase

    try:
        sb = get_supabase()
    except SupabaseNotConfiguredError as e:
        logger.warning(f"Skipping Supabase insert — {e}")
        return 0

    inserted = 0

    for update in updates:
        try:
            sb.table("raw_updates").insert(
                {
                    "source_type": update.source_type.value,
                    "title": update.title,
                    "raw_content": update.raw_content,
                    "source_url": update.source_url,
                    "content_hash": update.content_hash,
                    "is_processed": False,
                }
            ).execute()
            inserted += 1
        except Exception as e:
            # Likely duplicate constraint violation — skip silently
            if "duplicate" in str(e).lower() or "unique" in str(e).lower():
                continue
            logger.error(f"Insert error: {e}")

    logger.info(f"Inserted {inserted}/{len(updates)} raw updates")
    return inserted


def collect_github_releases():
    """Job: fetch GitHub releases and store in raw_updates."""
    try:
        from app.scrapers.github_scraper import fetch_releases
        updates = fetch_releases()
        _insert_raw_updates(updates)
    except Exception as e:
        logger.error(f"GitHub collection job failed: {e}")


def collect_hackernews_stories():
    """Job: fetch HN stories and store in raw_updates."""
    try:
        from app.scrapers.hackernews_scraper import fetch_stories
        updates = fetch_stories()
        _insert_raw_updates(updates)
    except Exception as e:
        logger.error(f"HN collection job failed: {e}")


def collect_producthunt_launches():
    """Job: fetch Product Hunt launches and store in raw_updates."""
    try:
        from app.scrapers.producthunt_client import fetch_launches
        updates = fetch_launches()
        _insert_raw_updates(updates)
    except Exception as e:
        logger.error(f"Product Hunt collection job failed: {e}")


def process_raw_updates():
    """Job: process unprocessed raw_updates through the hybrid AI pipeline."""
    try:
        from app.services.supabase_client import get_supabase
        from app.ai.processor import process_raw_update

        try:
            sb = get_supabase()
        except SupabaseNotConfiguredError as e:
            logger.warning(f"Skipping process job — {e}")
            return
        result = (
            sb.table("raw_updates")
            .select("*")
            .eq("is_processed", False)
            .limit(50)
            .execute()
        )

        if not result.data:
            logger.info("No unprocessed raw updates")
            return

        for row in result.data:
            try:
                processed = process_raw_update(
                    raw_id=row["id"],
                    title=row["title"],
                    raw_content=row.get("raw_content", ""),
                    source_url=row.get("source_url"),
                    source_type=row.get("source_type"),
                )
                sb.table("processed_updates").insert(
                    processed.model_dump(exclude_none=True)
                ).execute()
                sb.table("raw_updates").update({"is_processed": True}).eq(
                    "id", row["id"]
                ).execute()
            except Exception as e:
                logger.error(f"Processing row {row['id']} failed: {e}")

        logger.info(f"Processed {len(result.data)} raw updates")
    except Exception as e:
        logger.error(f"Process job failed: {e}")


def start_scheduler() -> BackgroundScheduler:
    """Create, configure, and start the background scheduler.

    All scraper jobs use ``next_run_time=datetime.now(tz=timezone.utc)`` so
    they execute immediately on startup instead of waiting for the first
    interval to elapse (up to SCRAPE_INTERVAL_HOURS).

    ``misfire_grace_time=3600`` lets jobs recover gracefully when a run is
    missed (e.g. during a deployment restart or momentary downtime).
    """
    jobstores = {"default": MemoryJobStore()}
    scheduler = BackgroundScheduler(jobstores=jobstores)
    interval_hours = settings.SCRAPE_INTERVAL_HOURS
    now = datetime.now(tz=timezone.utc)

    scheduler.add_job(
        collect_github_releases,
        trigger=IntervalTrigger(hours=interval_hours),
        id="github_releases",
        name="Collect GitHub Releases",
        replace_existing=True,
        next_run_time=now,        # run immediately on startup
        misfire_grace_time=3600,  # tolerate up to 1-hour missed-run window
    )
    scheduler.add_job(
        collect_hackernews_stories,
        trigger=IntervalTrigger(hours=interval_hours),
        id="hackernews_stories",
        name="Collect Hacker News Stories",
        replace_existing=True,
        next_run_time=now,
        misfire_grace_time=3600,
    )
    scheduler.add_job(
        collect_producthunt_launches,
        trigger=IntervalTrigger(hours=interval_hours),
        id="producthunt_launches",
        name="Collect Product Hunt Launches",
        replace_existing=True,
        next_run_time=now,
        misfire_grace_time=3600,
    )
    scheduler.add_job(
        process_raw_updates,
        trigger=IntervalTrigger(hours=1),
        id="process_updates",
        name="Process Raw Updates",
        replace_existing=True,
        next_run_time=now,
        misfire_grace_time=3600,
    )

    scheduler.start()
    logger.info(
        f"Scheduler started — scraping every {interval_hours}h, "
        "processing every 1h (all jobs triggered immediately on startup)"
    )
    return scheduler
