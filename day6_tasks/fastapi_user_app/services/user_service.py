from fastapi import HTTPException, status, BackgroundTasks
from models.user_model import users_db
from schemas.user_schema import UserRegister, UserResponse, UserLogin
from core.security import hash_password, verify_password 
from . import send_emails

def register_user(user: UserRegister, background_tasks) -> UserResponse:
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pw = hash_password(user.password)
    users_db[user.email] = {
        "username": user.username,
        "email": user.email,
        "password": hashed_pw,
        "role": user.role
    }
    # day 8 task to send the user an email about successful registration
    background_tasks.add_task(send_emails.send_registeration_email_to_user, user.email)
    return UserResponse(
        username=user.username,
        email=user.email,
        role=user.role
    )


def verify_user(user: UserLogin) -> UserResponse:
    stored_user = users_db.get(user.email)
    if not stored_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    return UserResponse(
        username=stored_user["username"],
        email=stored_user["email"],
        role=stored_user["role"]
    )
