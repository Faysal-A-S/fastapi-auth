from fastapi import APIRouter, Depends
from api.v1.auth_deps import logged_in
from schemas import TodoIn, TodoOut, TodoOutUser, TodoUpdate, ResultIn
from exceptions import handle_result
from sqlalchemy.orm import Session
from db import get_db
from typing import List, Union
from services import todo_service

router = APIRouter()


@router.get('/', response_model=List[Union[ResultIn, List[TodoOut]]])
def all_todo(skip: int = 0, limit: int = 10,  db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    all = todo_service.get_with_pagination(
        db=db, skip=skip, limit=limit, descending=True, count_results=True)
    return handle_result(all)


@router.post('/', response_model=TodoOut)
def create_todo(data_in: TodoIn, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    todo = todo_service.create_todo(
        db=db, data_in=data_in, user_id=current_user.id)
    return handle_result(todo)


@router.get('/user-todo/', response_model=List[Union[ResultIn, List[TodoOutUser]]])
def user_todo(skip: int = 0, limit: int = 10,  db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    user_id = current_user.id
    all = todo_service.get_by_key(
        db=db, skip=skip, limit=limit, descending=True, count_results=True, user_id=user_id)
    return handle_result(all)


@router.get('/{id}', response_model=TodoOut)
def get_one(id, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    todo = todo_service.get_one(db, id)
    return handle_result(todo)


@router.put('/{id}', response_model=TodoOut)
def update_todo(id: int, todo_update: TodoUpdate, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    update = todo_service.update(db, id, data_update=todo_update)
    return handle_result(update)


@router.delete('/{id}')
def delete_todo(id: int, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    delete = todo_service.delete(db, id=id)
    return handle_result(delete)
