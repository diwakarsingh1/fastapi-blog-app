from fastapi import APIRouter, Depends, Response, status, HTTPException
import schemas, models, database
from typing import List
import oauth2

router = APIRouter(
    tags=["Blog"],
    prefix="/blog"
)

@router.post('/create-blog')
def create_blog(create_blog: schemas.Create_Blog, db: database.db_dependency, response: Response, get_current_user: schemas.CreateUser = Depends(oauth2.get_current_user)):
    create_blog = models.Create_Blog(
        title = create_blog.title,
        body = create_blog.body
    )
    db.add(create_blog)
    db.commit()
    response.status_code = status.HTTP_201_CREATED
    db.refresh(create_blog)

@router.get('/get-blog', response_model=List[schemas.ShowBlog])
def get_blog(db: database.db_dependency, get_current_user: schemas.CreateUser = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Create_Blog).all()
    return blogs

@router.get('/get-blog/{id}', response_model=schemas.ShowBlog)
def get_blog_id(id: int, db: database.db_dependency, response: Response, get_current_user: schemas.CreateUser = Depends(oauth2.get_current_user)):
    blog_id = db.query(models.Create_Blog).filter(models.Create_Blog.id == id).first()
    if not blog_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found in the database.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail" : f"Blog id with {id} not found."}
    return blog_id

@router.delete('/delete-blog/{id}')
def destroy(db: database.db_dependency, id: int, response: Response, get_current_user: schemas.CreateUser = Depends(oauth2.get_current_user)):
    delete_blog = db.query(models.Create_Blog).filter(models.Create_Blog.id == id)
    if not delete_blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The blog with id {id} not found to get delete")
    delete_blog.delete(synchronize_session=False)
    db.commit()
    response.status_code = status.HTTP_200_OK
    return {"detail" : f"Blog id with {id} deleted from the database"}

@router.put('/update-blog/{id}')
def update_blog(db: database.db_dependency, update_data: schemas.Create_Blog, id: int, get_current_user: schemas.CreateUser = Depends(oauth2.get_current_user)):
    blog_query = db.query(models.Create_Blog).filter(models.Create_Blog.id == id)
    blog = blog_query.first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No blog id {id} to update."
        )
    blog_query.update(update_data.model_dump(), synchronize_session=False)
    db.commit()