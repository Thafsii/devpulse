# DevPulse — Setup & Deployment Guide

## Prerequisites

| Tool | Version |
|---|---|
| Python | 3.12+ |
| Node.js | 20+ |
| npm | 10+ |
| Supabase account | free tier OK |

---

## 1. Clone & Configure

```bash
git clone <your-repo-url>
cd Devpulse
```

---

## 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` with your real keys:

| Key | Where to get it |
|---|---|
| `SUPABASE_URL` | Supabase Dashboard → Settings → API |
| `SUPABASE_ANON_KEY` | Same page, "anon public" key |
| `SUPABASE_SERVICE_ROLE_KEY` | Same page, "service_role" key — **keep secret** |
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| `GITHUB_PAT` | https://github.com/settings/tokens (no scopes needed for public repos) |
| `PRODUCTHUNT_TOKEN` | https://www.producthunt.com/v2/oauth/applications |
| `CORS_ORIGINS` | `http://localhost:3000,https://your-site.netlify.app` |

### Run locally

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

Test endpoints:

```bash
curl http://localhost:8000/health        # {"status":"ok"}
curl http://localhost:8000/updates       # demo data
curl http://localhost:8000/tools         # demo data
curl http://localhost:8000/trending-tools
```

### Test scrapers manually

```bash
cd backend
python -c "from app.scrapers.hackernews_scraper import fetch_stories; r=fetch_stories(2); print(len(r), r[0].title if r else 'empty')"
python -c "from app.scrapers.github_scraper import fetch_releases; r=fetch_releases(); print(f'{len(r)} releases fetched')"
```

---

## 3. Database Setup

1. Open **Supabase Dashboard → SQL Editor**
2. Run `supabase/schema.sql` — creates all tables, RLS policies, and the user-profile trigger
3. Run `supabase/seed.sql` — inserts 12 tools and 12 processed updates for testing

> **Tip:** If you have the Supabase CLI installed:
> ```bash
> supabase db reset   # runs schema.sql + seed.sql automatically
> ```

---

## 4. Frontend Setup

```bash
cd frontend
npm install
cp .env.example .env.local
```

Edit `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
```

### Run locally

```bash
cd frontend
npm run dev
# Open http://localhost:3000
```

---

## 5. End-to-End Verification

1. Open `http://localhost:3000` — home page shows trending tools and updates (seed data)
2. Click **Explore** — category filter chips work
3. Click **Sign In** → create an account → verify redirect to `/dashboard`
4. Toggle topics on dashboard — check Supabase `user_preferences` table has rows
5. Bookmark an update — check Supabase `bookmarks` table
6. Visit `/profile` — preferences and bookmarks appear

---

## 6. Deployment

### Backend → Railway

1. Push `backend/` to GitHub
2. Create a new Railway project → **Deploy from GitHub**
3. Set all environment variables from `.env.example` in Railway → Variables
4. Railway auto-detects the `Dockerfile` and deploys
5. Copy the Railway URL (e.g. `https://devpulse-api.up.railway.app`)

### Frontend → Netlify

1. Push `frontend/` to GitHub
2. Create a new Netlify site → **Import from GitHub**
3. Build command: `npm run build` | Publish: `.next`
4. Install the Netlify Next.js plugin (auto-detected from `netlify.toml`)
5. Set environment variables in Netlify → Site → Environment:
   - `NEXT_PUBLIC_API_URL` = your Railway URL
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
6. Update `CORS_ORIGINS` in Railway to include your Netlify domain

---

## 7. Architecture Overview

```
┌─ Frontend (Netlify) ─────────────────────────────────────────┐
│  Next.js 16 · src/app/ pages · src/lib/api.js + supabase.js │
└──────────────────────┬───────────────────────────────────────┘
                       │ REST  (NEXT_PUBLIC_API_URL)
┌─ Backend (Railway) ──▼───────────────────────────────────────┐
│  FastAPI · APScheduler (runs scrapers on startup + interval) │
│  Scrapers: GitHub · HackerNews · Product Hunt                │
│  AI Processor: rule-based → GPT-4o-mini fallback            │
└──────────────────────┬───────────────────────────────────────┘
                       │ supabase-py (service role)
┌─ Database (Supabase) ▼───────────────────────────────────────┐
│  PostgreSQL · RLS · auth.users trigger · raw_updates         │
│                                processed_updates · bookmarks  │
└──────────────────────────────────────────────────────────────┘
```
