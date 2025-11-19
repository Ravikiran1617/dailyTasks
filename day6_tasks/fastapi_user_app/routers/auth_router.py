from fastapi import APIRouter, Depends, BackgroundTasks
from schemas.user_schema import UserRegister, UserLogin
from services.user_service import register_user, verify_user
from core.security import create_access_token, get_current_user, blacklisted_tokens 
from models.user_model import users_db

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user: UserRegister, background_tasks: BackgroundTasks):
    return register_user(user, background_tasks)

@router.post("/login")
def login(user: UserLogin):
    verified = verify_user(user)

    # Fetch role from DB
    stored_user = users_db.get(verified.email)
    role = stored_user["role"]

    # Create token with role
    token = create_access_token({
        "sub": verified.email,
        "role": role
    })

    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout(token: str = Depends(get_current_user)):
    blacklisted_tokens.add(token)
    return {"message": "Logged out successfully"}
