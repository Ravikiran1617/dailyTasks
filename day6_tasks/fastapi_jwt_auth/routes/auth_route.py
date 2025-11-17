from fastapi import APIRouter, HTTPException, status, Depends
from models.user_model import fake_user_db
from schemas.user_schema import UserLogin, TokenResponse
from utils.hash_utils import verify_password
from core.security import create_access_token, blacklisted_tokens
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from core.config import settings
from core.dependencies import get_current_user

bearer_scheme  = HTTPBearer()
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


@router.post("/logout")
def logout(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme )):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        blacklisted_tokens.add(token)
        return {"message": "Successfully logged out"}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


