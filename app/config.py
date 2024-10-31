import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://:memory:")  # Ganti dengan URL PostgreSQL Anda
    SWAGGER_UI_DOC_EXPANSION = "list"  # Pengaturan Swagger
    RESTX_MASK_SWAGGER = False
