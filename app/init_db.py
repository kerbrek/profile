import asyncio

from alembic import command
from alembic.config import Config
from sqlalchemy import text

from . import database, models


async def create_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def drop_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)


# Programmatic Alembic API use (connection sharing) With Asyncio
# https://alembic.sqlalchemy.org/en/latest/cookbook.html#programmatic-api-use-connection-sharing-with-asyncio
def run_alembic_upgrade(connection, cfg):
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


async def alembic_create_tables():
    async with database.engine.begin() as conn:
        await conn.run_sync(run_alembic_upgrade, Config("alembic.ini"))


async def drop_alembic_version_table():
    async with database.engine.begin() as conn:
        await conn.execute(text("DROP TABLE IF EXISTS alembic_version;"))


async def alembic_drop_tables():
    await drop_tables()
    await drop_alembic_version_table()


if __name__ == "__main__":
    asyncio.run(create_tables())
