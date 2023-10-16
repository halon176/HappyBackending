from fastapi import APIRouter
from src.blog.schemas import Post
from src.databese import posts

router = APIRouter(
    prefix="/blog",
    tags=["Blog"]
)


@router.get("/post")
async def get_post(id_post: int = 1):
    for post in posts:
        if post["id"] == id_post:
            return post


@router.post("/post", response_model=list[Post])
async def create_post(content: Post):
    posts.append(content)
    return posts
