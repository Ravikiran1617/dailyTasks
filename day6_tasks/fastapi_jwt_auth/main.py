from fastapi import FastAPI
from routes import auth_route, user_route, add_two_numbers
app = FastAPI(title="JWT Auth API", version="1.0")

app.include_router(auth_route.router)
app.include_router(user_route.router) 
app.include_router(add_two_numbers.router) 

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "JWT Auth API is running"}
