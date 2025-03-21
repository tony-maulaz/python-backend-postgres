import asyncio
from db.init import init_db, init_skills

async def main():
    await init_db()
    await init_skills()

if __name__ == "__main__":
    asyncio.run(main())