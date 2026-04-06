'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function LoginPage() {
    const [isSignUp, setIsSignUp] = useState(false);
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        try {
            const { signIn, signUp } = await import('@/lib/supabase');
            if (isSignUp) {
                await signUp(email, password);
                setMessage('Account created! Check your email for verification.');
            } else {
                const data = await signIn(email, password);
                if (data?.session?.access_token) {
                    localStorage.setItem('devpulse_token', data.session.access_token);
                    window.location.href = '/dashboard';
                }
            }
        } catch (err) {
            setMessage(err.message || 'Authentication failed. Make sure Supabase is configured.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="page">
            <div className="auth-container animate-fade-in">
                <div className="auth-card">
                    <div className="text-center mb-lg">
                        <Link href="/" className="navbar-brand" style={{ justifyContent: 'center', fontSize: '1.3rem' }}>
                            <span className="logo-dot" />
                            DevPulse
                        </Link>
                    </div>

                    <h1 className="auth-title">
                        {isSignUp ? 'Create Account' : 'Welcome Back'}
                    </h1>

                    <form onSubmit={handleSubmit}>
                        <div className="form-group">
                            <label className="form-label" htmlFor="login-email">Email</label>
                            <input
                                type="email"
                                id="login-email"
                                className="form-input"
                                placeholder="you@example.com"
                                value={email}
                                onChange={e => setEmail(e.target.value)}
                                required
                            />
                        </div>

                        <div className="form-group">
                            <label className="form-label" htmlFor="login-password">Password</label>
                            <input
                                type="password"
                                id="login-password"
                                className="form-input"
                                placeholder="••••••••"
                                value={password}
                                onChange={e => setPassword(e.target.value)}
                                required
                                minLength={6}
                            />
                        </div>

                        {message && (
                            <p style={{
                                fontSize: '0.85rem',
                                marginBottom: '1rem',
                                padding: '0.5rem 0.75rem',
                                borderRadius: 'var(--radius-sm)',
                                background: message.includes('created') ? 'rgba(16,185,129,0.1)' : 'rgba(244,63,94,0.1)',
                                color: message.includes('created') ? 'var(--accent-emerald)' : 'var(--accent-rose)',
                            }}>
                                {message}
                            </p>
                        )}

                        <button
                            type="submit"
                            className="btn btn-primary w-full"
                            disabled={loading}
                            style={{ marginBottom: '1rem' }}
                        >
                            {loading ? 'Loading…' : (isSignUp ? 'Create Account' : 'Sign In')}
                        </button>
                    </form>

                    <p className="text-center" style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                        {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
                        <button
                            onClick={() => { setIsSignUp(!isSignUp); setMessage(''); }}
                            style={{
                                background: 'none', border: 'none', color: 'var(--accent-indigo)',
                                cursor: 'pointer', fontWeight: 600, fontFamily: 'var(--font-sans)',
                            }}
                        >
                            {isSignUp ? 'Sign In' : 'Sign Up'}
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
}
