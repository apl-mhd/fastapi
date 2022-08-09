from gettext import find
import http
from turtle import pos
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    

my_posts = [
    {'title': 'tile2', 'content': 'content1', 'id':1},
    {'title': 'tile2', 'content': 'content2', 'id':2}
    ]
    
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 
        

@app.get('/')
def root():
    return {"message": "hello world"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post('/createposts')
def create_posts(new_post: Post):
    post = new_post.dict()
    post['id'] = randrange(0,100000)
    my_posts.append(post)
    return {"data":  my_posts}



@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}



@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    post = find_post(int(id))
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"post_detail": post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT) #{'message': 'post with id {id} successfully deleted'}

@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    my_posts[index] = post
    
    return {"a": post}
   
    