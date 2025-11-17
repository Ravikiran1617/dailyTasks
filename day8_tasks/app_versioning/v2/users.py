from fastapi import APIRouter

router = APIRouter()

@router.get("/users")
def get_users_v2():
    return {
        "version": "v2",
        "data": {
            "full_name": "Ravi Kiran Armoor",
            "age": 25,
            "role": "admin",
            "is_active": True
        }
    }
