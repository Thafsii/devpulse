'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import UpdateCard from '@/components/UpdateCard';
import ToolCard from '@/components/ToolCard';
import { getUpdates, getTrendingTools } from '@/lib/api';

/* ── Static demo data (used until backend is live) ────── */
const DEMO_UPDATES = [
  { id: 'demo-1', tool_name: 'React', category: 'Frontend Framework', version: '19.1', summary: 'React 19 introduces Server Actions, an improved compiler, and automatic memoization — significantly reducing boilerplate and improving performance for large-scale apps.', source: 'github', source_url: 'https://github.com/facebook/react/releases', trend_score: 98, published_at: '2026-03-14T10:00:00Z' },
  { id: 'demo-2', tool_name: 'Bun', category: 'Runtime', version: '1.2', summary: 'Bun 1.2 adds native S3 support, a built-in Postgres driver, and a dramatically faster test runner, positioning it as a serious Node.js alternative.', source: 'hackernews', source_url: 'https://bun.sh/blog/bun-v1.2', trend_score: 91, published_at: '2026-03-13T08:00:00Z' },
  { id: 'demo-3', tool_name: 'Astro', category: 'Frontend Framework', version: '5.0', summary: 'Astro 5 ships Content Layer for type-safe data loading, Server Islands for hybrid rendering, and a simplified configuration API.', source: 'producthunt', source_url: 'https://astro.build/blog/astro-5/', trend_score: 87, published_at: '2026-03-12T14:00:00Z' },
  { id: 'demo-4', tool_name: 'Deno', category: 'Runtime', version: '2.0', summary: 'Deno 2.0 brings full Node.js and npm compatibility, a built-in package manager, and stabilized APIs — a drop-in replacement for Node.', source: 'github', source_url: 'https://deno.com/blog/v2.0', trend_score: 85, published_at: '2026-03-11T09:30:00Z' },
  { id: 'demo-5', tool_name: 'Tailwind CSS', category: 'CSS Framework', version: '4.0', summary: 'Tailwind CSS v4 introduces a Rust-based engine (10× faster builds), CSS-first configuration, and automatic content detection.', source: 'hackernews', source_url: 'https://tailwindcss.com/blog/tailwindcss-v4', trend_score: 93, published_at: '2026-03-10T11:00:00Z' },
  { id: 'demo-6', tool_name: 'Vite', category: 'Build Tool', version: '6.0', summary: 'Vite 6 introduces the Environment API for separate dev/build/SSR configuration, plus Rolldown-powered production builds.', source: 'hackernews', source_url: 'https://vitejs.dev/blog/announcing-vite6', trend_score: 88, published_at: '2026-03-07T10:30:00Z' },
];

const DEMO_TOOLS = [
  { id: 'tool-1', name: 'React', category: 'Frontend Framework', description: 'A JavaScript library for building user interfaces with component-based architecture.', website: 'https://react.dev', trend_score: 98 },
  { id: 'tool-3', name: 'Tailwind CSS', category: 'CSS Framework', description: 'A utility-first CSS framework for rapid UI development.', website: 'https://tailwindcss.com', trend_score: 93 },
  { id: 'tool-2', name: 'Bun', category: 'Runtime', description: 'An all-in-one JavaScript runtime and toolkit designed for speed.', website: 'https://bun.sh', trend_score: 91 },
  { id: 'tool-4', name: 'Supabase', category: 'Backend-as-a-Service', description: 'Open-source Firebase alternative with Postgres, auth, and realtime.', website: 'https://supabase.com', trend_score: 89 },
  { id: 'tool-5', name: 'Vite', category: 'Build Tool', description: 'Next-generation frontend tooling with lightning-fast HMR.', website: 'https://vitejs.dev', trend_score: 88 },
  { id: 'tool-6', name: 'Astro', category: 'Frontend Framework', description: 'The web framework for content-driven websites — ships zero JS by default.', website: 'https://astro.build', trend_score: 87 },
];

export default function HomePage() {
  const [updates, setUpdates] = useState(DEMO_UPDATES);
  const [tools, setTools] = useState(DEMO_TOOLS);

  useEffect(() => {
    getUpdates(6).then(data => { if (data?.updates?.length) setUpdates(data.updates); }).catch(() => { });
    getTrendingTools(6).then(data => { if (data?.tools?.length) setTools(data.tools); }).catch(() => { });
  }, []);

  return (
    <div className="page">
      {/* ── Hero ──────────────────────────────────────── */}
      <section className="container hero animate-fade-in">
        <div className="hero-glow" />
        <h1 className="hero-title">
          Stay Ahead of the<br />
          <span className="gradient-text">Developer Curve</span>
        </h1>
        <p className="hero-description">
          DevPulse aggregates the latest tools, frameworks, and releases from GitHub, Hacker News, and Product Hunt — so you never miss what matters.
        </p>
        <div className="hero-actions">
          <Link href="/explore" className="btn btn-primary">
            Explore Tools →
          </Link>
          <Link href="/dashboard" className="btn btn-secondary">
            My Dashboard
          </Link>
        </div>
      </section>

      {/* ── Trending Tools ────────────────────────────── */}
      <section className="container mt-2xl">
        <div className="section-header">
          <h2 className="section-title">
            🔥 <span className="gradient-text">Trending Tools</span>
          </h2>
          <p className="section-subtitle">What developers are talking about right now</p>
        </div>
        <div className="grid-3">
          {tools.map((tool, i) => (
            <ToolCard key={tool.id} tool={tool} index={i} />
          ))}
        </div>
      </section>

      {/* ── Recent Updates ────────────────────────────── */}
      <section className="container mt-2xl">
        <div className="section-header flex justify-between items-center">
          <div>
            <h2 className="section-title">📡 Latest Updates</h2>
            <p className="section-subtitle">Fresh releases and announcements</p>
          </div>
          <Link href="/explore" className="btn btn-secondary btn-sm">
            View All →
          </Link>
        </div>
        <div className="grid-2">
          {updates.map((update, i) => (
            <UpdateCard key={update.id} update={update} index={i} />
          ))}
        </div>
      </section>

      {/* ── CTA ───────────────────────────────────────── */}
      <section className="container mt-2xl text-center animate-fade-in">
        <div className="card" style={{ maxWidth: 640, margin: '0 auto', textAlign: 'center' }}>
          <h3 style={{ fontSize: '1.3rem', fontWeight: 700, marginBottom: '0.5rem' }}>
            Personalize your feed
          </h3>
          <p style={{ color: 'var(--text-secondary)', marginBottom: '1rem' }}>
            Sign in to select your favorite topics and get curated updates delivered to your dashboard.
          </p>
          <Link href="/login" className="btn btn-primary">
            Get Started — Free
          </Link>
        </div>
      </section>
    </div>
  );
}
