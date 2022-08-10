from ast import Not, While
from gettext import find
import http
from turtle import pos
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time



app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        conn =  psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database successfully connected')
        break

    except Exception as error:
        print("Connecting to database failed")
        print("error", error)
        time.sleep(2)
        

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
    cursor.execute("""SELECT * FROM posts""")
    posts =  cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post('/posts')
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) values(%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    
    new_post = cursor.fetchone()
    conn.commit()
    
    return {"data":  new_post}



@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}



@app.get('/posts/{id}')
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    test_post = cursor.fetchone()
    print(test_post, type(id))
    #post = find_post(int(id))
    if not test_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return {"post_detail": test_post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT) #{'message': 'post with id {id} successfully deleted'}

@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s 
                   where id = %s returning *  """, 
                   (post.title, post.content, post.published, id))
    
    updated_post = cursor.fetchall()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    return {"a": updated_post}
   
    