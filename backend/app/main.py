"""FastAPI app entrypoint."""
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.middleware.logging import LoggingMiddleware
# from app.middleware.audit import AuditMiddleware
# from app.middleware.rate_limit import RateLimitMiddleware
from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS)
app.add_middleware(LoggingMiddleware)
# app.add_middleware(AuditMiddleware)
# app.add_middleware(RateLimitMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def read_root():
    return {"Message": " Hello World! Welcome to the Care4U platform!"}