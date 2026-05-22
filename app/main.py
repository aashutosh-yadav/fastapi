from fastapi import FastAPI

from app import database

from .routers import auth, post, user, vote

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
# # this can be converted to hashtable for efficient searching algo
# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "favorite foos", "content": "I like pizza", "id": 2},
# ]


# to find a specific post
# we can optimize this with optimal search algo
# def find_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i
#
#
# def delete_pt(id):
#     for p in my_posts:
#         if p["id"] == id:
#             my_posts.remove(p)
#             return p
#     return None
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# first root route
@app.get("/")
def root():
    return {"message": "hey there buddy"}
