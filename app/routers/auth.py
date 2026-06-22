from fastapi import Depends,APIRouter,HTTPException,status,Request
from app.auth import hash_password,create_token,verify_password
from app.schemas import UserCreate,UserResponse,TokenResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.limiter import limiter
from fastapi.security import OAuth2PasswordRequestForm
import logging
router=APIRouter(
    tags=["Authorization"],
    prefix="/auth"
)
logger=logging.getLogger(__name__)
@router.post("/register",response_model=UserResponse,status_code=201)
@limiter.limit("3/minute")
def registration(request:Request,user:UserCreate,db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if db_user:
        logger.error(f"User {user.email} has already registrated")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email has already taken")
    new_user=User(
        email=user.email,
        hashed_password=hash_password(user.password),
        role="user",
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"User {user.email} registrated!")
    return new_user
@router.post("/login",response_model=TokenResponse)
@limiter.limit("5/minute")
def login(request:Request,form_data:OAuth2PasswordRequestForm=Depends(),db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==form_data.username).first()
    if not db_user:
        logger.error(f"User {form_data.username} not found")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not found")
    if verify_password(form_data.password,db_user.hashed_password):
        token=create_token({"sub":str(db_user.id),"role":db_user.role})
        return {"access_token":token,"token_type":"bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong password or email!")