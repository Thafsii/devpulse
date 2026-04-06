'use client';

import { useState, useEffect } from 'react';
import UpdateCard from '@/components/UpdateCard';
import ToolCard from '@/components/ToolCard';
import { getUpdates, getTools } from '@/lib/api';

const CATEGORIES = [
    'All',
    'Frontend Framework',
    'Backend Framework',
    'Runtime',
    'Build Tool',
    'CSS Framework',
    'AI/ML',
    'DevOps',
    'Database',
    'Backend-as-a-Service',
    'Language',
    'Mobile',
];

const DEMO_UPDATES = [
    { id: 'demo-1', tool_name: 'React', category: 'Frontend Framework', version: '19.1', summary: 'Server Actions, improved compiler, automatic memoization.', source: 'github', source_url: 'https://github.com/facebook/react/releases', trend_score: 98, published_at: '2026-03-14T10:00:00Z' },
    { id: 'demo-2', tool_name: 'Bun', category: 'Runtime', version: '1.2', summary: 'Native S3, built-in Postgres, faster test runner.', source: 'hackernews', trend_score: 91, published_at: '2026-03-13T08:00:00Z' },
    { id: 'demo-3', tool_name: 'Astro', category: 'Frontend Framework', version: '5.0', summary: 'Content Layer, Server Islands, simplified config.', source: 'producthunt', trend_score: 87, published_at: '2026-03-12T14:00:00Z' },
    { id: 'demo-4', tool_name: 'Django', category: 'Backend Framework', version: '5.1', summary: 'Composite primary keys, generated model fields, streamlined middleware.', source: 'github', trend_score: 82, published_at: '2026-03-11T09:00:00Z' },
    { id: 'demo-5', tool_name: 'Tailwind CSS', category: 'CSS Framework', version: '4.0', summary: 'Rust engine, CSS-first config, auto content detection.', source: 'hackernews', trend_score: 93, published_at: '2026-03-10T11:00:00Z' },
    { id: 'demo-6', tool_name: 'LangChain', category: 'AI/ML', version: '0.3', summary: 'Simplified chains, structured output, improved streaming.', source: 'github', trend_score: 86, published_at: '2026-03-09T15:00:00Z' },
    { id: 'demo-7', tool_name: 'Docker', category: 'DevOps', version: '27.0', summary: 'Compose v3, improved buildx, rootless mode improvements.', source: 'hackernews', trend_score: 79, published_at: '2026-03-08T12:00:00Z' },
    { id: 'demo-8', tool_name: 'Vite', category: 'Build Tool', version: '6.0', summary: 'Environment API, Rolldown-powered builds.', source: 'github', trend_score: 88, published_at: '2026-03-07T10:30:00Z' },
];

export default function ExplorePage() {
    const [activeCategory, setActiveCategory] = useState('All');
    const [searchQuery, setSearchQuery] = useState('');
    const [updates, setUpdates] = useState(DEMO_UPDATES);

    useEffect(() => {
        const category = activeCategory === 'All' ? '' : activeCategory;
        getUpdates(20, 0, category)
            .then(data => { if (data?.updates?.length) setUpdates(data.updates); })
            .catch(() => setUpdates(DEMO_UPDATES.filter(u => activeCategory === 'All' || u.category === activeCategory)));
    }, [activeCategory]);

    const filtered = updates.filter(u => {
        const matchCat = activeCategory === 'All' || u.category === activeCategory;
        const matchSearch = !searchQuery || u.tool_name?.toLowerCase().includes(searchQuery.toLowerCase()) || u.summary?.toLowerCase().includes(searchQuery.toLowerCase());
        return matchCat && matchSearch;
    });

    return (
        <div className="page">
            <div className="container">
                <div className="section-header animate-fade-in">
                    <h1 className="section-title">
                        🔍 <span className="gradient-text">Explore</span>
                    </h1>
                    <p className="section-subtitle">
                        Browse tools and updates by category
                    </p>
                </div>

                {/* Search */}
                <div className="search-wrapper mb-lg animate-fade-in">
                    <span className="search-icon">🔎</span>
                    <input
                        type="text"
                        className="search-input"
                        placeholder="Search tools and updates…"
                        value={searchQuery}
                        onChange={e => setSearchQuery(e.target.value)}
                        id="explore-search"
                    />
                </div>

                {/* Category chips */}
                <div className="chip-group mb-lg animate-fade-in">
                    {CATEGORIES.map(cat => (
                        <button
                            key={cat}
                            className={`chip ${activeCategory === cat ? 'active' : ''}`}
                            onClick={() => setActiveCategory(cat)}
                        >
                            {cat}
                        </button>
                    ))}
                </div>

                {/* Results */}
                <div className="grid-2">
                    {filtered.length > 0 ? (
                        filtered.map((update, i) => (
                            <UpdateCard key={update.id} update={update} index={i} />
                        ))
                    ) : (
                        <div className="card text-center" style={{ gridColumn: '1 / -1', padding: '3rem' }}>
                            <p style={{ color: 'var(--text-tertiary)', fontSize: '1.1rem' }}>
                                No updates found for this filter. Try another category or search term.
                            </p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
