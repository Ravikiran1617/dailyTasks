from fastapi import FastAPI
from routers.auth_router import router as auth_router
from routers.task_router import router as task_router
from routers.admin_router import router as admin_router
from routers.user_router import router as user_router

app = FastAPI(title="User Access Control System")

app.include_router(auth_router)
app.include_router(task_router)
app.include_router(admin_router)
app.include_router(user_router)  
