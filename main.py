from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
import os
from app.routes.users import router as user_router  # Adjust import based on your project structure


app = FastAPI(title="API for Mindsync", version="1.0.0")

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "mindsync")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
)

register_tortoise(
    app,
    db_url=DATABASE_URL,
    modules={"models": ["app.models.users"]},  
    generate_schemas=True,
    add_exception_handlers=True,
)

app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Welcome To Mindsync API"}
