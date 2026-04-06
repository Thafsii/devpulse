/**
 * DevPulse — Backend API Helpers
 */

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

async function apiFetch(path, options = {}) {
  const url = `${API_BASE}${path}`;
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };

  // Attach auth token if available
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('devpulse_token');
    if (token) headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(url, { ...options, headers });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

// ── Updates ──────────────────────────────────────────────

export async function getUpdates(limit = 20, offset = 0, category = '') {
  const params = new URLSearchParams({ limit, offset });
  if (category) params.set('category', category);
  return apiFetch(`/updates?${params}`);
}

export async function getTrendingTools(limit = 10) {
  return apiFetch(`/trending-tools?limit=${limit}`);
}

// ── Tools ────────────────────────────────────────────────

export async function getTools(category = '', limit = 20) {
  const params = new URLSearchParams({ limit });
  if (category) params.set('category', category);
  return apiFetch(`/tools?${params}`);
}

export async function getTool(id) {
  return apiFetch(`/tools/${id}`);
}

// ── Feed ─────────────────────────────────────────────────

export async function getUserFeed(limit = 20, offset = 0) {
  return apiFetch(`/user-feed?limit=${limit}&offset=${offset}`);
}

export async function getUserPreferences() {
  return apiFetch('/user-preferences');
}

export async function setUserPreferences(topics) {
  return apiFetch('/user-preferences', {
    method: 'POST',
    body: JSON.stringify(topics),
  });
}

// ── Bookmarks ────────────────────────────────────────────

export async function createBookmark(updateId, toolId) {
  return apiFetch('/bookmark', {
    method: 'POST',
    body: JSON.stringify({ update_id: updateId, tool_id: toolId }),
  });
}

export async function deleteBookmark(bookmarkId) {
  return apiFetch(`/bookmark/${bookmarkId}`, { method: 'DELETE' });
}

export async function getBookmarks() {
  return apiFetch('/bookmarks');
}
