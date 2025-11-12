import asyncio
from async_database import AsyncSessionLocal, Base, engine
import crud_async


async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await setup_db()

    async with AsyncSessionLocal() as db:
        print("Creating users...")
        print(await crud_async.create_user(db, "Ravi Kiran", "ravi@example.com"))
        print(await crud_async.create_user(db, "Sai Ashrith", "sai@example.com"))

        print("\nAll users:")
        res = await crud_async.get_users(db)
        if res["success"]:
            for user in res["data"]:
                print(f"{user.id}: {user.name} ({user.email})")

        print("\nUpdating user email...")
        print(await crud_async.update_user_email(db, 1, "ravi.new@example.com"))

        print("\nDeleting user...")
        print(await crud_async.delete_user(db, 2))

        print("\nFinal users:")
        final_res = await crud_async.get_users(db)
        if final_res["success"]:
            for user in final_res["data"]:
                print(f"{user.id}: {user.name} ({user.email})")

asyncio.run(main())
