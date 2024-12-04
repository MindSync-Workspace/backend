from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "chats" ADD "modified_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" DROP COLUMN "created_at";
        ALTER TABLE "chats" DROP COLUMN "modified_at";"""
