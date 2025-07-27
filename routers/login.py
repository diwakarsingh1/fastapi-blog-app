from fastapi import APIRouter, HTTPException, status, Response, Depends
from fastapi.security import  OAuth2PasswordRequestForm
import schemas, database, models
from hashing import Hash
from  auth_token import create_access_token

# from .. import auth_token


router = APIRouter(
    tags=["Authentication"]
)

@router.post('/login', response_model=schemas.Token)
def login(db: database.db_dependency, request: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.Create_User).filter(models.Create_User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Username with {request.username} not found")
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect Password")   
    
    access_token = create_access_token(
        data={"sub": user.email}
        #expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
    # return {"message": "Login successful", "username": user.username, "email": user.email}

