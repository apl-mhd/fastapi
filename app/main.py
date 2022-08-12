
from fastapi import FastAPI
from passlib.context import CryptContext
from . database_con import engine
from . import models 
from . routers import post, user
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
   
@app.get('/')
def root():
    return {"message": "hello world"}


    
    