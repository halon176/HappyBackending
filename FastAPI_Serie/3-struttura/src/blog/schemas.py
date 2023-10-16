from pydantic import BaseModel, Field


class Post(BaseModel):
    id: int = Field(..., gt=1, lt=100, examples=[1])
    title: str = Field(..., max_length=100, examples=["Titolo del post"])
    content: str = Field(..., examples=["Contenuto del post"])
