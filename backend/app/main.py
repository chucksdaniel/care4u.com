"""FastAPI app entrypoint."""
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Middleware
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS)
app.add_middleware(LoggingMiddleware)
app.add_middleware(AuditMiddleware)
app.add_middleware(RateLimitMiddleware)