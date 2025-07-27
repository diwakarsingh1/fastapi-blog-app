from fastapi import FastAPI, HTTPException, Depends, status, Response
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

# @app.post('/create-blog' , status_code=status.HTTP_201_CREATED)
@app.post('/create-blog')
def create_blog(create_blog: schemas.Create_Blog, db: db_dependency, response: Response):
    create_blog = models.Create_Blog(
        title = create_blog.title,
        body = create_blog.body
    )
    db.add(create_blog)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    db.refresh(create_blog)

@app.get('/get-blog')
def get_blog(db: db_dependency):
    blogs = db.query(models.Create_Blog).all()
    return blogs
    
@app.get('/get-blog/{id}')
def get_blog_id(id: int, db: db_dependency, response: Response):
    blog_id = db.query(models.Create_Blog).filter(models.Create_Blog.id == id).first()
    if not blog_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found in the database.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail" : f"Blog id with {id} not found."}
    return blog_id

@app.delete('/delete-blog/{id}')
def destroy(db: db_dependency, id: int, response: Response):
    delete_blog = db.query(models.Create_Blog).filter(models.Create_Blog.id == id)
    if not delete_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} not found to get delete")
    delete_blog.delete(synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return {"detail" : f"Blog id with {id} deleted from the database"}


