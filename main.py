from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from app.routes import users
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="User CRUD API")

# Register routes
app.include_router(users.router)

# Database configuration
TORTOISE_ORM = {
    "connections": {
        "default": os.getenv("DATABASE_URL")
    },
    "apps": {
        "models": {
            "models": ["app.models.users", "aerich.models"],
            "default_connection": "default",
        },
    },
}

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True,
)