from fastapi import APIRouter, Depends
from core.dependencies import add_two_numbers

router = APIRouter(
    prefix="/add",       # All routes in this file will start with /users
    tags=["Addition"],        # Shown as a group in Swagger UI
)

@router.get("/sumof") 
def get_the_sum_number(sum_number = Depends(add_two_numbers)):
    return {"message":f"{sum_number} is the addition of two numbers."} 