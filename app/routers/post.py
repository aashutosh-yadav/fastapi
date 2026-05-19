from typing import List, Optional

from fastapi import (
    APIRouter,
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status,  # here  FastAPI is the main class in fastapi and is the entry point .
)
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.util.deprecations import deprecated

from app import oauth2

from .. import models, schemas , oauth2
from ..database import engine, get_db

models.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def creat_post(post: schemas.PostCreate, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #    "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #    (post.title, post.content, post.published),
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.email)
    new_post = models.Post(  # -> this is for efficiency
        **post.model_dump()
    )
    # new_post = models.Post(title=post.title , content=post.content , published=post.published) # create new post  -> this is slow
    db.add(new_post)  # add it to the database
    db.commit()  # commit the changes
    db.refresh(new_post)  # retrive the data  and strore is in the new variable new_post
    return new_post


# def creat_post(payload : dict = Body(...)):
#     print(payload)
#     return {
#         "new_message" : f"title : {payload["title"]}, content : {payload["content"]}"
#         }


@router.get("/{id}" , response_model=schemas.Post)  # path parameter
def get_post(id: int, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id :{id} was not found ",
        )
        # response.status_code = status.HTTP_404_NOT_FOUND
    # return {"message": f"post with id :{id} was not found "}
    return {"post": post}


# delete method
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    # post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )

    db.delete(post)
    db.commit()

    return {"message": "deleted sucessfully"}


#
# @app.put("/posts/{id}")
# def update_post(id: int,post: Post,db: Session = Depends(get_db)):
#     # cursor.execute(
#     #     """UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING *""",
#     #     (post.title, post.content, post.published, id),
#     # )
#     # updated_post = cursor.fetchone()
#     # conn.commit()  # anytime you want to make changes to the databae we need to add this line
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()
#     if not post:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
#         )
#     post_query.update(post.model_dump(),synchronize_session=False)
#     return {"data": post_query.first()}


@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db) , current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = (
        post_query.first()
    )  # here existing_post post  is the post that already exist int he database

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )

    post_query.update(post.model_dump(), synchronize_session=False)

    db.commit()

    return {"data": post_query.first()}
