from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sync_crud_operations.models import User

# CREATE
async def create_user(db, name: str, email: str):
    try:
        new_user = User(name=name, email=email)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return {"success": True, "user": new_user}
    except IntegrityError:
        await db.rollback()
        return {"success": False, "error": "Email already exists."}
    except SQLAlchemyError as e:
        await db.rollback()
        return {"success": False, "error": str(e)}

# READ
async def get_users(db):
    try:
        result = await db.execute(select(User))
        users = result.scalars().all()
        return {"success": True, "data": users}
    except SQLAlchemyError as e:
        return {"success": False, "error": str(e)}

# UPDATE
async def update_user_email(db, user_id: int, new_email: str):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return {"success": False, "error": "User not found."}
        user.email = new_email
        await db.commit()
        await db.refresh(user)
        return {"success": True, "user": user}
    except IntegrityError:
        await db.rollback()
        return {"success": False, "error": "Email already exists."}
    except SQLAlchemyError as e:
        await db.rollback()
        return {"success": False, "error": str(e)}

# DELETE
async def delete_user(db, user_id: int):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalars().first()
        if not user:
            return {"success": False, "error": "User not found."}
        await db.delete(user)
        await db.commit()
        return {"success": True, "message": "User deleted successfully."}
    except SQLAlchemyError as e:
        await db.rollback()
        return {"success": False, "error": str(e)}
