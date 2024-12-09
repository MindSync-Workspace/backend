from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "documents" ADD "file_id" VARCHAR(255) NOT NULL;
        ALTER TABLE "documents" ADD "extension_type" VARCHAR(10);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "documents" DROP COLUMN "file_id";
        ALTER TABLE "documents" DROP COLUMN "extension_type";"""
