from fastapi import APIRouter, status, HTTPException, Response
import schemas, models, database
from hashing import Hash

router = APIRouter(
    tags=["Users"],
    prefix="/user"
)

@router.post('/create-user', response_model=schemas.ShowUser)
def create_user(db: database.db_dependency, new_user: schemas.CreateUser, response: Response):
    create_new_user = models.Create_User(
        username = new_user.username,
        email = new_user.email,
        password = Hash.bcrypt(new_user.password)
    )
    db.add(create_new_user)
    db.commit()
    response.status_code=status.HTTP_201_CREATED
    db.refresh(create_new_user)
    return create_new_user


@router.get('/get-user/{id}', response_model=schemas.ShowUser)
def get_user_id(id: int, db: database.db_dependency, response: Response):
    user_id = db.query(models.Create_User).filter(models.Create_User.id == id)
    user = user_id.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with id {id}")
    return user