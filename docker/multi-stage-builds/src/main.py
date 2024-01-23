import time

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from src.comments.routers import router as comments_router
from src.config import settings
from src.events.routers import router as events_router
from src.reservations.routers import router as reservations_router
from src.tasks.routers import router as tasks_router
from src.users.routers import router as users_router

app = FastAPI(
    title=settings.app_name
)

app.mount("/static", StaticFiles(directory="static"))

app.include_router(users_router)
app.include_router(events_router)
app.include_router(reservations_router)
app.include_router(comments_router)
app.include_router(tasks_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.redis_host}:{settings.redis_port}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/operazione_lunghissima")
@cache(expire=20)
async def lunghissima():
    time.sleep(3)
    return {"operazione": "lunghissima"}


connected_users = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_users.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text("hai inviato questo messaggio: " + data)
    except:
        connected_users.remove(websocket)


@app.post("/send_message_to_all_websocket_users")
async def send_message_to_all_websocket_users(payload: dict):
    for user in connected_users:
        await user.send_json(payload)
    return {"message": "ok"}
