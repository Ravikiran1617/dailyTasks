from fastapi import FastAPI
from database import engine
import models
from routers import auth_router, books_router, members_router
from utils.startup import create_default_librarian

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

# Run default librarian setup on startup
@app.on_event("startup")
def startup_event():
    create_default_librarian()

@app.get("/")
def root():
    return {"message": "Welcome to Library Management System"}

# Routers
app.include_router(auth_router.router)
app.include_router(books_router.router)
app.include_router(members_router.router)
