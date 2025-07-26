from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import schemas, models
from typing import List, Annotated, Optional
from database import engine, SessionLocal
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
app = FastAPI()

@app.post('/create-blog')
def create_blog(create_blog: schemas.Create_Blog, db: db_dependency):
    create_blog = models.Create_Blog(
        title = create_blog.title,
        body = create_blog.body
    )
    db.add(create_blog)
    db.commit()
    db.refresh(create_blog)

@app.get('/get-blog')
def get_blog(db: db_dependency):
    blogs = db.query(models.Create_Blog).all()
    return blogs
    
@app.get('/get-blog/{id}')
def get_blog_id(id: int, db: db_dependency):
    blog_id = db.query(models.Create_Blog).filter(models.Create_Blog.id == id).first()
    return blog_id