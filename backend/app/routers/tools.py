"""
DevPulse Backend — Tools Router
GET /tools/{id}   — tool details
GET /tools        — list tools by category
"""
from fastapi import APIRouter, HTTPException, Query
from app.services.supabase_client import get_supabase

router = APIRouter(tags=["tools"])

DEMO_TOOLS = {
    "tool-1": {
        "id": "tool-1",
        "name": "React",
        "category": "Frontend Framework",
        "description": "A declarative, component-based JavaScript library for building user interfaces. Maintained by Meta and a massive community, React powers everything from SPAs to complex dashboards.",
        "website": "https://react.dev",
        "logo_url": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updates": [
            {"version": "19.1", "summary": "Server Actions, improved compiler, automatic memoization.", "published_at": "2026-03-14T10:00:00Z"},
            {"version": "19.0", "summary": "New React Compiler, use() hook, Actions API.", "published_at": "2026-02-01T10:00:00Z"},
        ],
    },
    "tool-2": {
        "id": "tool-2",
        "name": "Bun",
        "category": "Runtime",
        "description": "An all-in-one JavaScript runtime, bundler, transpiler, and package manager designed for speed. Built with Zig, it aims to replace Node.js, webpack, and more.",
        "website": "https://bun.sh",
        "logo_url": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updates": [
            {"version": "1.2", "summary": "Native S3, built-in Postgres, faster test runner.", "published_at": "2026-03-13T08:00:00Z"},
        ],
    },
    "tool-3": {
        "id": "tool-3",
        "name": "Tailwind CSS",
        "category": "CSS Framework",
        "description": "A utility-first CSS framework that lets you build modern designs directly in your markup. Highly customizable, no opinionated components.",
        "website": "https://tailwindcss.com",
        "logo_url": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updates": [
            {"version": "4.0", "summary": "Rust-based engine (10× faster), CSS-first config, auto content detection.", "published_at": "2026-03-10T11:00:00Z"},
        ],
    },
    "tool-4": {
        "id": "tool-4",
        "name": "Supabase",
        "category": "Backend-as-a-Service",
        "description": "Open-source Firebase alternative offering a Postgres database, authentication, instant APIs, edge functions, realtime subscriptions, and storage.",
        "website": "https://supabase.com",
        "logo_url": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updates": [
            {"version": "2.0", "summary": "Branching, AI vector embeddings, queue-based background jobs.", "published_at": "2026-03-08T12:00:00Z"},
        ],
    },
    "tool-5": {
        "id": "tool-5",
        "name": "Vite",
        "category": "Build Tool",
        "description": "A next-generation frontend build tool offering instant server start, lightning-fast HMR, and optimized Rollup-based production builds.",
        "website": "https://vitejs.dev",
        "logo_url": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updates": [
            {"version": "6.0", "summary": "Environment API, Rolldown-powered builds.", "published_at": "2026-03-07T10:30:00Z"},
        ],
    },
    "tool-6": {
        "id": "tool-6",
        "name": "Astro",
        "category": "Frontend Framework",
        "description": "The web framework for content-driven websites. Ships zero JavaScript by default, supports any UI framework, and delivers blazing-fast performance.",
        "website": "https://astro.build",
        "logo_url": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updates": [
            {"version": "5.0", "summary": "Content Layer, Server Islands, simplified config.", "published_at": "2026-03-12T14:00:00Z"},
        ],
    },
    "tool-7": {
        "id": "tool-7",
        "name": "Deno",
        "category": "Runtime",
        "description": "A modern, secure runtime for JavaScript and TypeScript with built-in tooling, native TypeScript support, and web-standard APIs.",
        "website": "https://deno.com",
        "logo_url": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updates": [
            {"version": "2.0", "summary": "Full Node.js/npm compatibility, built-in package manager.", "published_at": "2026-03-11T09:30:00Z"},
        ],
    },
    "tool-8": {
        "id": "tool-8",
        "name": "SvelteKit",
        "category": "Frontend Framework",
        "description": "The official application framework for Svelte with file-based routing, SSR, and a great developer experience.",
        "website": "https://kit.svelte.dev",
        "logo_url": None,
        "created_at": "2026-01-01T00:00:00Z",
        "updates": [
            {"version": "2.5", "summary": "Svelte 5 runes, ISR, smaller bundles.", "published_at": "2026-03-09T16:00:00Z"},
        ],
    },
}


@router.get("/tools")
async def list_tools(category: str | None = None, limit: int = Query(20, ge=1, le=100)):
    """List tools, optionally filtered by category."""
    sb = get_supabase()
    try:
        query = sb.table("tools").select("*")
        if category:
            query = query.eq("category", category)
        result = query.limit(limit).execute()
        return {"tools": result.data}
    except Exception:
        tools = list(DEMO_TOOLS.values())
        if category:
            tools = [t for t in tools if t["category"].lower() == category.lower()]
        return {"tools": tools[:limit]}


@router.get("/tools/{tool_id}")
async def get_tool(tool_id: str):
    """Get detailed info about a specific tool."""
    sb = get_supabase()
    try:
        result = sb.table("tools").select("*").eq("id", tool_id).single().execute()
        updates = (
            sb.table("processed_updates")
            .select("*")
            .eq("tool_id", tool_id)
            .order("published_at", desc=True)
            .limit(10)
            .execute()
        )
        return {**result.data, "updates": updates.data}
    except Exception:
        tool = DEMO_TOOLS.get(tool_id)
        if not tool:
            raise HTTPException(status_code=404, detail="Tool not found")
        return tool
