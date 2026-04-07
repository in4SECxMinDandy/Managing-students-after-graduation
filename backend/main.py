"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.auth.router import router as auth_router
from apps.admissions.router import router as admissions_router
from apps.training.router import router as training_router
from apps.thesis.router import router as thesis_router
from apps.finance.router import router as finance_router
from apps.support.router import router as support_router
from backend.config.settings import settings
from backend.core.handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    yield
    # Shutdown


def create_app() -> FastAPI:
    """Factory to create FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        lifespan=lifespan,
        debug=settings.debug,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    register_exception_handlers(app)

    # Register module routers
    app.include_router(auth_router)
    app.include_router(admissions_router)
    app.include_router(training_router)
    app.include_router(thesis_router)
    app.include_router(finance_router)
    app.include_router(support_router)

    return app


app = create_app()
