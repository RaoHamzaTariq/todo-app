"""
JWT Bearer token authentication middleware for FastAPI.

This module provides stateless JWT verification using python-jose.
The user_id is extracted from the JWT token claims for all protected endpoints.
"""

from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

from src.app.config import settings


# HTTP Bearer scheme for JWT extraction
security_scheme = HTTPBearer(
    scheme_name="Bearer",
    description="JWT token in the format: Bearer <token>"
)


class JWTBearer:
    """
    JWT verification middleware for FastAPI.

    Verifies JWT tokens using the shared BETTER_AUTH_SECRET.
    Extracts user_id from token claims for user isolation.
    """

    def __init__(self):
        self.secret = settings.better_auth_secret
        self.algorithm = settings.jwt_algorithm

    async def __call__(
        self,
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme)
    ) -> dict:
        """
        Decode and verify JWT token.

        Args:
            credentials: HTTP Bearer credentials from request header

        Returns:
            dict: Decoded JWT payload with user_id

        Raises:
            HTTPException: If token is invalid, expired, or missing user_id
        """
        token = credentials.credentials

        try:
            # Decode JWT using shared secret
            payload = jwt.decode(
                token,
                self.secret,
                algorithms=[self.algorithm]
            )

            # Validate expiration (exp claim)
            exp = payload.get("exp")
            if exp and datetime.utcnow().timestamp() > exp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            # Extract user_id from token
            user_id = payload.get("user_id") or payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user_id",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return {"user_id": user_id, "payload": payload}

        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid token: {str(e)}",
                headers={"WWW-Authenticate": "Bearer"},
            )


def verify_ownership(task_user_id: str, auth_user_id: str) -> bool:
    """
    Verify that a task belongs to the authenticated user.

    Args:
        task_user_id: The user_id from the task record
        auth_user_id: The user_id from the JWT token

    Returns:
        bool: True if ownership is verified

    Raises:
        HTTPException: 404 if task doesn't exist or belongs to different user
    """
    if task_user_id != auth_user_id:
        # Return 404 (not 403) to prevent information disclosure
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return True


# Create singleton instance for dependency injection
jwt_bearer = JWTBearer()
