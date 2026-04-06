"""
DevPulse Backend — FastAPI Application
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)-30s %(levelname)-8s %(message)s",
)
logger = logging.getLogger("devpulse")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Start the background scheduler on startup; shut it down on teardown."""
    logger.info("DevPulse API starting up…")
    scheduler = None
    try:
        from app.scheduler.jobs import start_scheduler
        scheduler = start_scheduler()
        logger.info("Background scheduler started")
    except Exception as e:
        logger.warning(f"Scheduler not started (likely missing config): {e}")
    yield
    if scheduler:
        scheduler.shutdown(wait=False)
        logger.info("Background scheduler shut down")


app = FastAPI(
    title="DevPulse API",
    description="Developer updates aggregation platform — API backend",
    version="1.0.0",
    lifespan=lifespan,
)

# ── CORS ─────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ──────────────────────────────────────────────────
from app.routers import updates, tools, bookmarks, feed  # noqa: E402

app.include_router(updates.router)
app.include_router(tools.router)
app.include_router(bookmarks.router)
app.include_router(feed.router)


# ── Health check ─────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok", "service": "devpulse-api"}
