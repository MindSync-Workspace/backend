from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "notes" DROP COLUMN "token_identifier";
        ALTER TABLE "notes" DROP COLUMN "embedding";
        ALTER TABLE "documents" RENAME COLUMN "file_id" TO "file_path";
        ALTER TABLE "documents" DROP COLUMN "token_identifier";
        ALTER TABLE "documents" DROP COLUMN "embedding";
        ALTER TABLE "chats" DROP COLUMN "token_identifier";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "chats" ADD "token_identifier" VARCHAR(255);
        ALTER TABLE "notes" ADD "token_identifier" VARCHAR(255);
        ALTER TABLE "notes" ADD "embedding" JSONB;
        ALTER TABLE "documents" ADD "token_identifier" VARCHAR(255);
        ALTER TABLE "documents" ADD "embedding" JSONB;
        ALTER TABLE "documents" RENAME COLUMN "file_path" TO "file_id";"""
