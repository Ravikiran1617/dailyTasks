from fastapi import FastAPI
from routes import auth_route

app = FastAPI(title="JWT Auth API", version="1.0")

app.include_router(auth_route.router)

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "JWT Auth API is running"}
