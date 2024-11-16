from fastapi import APIRouter, Depends
from api.v1.auth_deps import logged_in
from exceptions import handle_result
from schemas import TaskBase, TaskIn, TaskOut, ResultIn
from sqlalchemy.orm import Session
from db import get_db
from typing import List, Union
from services import task_service
router = APIRouter()


@router.get('/', response_model=List[TaskOut])
def all_task(db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    user_id = current_user.id
    all = task_service.get_tasks(db=db, current_user_id=user_id)
    return handle_result(all)


@router.post('/', response_model=TaskOut)
def create_task(data_in: TaskBase, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    task = task_service.create_task(
        db=db, data_in=data_in, user_id=current_user.id)
    return handle_result(task)


@router.get('/{id}', response_model=TaskOut)
def get_one(id, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    user_id = current_user.id
    task = task_service.get_one_task(db=db, current_user_id=user_id, id=id)
    return handle_result(task)


@router.delete('/{id}')
def delete_task(id: int, db: Session = Depends(get_db), current_user: Session = Depends(logged_in)):
    user_id = current_user.id
    delete = task_service.delete_task(db, id=id, current_user_id=user_id)
    return handle_result(delete)
