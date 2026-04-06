"""
DevPulse Backend — Pydantic Models
"""
from __future__ import annotations
import hashlib
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, computed_field


# ── Enums ────────────────────────────────────────────────────

class SourceType(str, Enum):
    GITHUB = "github"
    HACKERNEWS = "hackernews"
    PRODUCTHUNT = "producthunt"


# ── Raw Updates ──────────────────────────────────────────────

class RawUpdateBase(BaseModel):
    source_type: SourceType
    title: str
    raw_content: Optional[str] = None
    source_url: Optional[str] = None


class RawUpdateCreate(RawUpdateBase):
    """Used by scrapers when inserting new raw updates."""

    @computed_field  # type: ignore[misc]
    @property
    def content_hash(self) -> str:
        payload = f"{self.source_type.value}|{self.title}|{self.source_url or ''}"
        return hashlib.sha256(payload.encode()).hexdigest()


class RawUpdate(RawUpdateBase):
    id: str
    content_hash: str
    is_processed: bool = False
    collected_at: datetime

    class Config:
        from_attributes = True


# ── Processed Updates ────────────────────────────────────────

class ProcessedUpdateBase(BaseModel):
    tool_name: str
    category: Optional[str] = None
    version: Optional[str] = None
    summary: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    trend_score: float = 0


class ProcessedUpdateCreate(ProcessedUpdateBase):
    raw_update_id: str
    tool_id: Optional[str] = None


class ProcessedUpdate(ProcessedUpdateBase):
    id: str
    raw_update_id: Optional[str] = None
    tool_id: Optional[str] = None
    published_at: datetime

    class Config:
        from_attributes = True


# ── Tools ────────────────────────────────────────────────────

class ToolBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None


class ToolCreate(ToolBase):
    pass


class Tool(ToolBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


# ── User ─────────────────────────────────────────────────────

class UserProfile(BaseModel):
    id: str
    email: str
    display_name: Optional[str] = None
    avatar_url: Optional[str] = None
    favorite_topics: list[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


# ── User Preferences ────────────────────────────────────────

class UserPreference(BaseModel):
    id: str
    user_id: str
    topic: str


class UserPreferenceCreate(BaseModel):
    topic: str


# ── Bookmarks ────────────────────────────────────────────────

class Bookmark(BaseModel):
    id: str
    user_id: str
    update_id: Optional[str] = None
    tool_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class BookmarkCreate(BaseModel):
    update_id: Optional[str] = None
    tool_id: Optional[str] = None
