import email
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    
    class Config():
        orm_mode = True
    
class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True
    
class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool
    

class UserCreate(BaseModel):
    
    email: str
    password: str
    