from fastapi import FastAPI

from app.api.routes import router
from app.db import init_db


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    application = FastAPI(title="Auth Service", version="0.1.0")

    @application.on_event("startup")
    def on_startup() -> None:
        init_db()

    application.include_router(router)
    return application


app = create_app()

