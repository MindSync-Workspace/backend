from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "whatsapps" ADD "number" VARCHAR(20)  UNIQUE;
        CREATE UNIQUE INDEX "uid_whatsapps_number_a7f488" ON "whatsapps" ("number");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP INDEX "idx_whatsapps_number_a7f488";
        ALTER TABLE "whatsapps" DROP COLUMN "number";"""
