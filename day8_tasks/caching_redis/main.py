from fastapi import FastAPI, HTTPException, Header
from redis import Redis
import json
import time
from utils import rate_limit

app = FastAPI()

# Connect to Redis
redis_client = Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)

# Simulate slow function
def slow_operation():
    time.sleep(5)  # simulate 5 second slow task
    return {"message": "Data retrieved successfully"}


@app.get("/redis-cache")
def get_data():

    cache_key = "sample:data"

    # 1️⃣ Check if data exists in Redis
    cached_data = redis_client.get(cache_key)
    if cached_data:
        return {
            "data": json.loads(cached_data),
            "cached": True
        }

    # 2️⃣ If not cached → get fresh data
    result = slow_operation()

    # 3️⃣ Store data in Redis with TTL (e.g., 30 seconds)
    redis_client.set(cache_key, json.dumps(result), ex=30)

    return {
        "data": result,
        "cached": False
    }

@app.get("/secure-data")
def secure_data(x_user_id: str = Header(None)):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-Id header missing")

    # Apply rate limit (5 requests per 60 sec)
    rate_limit(user_id=x_user_id, limit=5, window=60)

    return {"message": f"Hello user {x_user_id}, this is secured data!"}