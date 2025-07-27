from pydantic import BaseModel

class Create_Blog(BaseModel):
    title: str
    body: str

class ShowBlog(Create_Blog):
    title: str
    body: str

    class Config():
        orm_mode = True

# create user

class CreateUser(BaseModel):
    username: str
    email: str
    password: str

class ShowUser(BaseModel):
    username: str
    email: str
    class Config():
        orm_mode = True
    
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
