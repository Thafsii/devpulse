"""
DevPulse Backend — Bookmarks Router
POST /bookmark   — save a bookmark
DELETE /bookmark — remove a bookmark
GET  /bookmarks  — list user bookmarks
"""
from fastapi import APIRouter, Depends, HTTPException
from app.models import BookmarkCreate, Bookmark
from app.services.auth import get_current_user
from app.services.supabase_client import get_supabase

router = APIRouter(tags=["bookmarks"])


@router.post("/bookmark")
async def create_bookmark(body: BookmarkCreate, user: dict = Depends(get_current_user)):
    """Save a tool or update as a bookmark."""
    sb = get_supabase()
    try:
        data = {"user_id": user["id"]}
        if body.update_id:
            data["update_id"] = body.update_id
        if body.tool_id:
            data["tool_id"] = body.tool_id
        result = sb.table("bookmarks").insert(data).execute()
        return {"bookmark": result.data[0] if result.data else data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/bookmark/{bookmark_id}")
async def delete_bookmark(bookmark_id: str, user: dict = Depends(get_current_user)):
    """Remove a bookmark."""
    sb = get_supabase()
    try:
        sb.table("bookmarks").delete().eq("id", bookmark_id).eq(
            "user_id", user["id"]
        ).execute()
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/bookmarks")
async def list_bookmarks(user: dict = Depends(get_current_user)):
    """List all bookmarks for the authenticated user."""
    sb = get_supabase()
    try:
        result = (
            sb.table("bookmarks")
            .select("*, processed_updates(*), tools(*)")
            .eq("user_id", user["id"])
            .order("created_at", desc=True)
            .execute()
        )
        return {"bookmarks": result.data}
    except Exception:
        return {"bookmarks": []}
