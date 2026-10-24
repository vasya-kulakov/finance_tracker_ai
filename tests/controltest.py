import asyncio
from sqlalchemy import text
from src.db.database import engine

async def main():
    async with engine.connect() as conn:
        print((await conn.execute(text("select 1"))).scalar())
    await engine.dispose()

asyncio.run(main())