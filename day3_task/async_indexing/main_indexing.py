
import asyncio
from async_many_to_many.database import engine, Base
import crud_indexing

async def main():
    print("Creating tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")

    # Insert dummy data
    # await crud_indexing.create_dummy_data()

    # Compare performance
    # await crud_indexing.query_without_index()
    await crud_indexing.query_with_index()

if __name__ == "__main__":
    asyncio.run(main())
