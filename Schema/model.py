from typing import Optional
from pydantic import BaseModel


class Posts(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None

class User(BaseModel):
    name: str

class UpdatePost(BaseModel):
    title :Optional[str] = None
    content: Optional[str] = None
    