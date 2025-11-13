from fastapi import HTTPException, status
from models.user_model import users_db
from schemas.user_schema import UserRegister, UserResponse, UserLogin
from core.security import hash_password, verify_password

def register_user(user: UserRegister) -> UserResponse:
    """Registers a new user after validating and hashing the password."""
    if user.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    hashed_pw = hash_password(user.password)
    users_db[user.email] = {
        "username": user.username,
        "email": user.email,
        "password": hashed_pw
    }

    return UserResponse(username=user.username, email=user.email)


def verify_user(user: UserLogin) -> UserResponse:
    """Verifies user email and password."""
    stored_user = users_db.get(user.email)
    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    return UserResponse(username=stored_user["username"], email=stored_user["email"])
