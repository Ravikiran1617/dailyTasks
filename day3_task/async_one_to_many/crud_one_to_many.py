from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from models_one_to_many import User, Post

# CREATE User
async def create_user(db, name: str, email: str):
    try:
        user = User(name=name, email=email)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return {"success": True, "user": user}
    except IntegrityError:
        await db.rollback()
        return {"success": False, "error": "Email already exists."}
    except SQLAlchemyError as e:
        await db.rollback()
        return {"success": False, "error": str(e)}

# CREATE Post
async def create_post(db, title: str, content: str, user_id: int):
    try:
        post = Post(title=title, content=content, owner_id=user_id)
        db.add(post)
        await db.commit()
        await db.refresh(post)
        return {"success": True, "post": post}
    except SQLAlchemyError as e:
        await db.rollback()
        return {"success": False, "error": str(e)}

# READ all users with posts
async def get_users_with_posts(db):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return {"success": True, "data": users}
    except SQLAlchemyError as e:
        return {"success": False, "error": str(e)}
