from fastapi import APIRouter, Depends
from core.dependencies import get_current_user, add_two_numbers

# Create a router instance
router = APIRouter(
    prefix="/users",       # All routes in this file will start with /users
    tags=["Users"],        # Shown as a group in Swagger UI
)

# Example route (protected)
@router.get("/me")
def get_user_profile(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello {current_user}, this is your profile."}


