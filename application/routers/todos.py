from fastapi import Depends,APIRouter,HTTPException,status,Request
from application.schemas import TodoCreate,TodoResponse,UserResponse,TodoUpdate
from sqlalchemy.orm import Session
from application.database import get_db
from application.models import User,Todo
from typing import List
from application.limiter import limiter
from application.dependencies import get_current_user,require_admin
import logging
router=APIRouter(
    tags=["Todos"],
    prefix="/todos"
)
logger=logging.getLogger(__name__)
@router.get("/",response_model=List[TodoResponse])  
@limiter.limit("100/minute")
def get_todos(request:Request,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    todos=db.query(Todo).filter(Todo.owner_id==current_user.id).all()
    return todos
@router.post("/",status_code=201,response_model=TodoResponse)
@limiter.limit("30/minutes")
def create_todo(request:Request,todo:TodoCreate,current_user:UserResponse=Depends(get_current_user),db:Session=Depends(get_db)):
    new_todo=Todo(**todo.model_dump(),owner_id=current_user.id)
    db.add(new_todo)
    db.commit()
    return new_todo
@router.patch("/{id}")
def update_todo(id:int,todo:TodoUpdate,current_user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    db_todo=db.query(Todo).filter(Todo.id==id).first()
    if not db_todo:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo {id} not found")
    if db_todo.owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not your todo")
    for key,value in todo.model_dump(exclude_none=True).items():
         setattr(db_todo,key,value)
    db.add(db_todo)
    db.commit()
    return db_todo
@router.delete("/{id}",status_code=204)
def delete_todo(id:int,current_user:UserResponse=Depends(get_current_user),db:Session=Depends(get_db)):
    todo=db.query(Todo).filter(Todo.id==id).first()
    if not todo:
        logger.error(f"Todo not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Todo not found")
    if todo.owner_id!=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not your todo")
    db.delete(todo)
    db.commit()
@router.get("/all",response_model=list[TodoResponse])
def get_all_todo(admin:User=Depends(require_admin),db:Session=Depends(get_db)):
    todos=db.query(Todo).all()
    return todos

