"""API v1 router."""
from fastapi import APIRouter
from app.api.v1.routes import auth, requests, users, admin, caregiver

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(caregiver.router, prefix="/caregivers", tags=["caregivers"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(requests.router, prefix="/requests", tags=["requests"])
