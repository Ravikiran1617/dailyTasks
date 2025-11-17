from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
from core.config import settings
from models.user_model import users_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

blacklisted_tokens = set()

# ----------------------------
# Password Helpers
# ----------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ----------------------------
# Token Creation
# ----------------------------
def create_access_token(data: dict):
    """
    data must include:
        {
            "sub": email,
            "role": "admin" or "user"
        }
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# ----------------------------
# Get Current User (Authentication)
# ----------------------------
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    # Check if token is revoked
    if token in blacklisted_tokens:
        raise HTTPException(status_code=401, detail="Token revoked")

    try:
        # Decode JWT
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        email = payload.get("sub")
        role = payload.get("role")
        print('role:::==>', role)   # <-- role from JWT

        if not email or not role:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Lookup user
        user = users_db.get(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Attach role from token
        user_with_role = {**user, "role": role}

        return user_with_role, token

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


# ----------------------------
# Role-Based Access Control
# ----------------------------
def require_role(required_role: str):
    """
    Usage:
        Depends(require_role("admin"))
        Depends(require_role("user"))
    """

    def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] != required_role:
            print(user["role"]) 
            raise HTTPException(
                status_code=403,
                detail=f"Access forbidden: requires {required_role} role"
            )
        return user

    return role_checker
