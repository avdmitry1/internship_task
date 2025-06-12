import asyncio

from dotenv import load_dotenv
from core.config import settings
from asyncpg import connect

load_dotenv()


async def test_connection():
    try:
        conn = await connect(str(settings.db.url))
        print("Connection successful to database!")
        await conn.close()
    except Exception as e:
        print(f"Error connecting to database: {e}")


asyncio.run(test_connection())
