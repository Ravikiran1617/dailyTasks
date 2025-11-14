from fastapi import APIRouter, Depends
from core.security import get_current_user
from models.task_model import user_tasks

router = APIRouter(prefix="/tasks", tags=["User Tasks"])

@router.get("/")
def get_my_tasks(current_user = Depends(get_current_user)):
    email = current_user["email"]
    return {"tasks": user_tasks.get(email, [])}

@router.post("/add")
def add_task(task: str, current_user = Depends(get_current_user)):
    email = current_user["email"]

    if email not in user_tasks:
        user_tasks[email] = []

    user_tasks[email].append(task)

    return {"message": "Task added", "tasks": user_tasks[email]}
