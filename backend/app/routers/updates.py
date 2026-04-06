"""
DevPulse Backend — Updates Router
GET /updates        — latest processed updates
GET /trending-tools — tools ranked by trend score
"""
import logging
from fastapi import APIRouter, Query
from app.services.supabase_client import get_supabase

router = APIRouter(tags=["updates"])
logger = logging.getLogger("devpulse.routers.updates")

# ── Demo data (used when Supabase is not configured) ─────────

DEMO_UPDATES = [
    {
        "id": "demo-1",
        "tool_name": "React",
        "category": "Frontend Framework",
        "version": "19.1",
        "summary": "React 19 introduces Server Actions, an improved compiler, and automatic memoization — significantly reducing boilerplate and improving performance for large-scale apps.",
        "source": "github",
        "source_url": "https://github.com/facebook/react/releases",
        "trend_score": 98,
        "published_at": "2026-03-14T10:00:00Z",
    },
    {
        "id": "demo-2",
        "tool_name": "Bun",
        "category": "Runtime",
        "version": "1.2",
        "summary": "Bun 1.2 adds native S3 support, Postgres driver built into the runtime, and a dramatically faster test runner, positioning it as a serious Node.js alternative.",
        "source": "hackernews",
        "source_url": "https://bun.sh/blog/bun-v1.2",
        "trend_score": 91,
        "published_at": "2026-03-13T08:00:00Z",
    },
    {
        "id": "demo-3",
        "tool_name": "Astro",
        "category": "Frontend Framework",
        "version": "5.0",
        "summary": "Astro 5 ships Content Layer for type-safe data loading, Server Islands for hybrid rendering, and a simplified configuration API.",
        "source": "producthunt",
        "source_url": "https://astro.build/blog/astro-5/",
        "trend_score": 87,
        "published_at": "2026-03-12T14:00:00Z",
    },
    {
        "id": "demo-4",
        "tool_name": "Deno",
        "category": "Runtime",
        "version": "2.0",
        "summary": "Deno 2.0 brings full Node.js and npm compatibility, a built-in package manager, and stabilized APIs — making it a drop-in replacement for Node in many projects.",
        "source": "github",
        "source_url": "https://deno.com/blog/v2.0",
        "trend_score": 85,
        "published_at": "2026-03-11T09:30:00Z",
    },
    {
        "id": "demo-5",
        "tool_name": "Tailwind CSS",
        "category": "CSS Framework",
        "version": "4.0",
        "summary": "Tailwind CSS v4 introduces a Rust-based engine (10× faster builds), CSS-first configuration, and automatic content detection — no config file needed.",
        "source": "hackernews",
        "source_url": "https://tailwindcss.com/blog/tailwindcss-v4",
        "trend_score": 93,
        "published_at": "2026-03-10T11:00:00Z",
    },
    {
        "id": "demo-6",
        "tool_name": "SvelteKit",
        "category": "Frontend Framework",
        "version": "2.5",
        "summary": "SvelteKit 2.5 upgrades to Svelte 5 runes, adds incremental static regeneration, and delivers significantly smaller client bundles.",
        "source": "github",
        "source_url": "https://github.com/sveltejs/kit/releases",
        "trend_score": 80,
        "published_at": "2026-03-09T16:00:00Z",
    },
    {
        "id": "demo-7",
        "tool_name": "Supabase",
        "category": "Backend-as-a-Service",
        "version": "2.0",
        "summary": "Supabase launches Branching (git-like database workflows), AI vector embeddings, and queue-based background jobs — expanding beyond its Firebase-alternative roots.",
        "source": "producthunt",
        "source_url": "https://supabase.com/blog",
        "trend_score": 89,
        "published_at": "2026-03-08T12:00:00Z",
    },
    {
        "id": "demo-8",
        "tool_name": "Vite",
        "category": "Build Tool",
        "version": "6.0",
        "summary": "Vite 6 introduces the Environment API, allowing frameworks to configure separate dev/build/SSR environments, plus Rolldown-powered production builds.",
        "source": "hackernews",
        "source_url": "https://vitejs.dev/blog/announcing-vite6",
        "trend_score": 88,
        "published_at": "2026-03-07T10:30:00Z",
    },
]

DEMO_TOOLS = [
    {
        "id": "tool-1",
        "name": "React",
        "category": "Frontend Framework",
        "description": "A JavaScript library for building user interfaces with component-based architecture.",
        "website": "https://react.dev",
        "logo_url": None,
        "trend_score": 98,
    },
    {
        "id": "tool-2",
        "name": "Bun",
        "category": "Runtime",
        "description": "An all-in-one JavaScript runtime and toolkit designed for speed.",
        "website": "https://bun.sh",
        "logo_url": None,
        "trend_score": 91,
    },
    {
        "id": "tool-3",
        "name": "Tailwind CSS",
        "category": "CSS Framework",
        "description": "A utility-first CSS framework for rapid UI development.",
        "website": "https://tailwindcss.com",
        "logo_url": None,
        "trend_score": 93,
    },
    {
        "id": "tool-4",
        "name": "Supabase",
        "category": "Backend-as-a-Service",
        "description": "An open-source Firebase alternative with Postgres, auth, and realtime subscriptions.",
        "website": "https://supabase.com",
        "logo_url": None,
        "trend_score": 89,
    },
    {
        "id": "tool-5",
        "name": "Vite",
        "category": "Build Tool",
        "description": "Next-generation frontend tooling with lightning-fast HMR and optimized builds.",
        "website": "https://vitejs.dev",
        "logo_url": None,
        "trend_score": 88,
    },
    {
        "id": "tool-6",
        "name": "Astro",
        "category": "Frontend Framework",
        "description": "The web framework for content-driven websites — ships zero JS by default.",
        "website": "https://astro.build",
        "logo_url": None,
        "trend_score": 87,
    },
    {
        "id": "tool-7",
        "name": "Deno",
        "category": "Runtime",
        "description": "A modern runtime for JavaScript and TypeScript with built-in security.",
        "website": "https://deno.com",
        "logo_url": None,
        "trend_score": 85,
    },
    {
        "id": "tool-8",
        "name": "SvelteKit",
        "category": "Frontend Framework",
        "description": "The fastest way to build Svelte apps with server-side rendering and routing.",
        "website": "https://kit.svelte.dev",
        "logo_url": None,
        "trend_score": 80,
    },
]


@router.get("/updates")
async def get_updates(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: str | None = None,
):
    """Return latest processed updates, optionally filtered by category."""
    sb = get_supabase()
    try:
        query = sb.table("processed_updates").select("*").order(
            "published_at", desc=True
        )
        if category:
            query = query.eq("category", category)
        result = query.range(offset, offset + limit - 1).execute()
        return {"updates": result.data, "count": len(result.data)}
    except Exception as e:
        logger.warning(f"get_updates falling back to demo data: {e}")
        data = DEMO_UPDATES
        if category:
            data = [u for u in data if u.get("category", "").lower() == category.lower()]
        return {"updates": data[offset : offset + limit], "count": len(data)}


@router.get("/trending-tools")
async def get_trending_tools(limit: int = Query(10, ge=1, le=50)):
    """Return tools ranked by trend score (descending)."""
    sb = get_supabase()
    try:
        result = (
            sb.table("processed_updates")
            .select("tool_name, category, source_url, trend_score, summary, version")
            .order("trend_score", desc=True)
            .limit(limit)
            .execute()
        )
        return {"tools": result.data}
    except Exception as e:
        logger.warning(f"get_trending_tools falling back to demo data: {e}")
        sorted_tools = sorted(DEMO_TOOLS, key=lambda t: t["trend_score"], reverse=True)
        return {"tools": sorted_tools[:limit]}
