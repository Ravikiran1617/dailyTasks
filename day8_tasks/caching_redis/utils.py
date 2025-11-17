from fastapi import HTTPException
from redis import Redis

redis_client = Redis(host="localhost", port=6379, decode_responses=True)

def rate_limit(user_id: str, limit: int, window: int):
    """
    user_id: unique identifier for the user
    limit: max allowed requests
    window: time window in seconds (ex: 60 → 1 minute)
    """
    key = f"rate_limit:{user_id}"

    # Increment request count
    current = redis_client.incr(key)

    # Set TTL if it's the first request
    if current == 1:
        redis_client.expire(key, window)

    # Check limit
    if current > limit:
        ttl = redis_client.ttl(key)
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded. Try again in {ttl} seconds."
        )
