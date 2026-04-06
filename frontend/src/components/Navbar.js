'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { getSession, signOut, syncTokenToStorage, onAuthStateChange } from '@/lib/supabase';

const NAV_LINKS = [
    { href: '/', label: 'Home' },
    { href: '/explore', label: 'Explore' },
    { href: '/dashboard', label: 'Dashboard' },
];

export default function Navbar() {
    const pathname = usePathname();
    const router   = useRouter();
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Set initial auth state
        getSession().then(session => setUser(session?.user ?? null));

        // Keep localStorage token fresh on every session event
        const unsubSync = syncTokenToStorage();

        // Update navbar when auth state changes (login / logout / token refresh)
        const { data: { subscription } } = onAuthStateChange((_event, session) => {
            setUser(session?.user ?? null);
        });

        return () => {
            unsubSync();
            subscription.unsubscribe();
        };
    }, []);

    const handleSignOut = async () => {
        await signOut();
        setUser(null);
        router.push('/');
    };

    return (
        <nav className="navbar" id="main-navbar">
            <Link href="/" className="navbar-brand">
                <span className="logo-dot" />
                DevPulse
            </Link>

            <ul className="navbar-links">
                {NAV_LINKS.map((link) => (
                    <li key={link.href}>
                        <Link
                            href={link.href}
                            className={pathname === link.href ? 'active' : ''}
                        >
                            {link.label}
                        </Link>
                    </li>
                ))}
            </ul>

            <div className="navbar-actions">
                {user ? (
                    <>
                        <Link href="/profile" className="btn btn-ghost btn-sm">
                            Profile
                        </Link>
                        <button
                            id="navbar-signout-btn"
                            className="btn btn-secondary btn-sm"
                            onClick={handleSignOut}
                        >
                            Sign Out
                        </button>
                    </>
                ) : (
                    <>
                        <Link href="/profile" className="btn btn-ghost btn-sm">
                            Profile
                        </Link>
                        <Link
                            href="/login"
                            id="navbar-signin-btn"
                            className="btn btn-primary btn-sm"
                        >
                            Sign In
                        </Link>
                    </>
                )}
            </div>
        </nav>
    );
}
