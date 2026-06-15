from pydantic import Field,BaseModel,ConfigDict
from typing import Optional
class UserCreate(BaseModel):
    email:str
    password:str=Field(min_length=8)
class TodoResponse(BaseModel):
    id:int
    title:str
    description:Optional[str]=None
    is_done:bool
    model_config=ConfigDict(from_attributes=True)
class UserResponse(BaseModel):
    id:int
    email:str
    role:str
    is_active:bool
    todos:list[TodoResponse]
    model_config=ConfigDict(from_attributes=True)
class TodoCreate(BaseModel):
    title:str=Field(min_length=2,max_length=500)
    description:Optional[str]=None
class TokenResponse(BaseModel):
    access_token:str
    token_type:str="bearer"
class TodoUpdate(BaseModel):
    title:Optional[str]=None
    description:Optional[str]=None