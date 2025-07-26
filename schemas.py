from pydantic import BaseModel

class Create_Blog(BaseModel):
    title: str
    body: str