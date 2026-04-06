"""
DevPulse Backend — User Feed Router
GET  /user-feed         — personalized feed based on user preferences
GET  /user-preferences  — retrieve topic preferences
POST /user-preferences  — replace topic preferences (JSON body: ["topic1", "topic2"])
"""
import logging
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from app.services.auth import get_current_user
from app.services.supabase_client import get_supabase

router = APIRouter(tags=["feed"])
logger = logging.getLogger("devpulse.routers.feed")


@router.get("/user-feed")
async def get_user_feed(
    user: dict = Depends(get_current_user),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """
    Return updates filtered by the user's preferred topics.
    Falls back to all updates if no preferences are set.
    """
    sb = get_supabase()
    try:
        # Get user's preferred topics
        prefs = (
            sb.table("user_preferences")
            .select("topic")
            .eq("user_id", user["id"])
            .execute()
        )
        topics = [p["topic"] for p in prefs.data] if prefs.data else []

        query = sb.table("processed_updates").select("*").order(
            "published_at", desc=True
        )

        if topics:
            query = query.in_("category", topics)

        result = query.range(offset, offset + limit - 1).execute()
        return {"updates": result.data, "topics": topics, "count": len(result.data)}
    except Exception as e:
        logger.error(f"get_user_feed failed for user {user['id']}: {e}")
        return {"updates": [], "topics": [], "count": 0}


@router.get("/user-preferences")
async def get_preferences(user: dict = Depends(get_current_user)):
    """Return the user's topic preferences."""
    sb = get_supabase()
    try:
        result = (
            sb.table("user_preferences")
            .select("*")
            .eq("user_id", user["id"])
            .execute()
        )
        return {"preferences": result.data}
    except Exception as e:
        logger.error(f"get_preferences failed for user {user['id']}: {e}")
        return {"preferences": []}


@router.post("/user-preferences")
async def set_preferences(
    topics: list[str] = Body(..., example=["Frontend Framework", "AI/ML"]),
    user: dict = Depends(get_current_user),
):
    """Replace the user's topic preferences.

    Accepts a JSON array in the request body, e.g.:
        ["Frontend Framework", "AI/ML", "DevOps"]

    Note: ``Body(...)`` is required here — without it FastAPI would interpret
    the list as repeated query parameters instead of a JSON body.
    """
    sb = get_supabase()
    try:
        # Delete existing preferences for this user
        sb.table("user_preferences").delete().eq("user_id", user["id"]).execute()
        # Insert new preferences (skip empty strings)
        rows = [{"user_id": user["id"], "topic": t} for t in topics if t.strip()]
        if rows:
            sb.table("user_preferences").insert(rows).execute()
        return {"preferences": topics}
    except Exception as e:
        logger.error(f"set_preferences failed for user {user['id']}: {e}")
        raise HTTPException(status_code=400, detail=f"Could not save preferences: {e}")
