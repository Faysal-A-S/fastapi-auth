from schemas import TodoIn, TodoDBIn, TodoUpdate
from sqlalchemy.orm import Session
from repositories import todo_repo
from services import BaseService
from models import ToDo


class TodoService(BaseService[ToDo, TodoIn, TodoUpdate]):

    def create_todo(self, db: Session, data_in: TodoIn, user_id: int):
        todo = self.create(
            db=db,
            data_in=TodoDBIn(
                **data_in.dict(), user_id=user_id
            )
        )

        return todo


todo_service = TodoService(ToDo, todo_repo)
