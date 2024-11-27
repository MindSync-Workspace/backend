# app/models/users.py
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise
import os


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    password = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.username


# Create Pydantic models for API
UserPydantic = pydantic_model_creator(Users, name="User")
UserInPydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)
UserOutPydantic = pydantic_model_creator(
<<<<<<< Updated upstream
    Users, name="UserOut", exclude=("password",)  # Don't expose password in responses
)


# Database initialization function
async def init():
    # Get database URL from environment variable with a default value
    db_url = os.getenv("DATABASE_URL")

    await Tortoise.init(db_url=db_url, modules={"models": ["app.models.users"]})

    # Generate schemas
    await Tortoise.generate_schemas()
=======
    Users, 
    name="UserOut",
    exclude=("password",)  # Don't expose password in responses
)
>>>>>>> Stashed changes
