from services import BaseService
from repositories import task_repo
from models import Task
from schemas import TaskIn, TaskUpdate
from sqlalchemy.orm import Session
from exceptions import ServiceResult, AppException
from fastapi import status


class TaskService(BaseService[Task, TaskIn, TaskUpdate]):

    def create_task(self, db: Session, data_in: TaskIn, user_id: int):

        task = self.repo.create_task(db=db, data_in=data_in, user_id=user_id)

        if not task:
            return ServiceResult(AppException.ServerError("task not created!"))
        else:
            return ServiceResult(task, status_code=status.HTTP_201_CREATED)

    def get_tasks(self, db: Session, current_user_id: int):

        task = self.repo.get_tasks(db=db, current_user_id=current_user_id)

        if not task:
            task = []
        return ServiceResult(task, status_code=status.HTTP_200_OK)

    def get_one_task(self, db: Session, current_user_id: int, id: int):
        task = self.repo.get_one_task(
            db=db, current_user_id=current_user_id, id=id)

        if not task:
            return ServiceResult(AppException.NotFound(f"No tasks found."))
        if task.user_id == current_user_id:
            return ServiceResult(task, status_code=status.HTTP_200_OK)
        else:
            return ServiceResult(AppException.Unauthorized("Incorrect user"))

    def delete_task(self, db: Session, id: int, current_user_id: int,):
        task = self.repo.get_one_task(
            db=db, current_user_id=current_user_id, id=id)

        if task.user_id != current_user_id:
            return ServiceResult(AppException.Unauthorized("Incorrect user"))
        else:
            remove = self.repo.delete_task(
                db=db, current_user_id=current_user_id, id=id)
            if remove:
                return ServiceResult("Deleted", status_code=status.HTTP_202_ACCEPTED)
            return ServiceResult(AppException.Forbidden())


task_service = TaskService(Task, task_repo)
