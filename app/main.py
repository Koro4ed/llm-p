from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_auth import router as auth_router
from app.api.routes_chat import router as chat_router

from app.db.base import Base
from app.db.session import engine
from app.core.config import settings


def create_app():

    app = FastAPI(title=settings.app_name)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(chat_router)

    @app.on_event("startup")
    async def startup():

        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @app.get("/health")
    async def health():
        return {"status": "ok", "env": settings.env}

    return app


app = create_app()
