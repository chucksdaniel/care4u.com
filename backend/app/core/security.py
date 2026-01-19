"""JWT and RBAC checks."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt

from app.core.config import settings


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode a JWT token."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def check_permission(user: Dict[str, Any], required_permission: str) -> bool:
    """Check if user has required permission (RBAC)."""
    # TODO: Implement RBAC permission checking
    user_permissions = user.get("permissions", [])
    return required_permission in user_permissions


def check_role(user: Dict[str, Any], required_role: str) -> bool:
    """Check if user has required role."""
    # TODO: Implement role checking
    user_roles = user.get("roles", [])
    return required_role in user_roles
