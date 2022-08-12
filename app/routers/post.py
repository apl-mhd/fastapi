from .. database_con import get_db, conn, cursor
from sqlalchemy.orm import Session
from fastapi import Depends, status, HTTPException, Response, APIRouter
from .. import models
from .. import schemas



router = APIRouter()



@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post


@router.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
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

@router.put('/posts/{id}')
def update_post(id:int, post:schemas.Post):
    
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s 
                   where id = %s returning *  """, 
                   (post.title, post.content, post.published, id))
    updated_post = cursor.fetchall()
    conn.commit()
    
    if not updated_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    
    return updated_post