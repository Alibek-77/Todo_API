from app.database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__="users"
    id=Column(Integer,autoincrement=True,primary_key=True)
    email=Column(String,nullable=False,unique=True)
    hashed_password=Column(String,nullable=False)
    role=Column(String,default="user")
    is_active=Column(Boolean,default=True)
    todos=relationship("Todo",back_populates="owner")
class Todo(Base):
    __tablename__="todos"
    id=Column(Integer,primary_key=True,autoincrement=True)
    title=Column(String(250),nullable=False)
    description=Column(String(500))
    is_done=Column(Boolean,default=False)
    owner_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    owner=relationship("User",back_populates="todos")