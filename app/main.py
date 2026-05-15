import time

# from random import randrange
# from typing import Optional
# import psycopg2
from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    Response,
    status,
)  # here  FastAPI is the main class in fastapi and is the entry point .
from psycopg2.extras import DictCursor

from fastapi.params import Body
from sqlalchemy.orm import Session

from . import models ,schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="postgres",
#             password="password123",
#             cursor_factory=DictCursor,
#         )  # the return object is usually a tuple but cursor_factory is used change it to a dictionary .
#         cursor = conn.cursor()
#         print("database connected")
#         break
#     except Exception as e:
#         print(f"database connection failed: {e}")
#         time.sleep(2)
#

# temporary database
# this can be converted to hashtable for efficient searching algo
my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "favorite foos", "content": "I like pizza", "id": 2},
]


# to find a specific post
# we can optimize this with optimal search algo
def find_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


def delete_pt(id):
    for p in my_posts:
        if p["id"] == id:
            my_posts.remove(p)
            return p
    return None


# first root route
@app.get("/")
def root():
    return {"message": "hey there buddy"}


@app.get("/posts")
def get_posts():
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def creat_post(post: schemas.PostCreate,db: Session = Depends(get_db)):
    #cursor.execute(
    #    "INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *",
    #    (post.title, post.content, post.published),
    #)
    #new_post = cursor.fetchone()
    #conn.commit()
    new_post = models.Post(            # -> this is for efficiency
        **post.model_dump()
    )
    #new_post = models.Post(title=post.title , content=post.content , published=post.published) # create new post  -> this is slow 
    db.add(new_post) # add it to the database 
    db.commit() # commit the changes 
    db.refresh(new_post) # retrive the data  and strore is in the new variable new_post
    return {"data": new_post}


# def creat_post(payload : dict = Body(...)):
#     print(payload)
#     return {
#         "new_message" : f"title : {payload["title"]}, content : {payload["content"]}"
#         }


@app.get("/post/{id}")  # path parameter
def get_post(id : int , db : Session = Depends(get_db)):
    #cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
    #post = cursor.fetchone()
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
@app.delete("/posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int, db : Session = Depends(get_db)):
    #cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (id,))
    #post = cursor.fetchone()
    #conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found"
        )

    db.delete(post)
    db.commit()

    return {"message" : "deleted sucessfully"}

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

@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    existing_post = post_query.first() # here existing_post post  is the post that already exist int he database 

    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found"
        )

    post_query.update(
        post.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return {"data": post_query.first()}
