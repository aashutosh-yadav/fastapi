from pydantic import BaseModel

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # if the user dosent provide a value it default prints True


class PostCreate(PostBase):
    pass
