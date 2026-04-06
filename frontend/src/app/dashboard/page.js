'use client';

import { useState, useEffect, useCallback } from 'react';
import UpdateCard from '@/components/UpdateCard';
import { getUserFeed, getUserPreferences, setUserPreferences } from '@/lib/api';

const ALL_TOPICS = [
    'Frontend Framework', 'Backend Framework', 'Runtime',
    'Build Tool', 'CSS Framework', 'AI/ML',
    'DevOps', 'Database', 'Backend-as-a-Service', 'Language', 'Mobile',
];

const DEMO_FEED = [
    { id: 'demo-1', tool_name: 'React',       category: 'Frontend Framework', version: '19.1', summary: 'Server Actions, improved compiler, automatic memoization.',  source: 'github',     trend_score: 98, published_at: '2026-03-14T10:00:00Z' },
    { id: 'demo-5', tool_name: 'Tailwind CSS', category: 'CSS Framework',      version: '4.0',  summary: 'Rust engine, CSS-first config, auto content detection.',    source: 'hackernews', trend_score: 93, published_at: '2026-03-10T11:00:00Z' },
    { id: 'demo-8', tool_name: 'Vite',         category: 'Build Tool',          version: '6.0',  summary: 'Environment API, Rolldown-powered builds.',                 source: 'github',     trend_score: 88, published_at: '2026-03-07T10:30:00Z' },
];

export default function DashboardPage() {
    const [topics,  setTopics]  = useState([]);
    const [feed,    setFeed]    = useState(DEMO_FEED);
    const [saving,  setSaving]  = useState(false);
    const [loading, setLoading] = useState(true);

    // Load preferences and personalized feed on mount
    useEffect(() => {
        Promise.all([
            getUserPreferences().catch(() => ({ preferences: [] })),
            getUserFeed(20, 0).catch(() => ({ updates: [] })),
        ]).then(([prefData, feedData]) => {
            // Preferences come back as [{ id, user_id, topic }, ...]
            const savedTopics = (prefData.preferences || []).map(p => p.topic);
            if (savedTopics.length) setTopics(savedTopics);
            if (feedData.updates?.length) setFeed(feedData.updates);
        }).finally(() => setLoading(false));
    }, []);

    // Toggle a topic chip and immediately persist to the backend
    const toggleTopic = useCallback(async (topic) => {
        const next = topics.includes(topic)
            ? topics.filter(t => t !== topic)
            : [...topics, topic];

        // Optimistic update
        setTopics(next);
        setSaving(true);
        try {
            await setUserPreferences(next);
        } catch {
            // Rollback on failure
            setTopics(topics);
        } finally {
            setSaving(false);
        }
    }, [topics]);

    return (
        <div className="page">
            <div className="container">
                <div className="section-header animate-fade-in">
                    <h1 className="section-title">
                        📊 <span className="gradient-text">Your Dashboard</span>
                    </h1>
                    <p className="section-subtitle">
                        Updates personalized to your interests
                        {saving && (
                            <span style={{ marginLeft: '0.5rem', fontSize: '0.8rem', color: 'var(--text-tertiary)' }}>
                                Saving…
                            </span>
                        )}
                    </p>
                </div>

                {/* Topic selection */}
                <div className="card mb-lg animate-fade-in" id="topic-selector">
                    <h3 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: '0.75rem', color: 'var(--text-secondary)' }}>
                        Your Topics
                        <span style={{ fontWeight: 400, marginLeft: '0.5rem', fontSize: '0.8rem' }}>
                            — click to toggle, saves instantly
                        </span>
                    </h3>
                    <div className="chip-group">
                        {ALL_TOPICS.map(topic => (
                            <button
                                key={topic}
                                className={`chip ${topics.includes(topic) ? 'active' : ''}`}
                                onClick={() => toggleTopic(topic)}
                                disabled={saving}
                            >
                                {topics.includes(topic) ? '✓ ' : ''}{topic}
                            </button>
                        ))}
                    </div>
                </div>

                {/* Feed */}
                {loading ? (
                    <div className="card text-center animate-fade-in" style={{ padding: '3rem' }}>
                        <p style={{ color: 'var(--text-tertiary)' }}>Loading your feed…</p>
                    </div>
                ) : feed.length > 0 ? (
                    <div className="grid-2">
                        {feed.map((update, i) => (
                            <UpdateCard key={update.id} update={update} index={i} />
                        ))}
                    </div>
                ) : (
                    <div className="card text-center animate-fade-in" style={{ padding: '3rem' }}>
                        <p style={{ fontSize: '1.1rem', color: 'var(--text-tertiary)' }}>
                            Select topics above to see personalized updates.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}
