from fastapi import FastAPI, HTTPException, Depends, status, Response
from pydantic import BaseModel
import schemas, models, hashing
from typing import List, Annotated, Optional
from database import engine, get_db, db_dependency
from sqlalchemy.orm import Session
from hashing import Hash
from routers import blog, users, login
models.Base.metadata.create_all(bind=engine)



app = FastAPI(
    title = "My Blog Project",
    description= "This is the blog app"
)



app.include_router(blog.router)
app.include_router(users.router)
app.include_router(login.router)

# @app.post('/create-blog' , status_code=status.HTTP_201_CREATED)
# @app.post('/create-blog', tags=["Blog"])
# def create_blog(create_blog: schemas.Create_Blog, db: db_dependency, response: Response):
#     create_blog = models.Create_Blog(
#         title = create_blog.title,
#         body = create_blog.body
#     )
#     db.add(create_blog)
#     db.commit()
#     response.status_code = status.HTTP_201_CREATED
#     db.refresh(create_blog)

# @app.get('/get-blog', response_model=List[schemas.ShowBlog], tags=["Blog"])
# def get_blog(db: db_dependency):
#     blogs = db.query(models.Create_Blog).all()
#     return blogs
    
# @app.get('/get-blog/{id}', response_model=schemas.ShowBlog, tags=["Blog"])
# def get_blog_id(id: int, db: db_dependency, response: Response):
#     blog_id = db.query(models.Create_Blog).filter(models.Create_Blog.id == id).first()
#     if not blog_id:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Blog with the id {id} not found in the database.")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"detail" : f"Blog id with {id} not found."}
#     return blog_id

# @app.delete('/delete-blog/{id}', tags=["Blog"])
# def destroy(db: db_dependency, id: int, response: Response):
#     delete_blog = db.query(models.Create_Blog).filter(models.Create_Blog.id == id)
#     if not delete_blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} not found to get delete")
#     delete_blog.delete(synchronize_session=False)
#     db.commit()
#     response.status_code = status.HTTP_200_OK
#     return {"detail" : f"Blog id with {id} deleted from the database"}


# @app.put('/update-blog/{id}', tags=["Blog"])
# def update_blog(db: db_dependency, update_data: schemas.Create_Blog, id: int):
#     blog_query = db.query(models.Create_Blog).filter(models.Create_Blog.id == id)
#     blog = blog_query.first()
#     if not blog:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"No blog id {id} to update."
#         )
#     blog_query.update(update_data.model_dump(), synchronize_session=False)
#     db.commit()







# @app.post('/create-user', response_model=schemas.ShowUser, tags=["User"])
# def create_user(db: db_dependency, new_user: schemas.CreateUser, response: Response):
#     create_new_user = models.Create_User(
#         username = new_user.username,
#         email = new_user.email,
#         password = Hash.bcrypt(new_user.password)
#     )
#     db.add(create_new_user)
#     db.commit()
#     response.status_code=status.HTTP_201_CREATED
#     db.refresh(create_new_user)
#     return create_new_user


# @app.get('/get-user/{id}', response_model=schemas.ShowUser, tags=["User"])
# def get_user_id(id: int, db: db_dependency, response: Response):
#     user_id = db.query(models.Create_User).filter(models.Create_User.id == id)
#     user = user_id.first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with id {id}")
#     return user