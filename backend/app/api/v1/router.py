"""API v1 router."""
from fastapi import APIRouter
from app.api.v1.routes import auth, requests

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(requests.router, prefix="/requests", tags=["requests"])
