"""CORS middleware setup."""
from fastapi.middleware.cors import CORSMiddleware

from backend.config.settings import settings


def setup_cors(app) -> None:
    """Configure CORS middleware."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
