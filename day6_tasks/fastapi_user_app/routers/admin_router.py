from fastapi import APIRouter, Depends
from core.security import require_role

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/admin/dashboard")
def admin_dashboard(user = Depends(require_role("admin"))):
    return {"message": "Welcome Admin", "user": user}