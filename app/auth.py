from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timezone,timedelta
from settings import Settings
pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
settings=Settings()
SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_MINUTES=settings.access_token_minutes
def hash_password(password:str)->str:
    return pwd_context.hash(password)
def verify_password(plain:str,hashed:str)->bool:
    return pwd_context.verify(plain,hashed)
def create_token(data:dict):
    to_exp=data.copy()
    to_exp["exp"]=datetime.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_MINUTES))
    return jwt.encode(to_exp,SECRET_KEY,algorithm=ALGORITHM)