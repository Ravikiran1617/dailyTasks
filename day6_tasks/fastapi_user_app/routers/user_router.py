from fastapi import APIRouter, Depends
from core.security import require_role

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/users/profile")
def profile(user = Depends(require_role("user"))):
    return {"message": "User Profile", "user": user}
