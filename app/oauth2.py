from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models, schemas
from .config import settings
from .database import get_db

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

oauth2_scheme = OAuth2PasswordBearer('login')

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # noqa: UP017
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id") if payload is not None else None # type: ignore
        
        if id is None:
            raise credentials_exception
        token_data: schemas.TokenData = schemas.TokenData(id = int(id))
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], 
                     db: Annotated[Session, Depends(get_db)]
                    ) -> models.User | None:
    
    credentials_exception = HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                        detail="Could not validate credentials",
                                        headers={"WWW-Authenticate": "Bearer"})
    
    access_token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == access_token.id).first()
    
    return user
