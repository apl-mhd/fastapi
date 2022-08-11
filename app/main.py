from multiprocessing import synchronize
from re import I
from turtle import pos, title
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends   
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
#from database import engine, session_local
from . database_con import engine, session_local
from sqlalchemy.orm import Session
from . import models 
from . schemas import Post

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
   # rating: Optional[int] = None

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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts =  db.query(models.Post).all()
    
    return {"status": posts}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.post('/posts')
def create_posts(post: Post,db: Session = Depends(get_db), ):
    # cursor.execute(""" INSERT INTO posts (title, content, published) values(%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    
    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data":  new_post}
    
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return post



@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # test_post = cursor.fetchone()
    # print(test_post, type(id))
    #post = find_post(int(id))
    # if not test_post:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    # return {"post_detail": test_post}
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    return post



@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post =  db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post.delete(synchronize_session = False)
    db.commit()
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
    
    return updated_post
   
@app.post('/users')
def create_user():
    pass
    
    