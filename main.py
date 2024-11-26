from fastapi import FastAPI, APIRouter
from tortoise.contrib.fastapi import register_tortoise
import os
from fastapi.middleware.cors import CORSMiddleware
from app.routes.users import router as user_router
from app.routes.notes import router as note_router
from app.routes.organizations import router as organization_router
from app.routes.memberships import router as membership_router
from app.routes.chats import router as chat_router  # Import chat router

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

# Create a main API router with '/api' prefix
api_router = APIRouter(prefix="/api")

# Include the sub-routers with their own prefix
api_router.include_router(user_router)
api_router.include_router(note_router)
api_router.include_router(organization_router)
api_router.include_router(membership_router)
api_router.include_router(chat_router)

# Include the main API router in the app
app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome To Mindsync API"}
