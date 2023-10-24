from fastapi import FastAPI

# from src.blog.routers import router as blog_router
from src.config import settings

app = FastAPI(
    title=settings.app_name
)


# app.include_router(blog_router)


@app.get("/")
async def hello():
    return {"saluto": "ciao"}


@app.get("/auguri/{nome}")
async def auguri(nome):
    return {"AUGURI": nome}
