"""
DevPulse Backend — Auth Middleware
Verifies Supabase JWT from the Authorization header.
"""
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client
from app.services.supabase_client import get_supabase

security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict:
    """
    FastAPI dependency — extracts and verifies the Supabase JWT.
    Returns the decoded user payload or raises 401.
    """
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials
    sb: Client = get_supabase()

    try:
        user_response = sb.auth.get_user(token)
        if user_response and user_response.user:
            return {
                "id": str(user_response.user.id),
                "email": user_response.user.email,
            }
    except Exception:
        pass

    raise HTTPException(status_code=401, detail="Invalid or expired token")


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> dict | None:
    """Same as get_current_user but returns None instead of 401."""
    if credentials is None:
        return None
    try:
        return await get_current_user(credentials)
    except HTTPException:
        return None
