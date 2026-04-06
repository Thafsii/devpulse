/**
 * DevPulse — Supabase Client (Frontend)
 *
 * Key fix: `onAuthStateChange` now keeps `localStorage.devpulse_token`
 * in sync with every session event (sign-in, token refresh, sign-out).
 * Without this the JWT stored at login goes stale after ~1 hour and all
 * authenticated API calls silently return 401.
 */
import { createClient } from '@supabase/supabase-js';

const supabaseUrl     = process.env.NEXT_PUBLIC_SUPABASE_URL     || '';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || '';

export const supabase = (supabaseUrl && supabaseAnonKey)
    ? createClient(supabaseUrl, supabaseAnonKey, {
        auth: {
            // Keep the session in localStorage so the page doesn't lose auth on reload.
            persistSession: true,
            // Auto-refresh the JWT before it expires (Supabase default is ~1 h).
            autoRefreshToken: true,
        },
    })
    : null;

/**
 * Sync the access token to localStorage on every auth state change.
 * Call this once from a top-level layout/provider so the backend API
 * client always sends a fresh Bearer token.
 *
 * Returns the unsubscribe function — call it on component unmount.
 */
export function syncTokenToStorage() {
    if (!supabase) return () => {};

    const { data: { subscription } } = supabase.auth.onAuthStateChange(
        (_event, session) => {
            if (typeof window === 'undefined') return;
            if (session?.access_token) {
                localStorage.setItem('devpulse_token', session.access_token);
            } else {
                // Signed out or session expired — remove the stale token.
                localStorage.removeItem('devpulse_token');
            }
        }
    );

    return () => subscription.unsubscribe();
}

/**
 * Sign up with email + password
 */
export async function signUp(email, password) {
    if (!supabase) throw new Error('Supabase not configured');
    const { data, error } = await supabase.auth.signUp({ email, password });
    if (error) throw error;
    return data;
}

/**
 * Sign in with email + password.
 * The onAuthStateChange listener (set up by syncTokenToStorage) will
 * automatically persist the token — no manual localStorage call needed.
 */
export async function signIn(email, password) {
    if (!supabase) throw new Error('Supabase not configured');
    const { data, error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) throw error;
    return data;
}

/**
 * Sign out — clears the session from Supabase and from localStorage.
 */
export async function signOut() {
    if (!supabase) return;
    await supabase.auth.signOut();
    if (typeof window !== 'undefined') {
        localStorage.removeItem('devpulse_token');
    }
}

/**
 * Get the current session (or null if unauthenticated).
 */
export async function getSession() {
    if (!supabase) return null;
    const { data: { session } } = await supabase.auth.getSession();
    return session;
}

/**
 * Subscribe to auth state changes.
 */
export function onAuthStateChange(callback) {
    if (!supabase) return { data: { subscription: { unsubscribe: () => {} } } };
    return supabase.auth.onAuthStateChange(callback);
}
