from fastapi import FastAPI
from schemas.user_schema import UserRegister, UserResponse, UserLogin
from services.user_service import register_user, verify_user

app = FastAPI(title="User Registration API", version="1.0.0")

@app.post("/register", response_model=UserResponse)
def register(user: UserRegister):
    """
    Register a new user with password hashing.
    """
    return register_user(user)

@app.post("/verify", response_model=UserResponse)
def verify(user: UserLogin):
    """
    Verify an existing user by checking email and password.
    """
    return verify_user(user)
