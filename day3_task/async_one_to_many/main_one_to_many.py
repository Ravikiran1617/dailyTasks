import asyncio
from database_one_to_many import engine, AsyncSessionLocal
from models_one_to_many import Base
import crud_one_to_many

async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created")

async def main():
    await setup_db()

    async with AsyncSessionLocal() as db:
        # Create users
        print(await crud_one_to_many.create_user(db, "Ravi Kiran", "ravi@example.com"))
        print(await crud_one_to_many.create_user(db, "Sai Ashrith", "sai@example.com"))

        # Create posts
        print(await crud_one_to_many.create_post(db, "Post 1", "Content of post 1", 1))
        print(await crud_one_to_many.create_post(db, "Post 2", "Content of post 2", 1))
        print(await crud_one_to_many.create_post(db, "Post 3", "Content of post 3", 2))

        # Fetch users with posts
        res = await crud_one_to_many.get_users_with_posts(db)
        if res["success"]:
            for user in res["data"]:
                print(f"\nUser: {user.name} ({user.email})")
                for post in user.posts:
                    print(f"  Post: {post.title} - {post.content}")
        else:
            print(res["error"])

asyncio.run(main())
