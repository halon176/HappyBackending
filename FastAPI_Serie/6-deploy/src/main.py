from fastapi import FastAPI

from src.comments.routers import router as comments_router
from src.config import settings
from src.events.routers import router as events_router
from src.reservations.routers import router as reservations_router
from src.users.routers import router as users_router

app = FastAPI(
    title=settings.app_name
)

app.include_router(users_router)
app.include_router(events_router)
app.include_router(reservations_router)
app.include_router(comments_router)
