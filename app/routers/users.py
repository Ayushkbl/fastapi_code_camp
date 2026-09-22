from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
    
    # print(f"password : {user.password}\tpassword length: {len(user.password)}")
    # print(f"password length: {len(user.password)}")
    # print(f"password bytes: {len(user.password.encode('utf-8'))}")  

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/{id}', response_model=schemas.UserResponse)
def get_user(id: int, db: Annotated[Session, Depends(get_db)]):
    
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"The user with id: {id} does not exist")
    
    return user