import time
import uuid
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def logging_and_tracking_middleware(request: Request, call_next):
    # 1. Generate unique request ID
    request_id = str(uuid.uuid4())

    # 2. Record request start time
    start_time = time.time()

    # 3. Log incoming request
    print(f"\n📥 Incoming Request | ID: {request_id}")
    print(f"URL: {request.url}")
    print(f"Method: {request.method}")
    print(f"Client IP: {request.client.host}")

    # 4. Execute the request and get response
    response = await call_next(request)

    # 5. Calculate processing time
    duration = time.time() - start_time

    # 6. Log outgoing response
    print(f"📤 Outgoing Response | ID: {request_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Processing Time: {duration:.4f} seconds")

    # 7. Add request ID to response headers
    response.headers["X-Request-ID"] = request_id

    return response


@app.get("/test")
async def test():
    return {"message": "Middleware working!"}
