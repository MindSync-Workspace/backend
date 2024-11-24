from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import (
    router as user_router,
)
from app.routes.notes import (
    router as note_router,
)
from app.routes.organizations import (
    router as organization_router,
)
from app.routes.memberships import (
    router as membership_router,
)


app = FastAPI(title="API for Mindsync", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "mindsync")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgres://postgres:admin123@localhost:5432/mindsync",
)


register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={
        "models": [
            "app.models.users",
            "app.models.notes",
            "app.models.organizations",
            "app.models.memberships",
            "app.models.documents",
            "app.models.chats",
        ]
    },
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(user_router)
app.include_router(note_router)
app.include_router(organization_router)
app.include_router(membership_router)


@app.get("/")
async def root():
    return {"message": "Welcome To Mindsync API"}
