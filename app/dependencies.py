from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError
import logging
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.settings import Settings
oauth2scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")
settings=Settings()
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
logger=logging.getLogger(__name__)
def get_current_user(token:str=Depends(oauth2scheme),db:Session=Depends(get_db)):
    common_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong authorization",
        headers={"WWW:Authenticate":"Bearer"}
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=payload.get("sub")
        if not user_id:
            logger.error(f"Couldnt get id from token")
            raise common_exception
    except JWTError:
        logger.error(f"Token error:jwt ERROR")
        raise common_exception
    db_user=db.query(User).filter(user_id==User.id).first()
    if not db_user:
        logger.error(f"User {db_user.email} not found")
        raise common_exception
    if not db_user.is_active:
        logger.error(f"User {db_user.email} inactive")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Inaactive user")
    return db_user
def require_admin(current_user:User=Depends(get_current_user)):
    if current_user.role!="admin":
        logger.error(f"User {current_user.email} havent access admin!")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Admin role reqiured!")
    return current_user
