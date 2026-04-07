"""
DevPulse Backend — Supabase Client
"""
from supabase import create_client, Client
from app.config import settings

_client: Client | None = None


class SupabaseNotConfiguredError(RuntimeError):
    """Raised when Supabase credentials are missing from the environment."""


def get_supabase() -> Client:
    """Return a singleton Supabase client using the service-role key.
    
    Raises SupabaseNotConfiguredError when SUPABASE_URL or keys are not set,
    giving a clear actionable message instead of a cryptic library error.
    """
    global _client
    if _client is None:
        if not settings.SUPABASE_URL:
            raise SupabaseNotConfiguredError(
                "SUPABASE_URL is not set. "
                "Add it to backend/.env (see .env.example for all required keys)."
            )
        key = settings.SUPABASE_SERVICE_ROLE_KEY or settings.SUPABASE_ANON_KEY
        if not key:
            raise SupabaseNotConfiguredError(
                "Neither SUPABASE_SERVICE_ROLE_KEY nor SUPABASE_ANON_KEY is set. "
                "Add at least one to backend/.env."
            )
        _client = create_client(settings.SUPABASE_URL, key)
    return _client
