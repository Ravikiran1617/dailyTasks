from fastapi import FastAPI
from v1.users import router as users_v1_router
from v2.users import router as users_v2_router

app = FastAPI(
    title="Versioned API Example",
    description="API Versioning Demo (v1, v2)",
    version="2.0.0"
)

# Include routers
app.include_router(users_v1_router, prefix="/v1")
app.include_router(users_v2_router, prefix="/v2")
