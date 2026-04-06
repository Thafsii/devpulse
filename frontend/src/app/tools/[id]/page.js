'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { getTool } from '@/lib/api';

const DEMO_TOOLS = {
    'tool-1': { id: 'tool-1', name: 'React', category: 'Frontend Framework', description: 'A declarative, component-based JavaScript library for building user interfaces. Maintained by Meta and a massive community, React powers everything from SPAs to complex dashboards.', website: 'https://react.dev', updates: [{ version: '19.1', summary: 'Server Actions, improved compiler, automatic memoization.', published_at: '2026-03-14T10:00:00Z' }, { version: '19.0', summary: 'New React Compiler, use() hook, Actions API.', published_at: '2026-02-01T10:00:00Z' }] },
    'tool-2': { id: 'tool-2', name: 'Bun', category: 'Runtime', description: 'An all-in-one JavaScript runtime, bundler, transpiler, and package manager designed for speed. Built with Zig.', website: 'https://bun.sh', updates: [{ version: '1.2', summary: 'Native S3, built-in Postgres, faster test runner.', published_at: '2026-03-13T08:00:00Z' }] },
    'tool-3': { id: 'tool-3', name: 'Tailwind CSS', category: 'CSS Framework', description: 'A utility-first CSS framework for rapid UI development. Highly customizable.', website: 'https://tailwindcss.com', updates: [{ version: '4.0', summary: 'Rust engine, CSS-first config, auto content detection.', published_at: '2026-03-10T11:00:00Z' }] },
    'tool-4': { id: 'tool-4', name: 'Supabase', category: 'Backend-as-a-Service', description: 'Open-source Firebase alternative with Postgres, auth, realtime, and edge functions.', website: 'https://supabase.com', updates: [{ version: '2.0', summary: 'Branching, AI embeddings, background jobs.', published_at: '2026-03-08T12:00:00Z' }] },
    'tool-5': { id: 'tool-5', name: 'Vite', category: 'Build Tool', description: 'Next-gen frontend build tool with instant HMR and optimized Rollup builds.', website: 'https://vitejs.dev', updates: [{ version: '6.0', summary: 'Environment API, Rolldown-powered builds.', published_at: '2026-03-07T10:30:00Z' }] },
    'tool-6': { id: 'tool-6', name: 'Astro', category: 'Frontend Framework', description: 'The web framework for content-driven sites — ships zero JS by default.', website: 'https://astro.build', updates: [{ version: '5.0', summary: 'Content Layer, Server Islands, simplified config.', published_at: '2026-03-12T14:00:00Z' }] },
    'tool-7': { id: 'tool-7', name: 'Deno', category: 'Runtime', description: 'A modern runtime for JS and TS with built-in security and native TypeScript.', website: 'https://deno.com', updates: [{ version: '2.0', summary: 'Full Node.js/npm compat, built-in package manager.', published_at: '2026-03-11T09:30:00Z' }] },
    'tool-8': { id: 'tool-8', name: 'SvelteKit', category: 'Frontend Framework', description: 'The official Svelte app framework with file-based routing and SSR.', website: 'https://kit.svelte.dev', updates: [{ version: '2.5', summary: 'Svelte 5 runes, ISR, smaller bundles.', published_at: '2026-03-09T16:00:00Z' }] },
};

export default function ToolDetailPage() {
    const params = useParams();
    const [tool, setTool] = useState(null);
    const [bookmarked, setBookmarked] = useState(false);

    useEffect(() => {
        if (!params?.id) return;
        getTool(params.id)
            .then(data => setTool(data))
            .catch(() => setTool(DEMO_TOOLS[params.id] || null));
    }, [params?.id]);

    if (!tool) {
        return (
            <div className="page">
                <div className="container">
                    <div className="card animate-fade-in" style={{ padding: '3rem', textAlign: 'center' }}>
                        <p style={{ color: 'var(--text-tertiary)', fontSize: '1.1rem' }}>Loading tool…</p>
                    </div>
                </div>
            </div>
        );
    }

    const initial = tool.name[0].toUpperCase();

    return (
        <div className="page">
            <div className="container" style={{ maxWidth: 860 }}>
                {/* Header */}
                <div className="tool-header animate-fade-in">
                    <div className="tool-icon">{initial}</div>
                    <div className="tool-info" style={{ flex: 1 }}>
                        <div className="flex justify-between items-center">
                            <h1>{tool.name}</h1>
                            <button
                                className={`bookmark-btn ${bookmarked ? 'active' : ''}`}
                                onClick={() => setBookmarked(!bookmarked)}
                                title={bookmarked ? 'Remove bookmark' : 'Bookmark this tool'}
                            >
                                {bookmarked ? '★' : '☆'}
                            </button>
                        </div>
                        <div className="flex gap-sm mt-sm">
                            <span className="badge badge-category">{tool.category}</span>
                        </div>
                        <p>{tool.description}</p>
                        {tool.website && (
                            <a
                                href={tool.website}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="btn btn-secondary btn-sm"
                                style={{ marginTop: '1rem', display: 'inline-flex' }}
                            >
                                Visit Website ↗
                            </a>
                        )}
                    </div>
                </div>

                {/* Update History */}
                <section className="mt-2xl animate-slide-up">
                    <h2 className="section-title mb-lg">📦 Release History</h2>
                    {tool.updates && tool.updates.length > 0 ? (
                        <div className="flex flex-col gap-md">
                            {tool.updates.map((update, i) => (
                                <div key={i} className="card">
                                    <div className="flex justify-between items-center">
                                        <span className="badge badge-version">v{update.version}</span>
                                        <span className="card-meta">
                                            {new Date(update.published_at).toLocaleDateString('en-US', {
                                                year: 'numeric', month: 'short', day: 'numeric',
                                            })}
                                        </span>
                                    </div>
                                    <p className="card-body mt-sm">{update.summary}</p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <div className="card" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-tertiary)' }}>
                            No releases recorded yet.
                        </div>
                    )}
                </section>

                {/* Back */}
                <div className="mt-xl animate-fade-in">
                    <Link href="/explore" className="btn btn-ghost">← Back to Explore</Link>
                </div>
            </div>
        </div>
    );
}
