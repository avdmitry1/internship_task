import asyncio

from core.config import settings
from asyncpg import connect


async def test_connection():
    try:
        dsn = str(settings.db.url).replace("postgresql+asyncpg://", "postgresql://")
        conn = await connect(dsn)
        print("Connection successful to database!")
        await conn.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")


asyncio.run(test_connection())
