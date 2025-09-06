from pydantic import BaseModel , EmailStr, ConfigDict, conint
from typing import Optional
from datetime import datetime


class User(BaseModel):
    email : EmailStr
    password : str

class UserBase(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime
    model_config = ConfigDict(from_attributes=True)


class CreatePost(BaseModel):
    title:str
    content: str
    publish: bool =True

class UpdatePosts(BaseModel):
    title : Optional[str] = None
    content : Optional[str] = None 
    publish : Optional[bool] = True 

class RespondPosts(UpdatePosts):
    id: int
    owner_id : int
    created_at : datetime
    owner: UserBase
    
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type : str

class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)


class ResponseOut(BaseModel):
    Posts : RespondPosts
    likes: int
    model_config = ConfigDict(from_attributes=True)