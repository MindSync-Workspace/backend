from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "documents" RENAME COLUMN "description" TO "summary";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "documents" RENAME COLUMN "summary" TO "description";"""
