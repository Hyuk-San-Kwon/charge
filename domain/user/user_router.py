from datetime import timedelta, datetime

from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from models import User
from database import get_db
from domain.user import user_crud, user_schema


ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24
SECRET_KEY = "3a6a54dbd17251738203ab4e2cfcaa5503ffed2400dbc5a2357620ca4a17fcc7"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")
router = APIRouter(
    prefix="/api/user",
)


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user

# 회원가입한 내용을 디비에 보내는 것까지 역할 #############################################################
@router.post("/signup", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: user_schema.UserCreate, db: Session = Depends(get_db)):
    user = user_crud.get_existing_user(db, user_create=_user_create)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db=db, user_create=_user_create)
    
