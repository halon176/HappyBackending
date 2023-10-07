from fastapi import FastAPI

from pydantic import BaseModel, Field

app = FastAPI()


@app.get("/")
async def hello():
    return {"saluto": "ciao"}


@app.get("/auguri/{nome}")
async def auguri(nome):
    return {"AUGURI": nome}


posts = [
    {"id": 1, "title": "Post 1", "content": "Oggi è una bella giornata"},
    {"id": 2, "title": "Post 2", "content": "Oggi il sole spende come non è mai spleso"},
    {"id": 3, "title": "Post 3", "content": "Oggi invece non splende più perché ieri è splenduto troppo"},
]


@app.get("/post")
async def get_post(id_post: int = 1):
    for post in posts:
        if post["id"] == id_post:
            return post


class Post(BaseModel):
    id: int = Field(..., gt=1, lt=100, examples=[1])
    title: str = Field(..., max_length=100, examples=["Titolo del post"])
    content: str = Field(..., examples=["Contenuto del post"])


@app.post("/post", response_model=list[Post])
async def create_post(content: Post):
    posts.append(content)
    return posts
