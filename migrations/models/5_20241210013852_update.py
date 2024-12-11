from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" ALTER COLUMN "text" TYPE TEXT USING "text"::TEXT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" ALTER COLUMN "text" TYPE VARCHAR(255) USING "text"::VARCHAR(255);"""
