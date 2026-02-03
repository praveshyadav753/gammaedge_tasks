import redis.asyncio as ai
from fastapi import FastAPI
from contextlib import asynccontextmanager

LOCAL_REDIS_URL = "redis://localhost:6379"


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = ai.from_url(LOCAL_REDIS_URL)
    app.state.redis = redis_client

    try:
        yield
    finally:
        print("good bye")
        await redis_client.aclose()


app = FastAPI(lifespan=lifespan)

@app.get("/ping")
async def ping():
    redis = app.state.redis
    await redis.set("hello", "world")
    return {"msg": await redis.get("hello")}
