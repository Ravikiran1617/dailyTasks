from fastapi import APIRouter, HTTPException, status, Depends
from models.user_model import fake_user_db
from schemas.user_schema import UserLogin, TokenResponse
from utils.hash_utils import verify_password
from core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    stored_user = fake_user_db.get(user.username)
    if not stored_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(user.password, stored_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token)
