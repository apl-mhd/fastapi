from datetime import datetime
from pydantic import BaseModel, EmailStr

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
    email: EmailStr
    password: str
    

class UserOut(BaseModel):
    id: int
    email: EmailStr
    password: str
    created_at: datetime
    
    
    
    class Config():
        orm_mode = True
    
    
    