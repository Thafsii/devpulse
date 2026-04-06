'use client';

import { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import { signOut, getSession } from '@/lib/supabase';
import { getBookmarks, deleteBookmark, getUserPreferences, setUserPreferences } from '@/lib/api';

const ALL_TOPICS = [
    'Frontend Framework', 'Backend Framework', 'Runtime',
    'Build Tool', 'CSS Framework', 'AI/ML',
    'DevOps', 'Database', 'Backend-as-a-Service', 'Language', 'Mobile',
];

export default function ProfilePage() {
    const [user,      setUser]      = useState(null);
    const [topics,    setTopics]    = useState([]);
    const [bookmarks, setBookmarks] = useState([]);
    const [saving,    setSaving]    = useState(false);
    const [loading,   setLoading]   = useState(true);

    // Load session, preferences, and bookmarks on mount
    useEffect(() => {
        getSession().then(session => {
            if (session?.user) setUser(session.user);
        });

        Promise.all([
            getUserPreferences().catch(() => ({ preferences: [] })),
            getBookmarks().catch(() => ({ bookmarks: [] })),
        ]).then(([prefData, bkData]) => {
            const saved = (prefData.preferences || []).map(p => p.topic);
            if (saved.length) setTopics(saved);
            setBookmarks(bkData.bookmarks || []);
        }).finally(() => setLoading(false));
    }, []);

    const toggleTopic = useCallback(async (topic) => {
        const next = topics.includes(topic)
            ? topics.filter(t => t !== topic)
            : [...topics, topic];
        setTopics(next);
        setSaving(true);
        try {
            await setUserPreferences(next);
        } catch {
            setTopics(topics); // rollback
        } finally {
            setSaving(false);
        }
    }, [topics]);

    const removeBookmark = async (id) => {
        try {
            await deleteBookmark(id);
            setBookmarks(prev => prev.filter(b => b.id !== id));
        } catch { /* ignore */ }
    };

    const handleSignOut = async () => {
        await signOut();
        window.location.href = '/';
    };

    const displayName = user?.user_metadata?.display_name || user?.email?.split('@')[0] || 'Developer';
    const initial     = displayName[0].toUpperCase();

    return (
        <div className="page">
            <div className="container" style={{ maxWidth: 800 }}>

                {/* Profile Header */}
                <div className="profile-header animate-fade-in">
                    <div className="avatar">{initial}</div>
                    <div>
                        <h1 style={{ fontSize: '1.5rem', fontWeight: 800 }}>{displayName}</h1>
                        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                            {user?.email || 'Not signed in'}
                        </p>
                    </div>
                </div>

                {/* Topic Preferences */}
                <section className="animate-slide-up stagger-1">
                    <h2 className="section-title mb-lg">
                        ⚙️ Your Topics
                        {saving && (
                            <span style={{ fontWeight: 400, marginLeft: '0.5rem', fontSize: '0.8rem', color: 'var(--text-tertiary)' }}>
                                Saving…
                            </span>
                        )}
                    </h2>
                    <div className="card">
                        <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginBottom: '1rem' }}>
                            Select the topics you care about. Your dashboard will show updates matching these preferences.
                        </p>
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
                </section>

                {/* Saved Bookmarks */}
                <section className="mt-2xl animate-slide-up stagger-3">
                    <h2 className="section-title mb-lg">🔖 Saved Items</h2>
                    {loading ? (
                        <div className="card text-center" style={{ padding: '2rem', color: 'var(--text-tertiary)' }}>
                            Loading bookmarks…
                        </div>
                    ) : bookmarks.length > 0 ? (
                        <div className="flex flex-col gap-md">
                            {bookmarks.map((bk) => {
                                // bookmarks may embed processed_updates or tools via Supabase join
                                const update = bk.processed_updates;
                                const tool   = bk.tools;
                                const title  = update?.tool_name || tool?.name || '—';
                                const cat    = update?.category  || tool?.category || '';
                                const body   = update?.summary   || tool?.description || '';
                                const saved  = new Date(bk.created_at).toLocaleDateString('en-US', {
                                    month: 'short', day: 'numeric', year: 'numeric',
                                });
                                return (
                                    <div key={bk.id} className="card">
                                        <div className="card-header">
                                            <div>
                                                <h3 className="card-title">{title}</h3>
                                                {cat && <span className="badge badge-category">{cat}</span>}
                                            </div>
                                            <button
                                                className="bookmark-btn active"
                                                title="Remove bookmark"
                                                onClick={() => removeBookmark(bk.id)}
                                            >
                                                ★
                                            </button>
                                        </div>
                                        {body && <p className="card-body">{body}</p>}
                                        <div className="card-meta mt-sm">Saved {saved}</div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="card text-center" style={{ padding: '2rem', color: 'var(--text-tertiary)' }}>
                            No saved items yet. Bookmark tools and updates to see them here.
                        </div>
                    )}
                </section>

                {/* Actions */}
                <div className="mt-xl flex gap-md animate-fade-in">
                    <Link href="/dashboard" className="btn btn-primary">Go to Dashboard →</Link>
                    <button className="btn btn-secondary" onClick={handleSignOut}>
                        Sign Out
                    </button>
                </div>
            </div>
        </div>
    );
}
