-- ============================================================
-- DevPulse — Supabase Database Schema
-- ============================================================

-- 1. Source type enum
CREATE TYPE source_type AS ENUM ('github', 'hackernews', 'producthunt');

-- 2. Users (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    display_name TEXT,
    avatar_url TEXT,
    favorite_topics TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- 3. Tools
CREATE TABLE IF NOT EXISTS public.tools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    website TEXT,
    logo_url TEXT,
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_tools_category ON public.tools(category);
CREATE INDEX idx_tools_name ON public.tools(name);

-- 4. Raw updates (collected by scrapers)
CREATE TABLE IF NOT EXISTS public.raw_updates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type source_type NOT NULL,
    title TEXT NOT NULL,
    raw_content TEXT,
    source_url TEXT,
    content_hash TEXT NOT NULL,
    is_processed BOOLEAN DEFAULT false,
    collected_at TIMESTAMPTZ DEFAULT now(),

    CONSTRAINT uq_raw_updates_content_hash UNIQUE (content_hash)
);

CREATE INDEX idx_raw_updates_source ON public.raw_updates(source_type);
CREATE INDEX idx_raw_updates_processed ON public.raw_updates(is_processed);

-- 5. Processed updates (AI-extracted structured data)
CREATE TABLE IF NOT EXISTS public.processed_updates (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_update_id UUID REFERENCES public.raw_updates(id) ON DELETE CASCADE,
    tool_id UUID REFERENCES public.tools(id) ON DELETE SET NULL,
    tool_name TEXT NOT NULL,
    category TEXT,
    version TEXT,
    summary TEXT,
    source TEXT,
    source_url TEXT,
    trend_score REAL DEFAULT 0,
    published_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_processed_updates_tool ON public.processed_updates(tool_id);
CREATE INDEX idx_processed_updates_category ON public.processed_updates(category);
CREATE INDEX idx_processed_updates_published ON public.processed_updates(published_at DESC);
CREATE INDEX idx_processed_updates_trend ON public.processed_updates(trend_score DESC);

-- 6. User preferences
CREATE TABLE IF NOT EXISTS public.user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    topic TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now(),

    CONSTRAINT uq_user_pref UNIQUE (user_id, topic)
);

-- 7. Bookmarks
-- A bookmark links a user to either an update OR a tool (not both at once).
-- Separate partial unique indexes prevent duplicate bookmarks for each type.
CREATE TABLE IF NOT EXISTS public.bookmarks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    -- ON DELETE CASCADE: removing an update/tool removes related bookmarks cleanly
    update_id UUID REFERENCES public.processed_updates(id) ON DELETE CASCADE,
    tool_id   UUID REFERENCES public.tools(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),

    -- Enforce: a user can only bookmark the same update once
    CONSTRAINT uq_bookmark_update UNIQUE (user_id, update_id),
    -- Enforce: a user can only bookmark the same tool once
    CONSTRAINT uq_bookmark_tool   UNIQUE (user_id, tool_id)
);

CREATE INDEX idx_bookmarks_user      ON public.bookmarks(user_id);
CREATE INDEX idx_bookmarks_update_id ON public.bookmarks(update_id) WHERE update_id IS NOT NULL;
CREATE INDEX idx_bookmarks_tool_id   ON public.bookmarks(tool_id)   WHERE tool_id   IS NOT NULL;

-- ============================================================
-- Row Level Security
-- ============================================================

ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.tools ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.raw_updates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.processed_updates ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.bookmarks ENABLE ROW LEVEL SECURITY;

-- ============================================================
-- Auto-create user profile on Supabase Auth signup
-- ============================================================
-- This trigger fires whenever a new row is inserted into auth.users
-- (i.e. every time someone signs up). It creates a matching row in
-- public.users so the backend can reference it via foreign keys.
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER          -- runs as the function owner, not the caller
SET search_path = public  -- prevent search_path hijacking
AS $$
BEGIN
    INSERT INTO public.users (id, email, display_name, avatar_url)
    VALUES (
        NEW.id,
        NEW.email,
        -- pull display_name from raw_user_meta_data if the client sent it
        NEW.raw_user_meta_data->>'display_name',
        NEW.raw_user_meta_data->>'avatar_url'
    )
    ON CONFLICT (id) DO NOTHING;  -- idempotent: safe to call multiple times
    RETURN NEW;
END;
$$;

-- Attach the trigger to auth.users (insert only; updates handled separately)
CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_new_user();

-- ============================================================
-- Row Level Security Policies
-- ============================================================

-- Users can read their own profile
CREATE POLICY "Users read own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

-- Users can insert their own profile (needed for manual upserts / magic-link flows)
CREATE POLICY "Users insert own profile" ON public.users
    FOR INSERT WITH CHECK (auth.uid() = id);

CREATE POLICY "Users update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

-- Tools and updates are publicly readable
CREATE POLICY "Tools are public" ON public.tools
    FOR SELECT USING (true);

CREATE POLICY "Raw updates are public" ON public.raw_updates
    FOR SELECT USING (true);

CREATE POLICY "Processed updates are public" ON public.processed_updates
    FOR SELECT USING (true);

-- User preferences: users manage their own
CREATE POLICY "Users manage own preferences" ON public.user_preferences
    FOR ALL USING (auth.uid() = user_id);

-- Bookmarks: users manage their own
CREATE POLICY "Users manage own bookmarks" ON public.bookmarks
    FOR ALL USING (auth.uid() = user_id);

-- Service role bypass for scrapers (inserts from backend)
CREATE POLICY "Service role full access raw_updates" ON public.raw_updates
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access processed_updates" ON public.processed_updates
    FOR ALL USING (auth.role() = 'service_role');

CREATE POLICY "Service role full access tools" ON public.tools
    FOR ALL USING (auth.role() = 'service_role');
