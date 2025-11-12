from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sync_crud_operations.models import User

# CREATE
def create_user(db: Session, name: str, email: str):
    try:
        new_user = User(name=name, email=email)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"success": True, "user": new_user}
    except IntegrityError:
        db.rollback()
        return {"success": False, "error": "Email already exists. Please use a unique email."}
    except SQLAlchemyError as e:
        db.rollback()
        return {"success": False, "error": str(e)}

# READ
def get_users(db: Session):
    try:
        users = db.query(User).all()
        return {"success": True, "data": users}
    except SQLAlchemyError as e:
        return {"success": False, "error": str(e)}

# UPDATE
def update_user_email(db: Session, user_id: int, new_email: str):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "error": "User not found."}

        user.email = new_email
        db.commit()
        db.refresh(user)
        return {"success": True, "user": user}
    except IntegrityError:
        db.rollback()
        return {"success": False, "error": "Email already exists. Cannot update to a duplicate email."}
    except SQLAlchemyError as e:
        db.rollback()
        return {"success": False, "error": str(e)}

# DELETE
def delete_user(db: Session, user_id: int):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"success": False, "error": "User not found."}
        db.delete(user)
        db.commit()
        return {"success": True, "message": "User deleted successfully."}
    except SQLAlchemyError as e:
        db.rollback()
        return {"success": False, "error": str(e)}
