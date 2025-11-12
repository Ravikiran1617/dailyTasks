import asyncio
from database import engine, Base
import crud_many_to_many

async def main():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")

    await crud_many_to_many.create_initial_data()
    await crud_many_to_many.fetch_all_data()

if __name__ == "__main__":
    asyncio.run(main())
