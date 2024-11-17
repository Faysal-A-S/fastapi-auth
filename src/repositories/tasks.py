from repositories import BaseRepo
from schemas import TaskIn, TaskUpdate
from models import Task
from sqlalchemy.orm import Session


class TaskRepo(BaseRepo[Task, TaskIn, TaskUpdate]):

    def get_tasks(self, db: Session, current_user_id: int):
        query = db.query(self.model).filter(
            self.model.user_id == current_user_id).all()
        return query

    def get_one_task(self, db: Session, id: int):
        query = db.query(self.model).filter(self.model.id == id).first()
        return query

    def delete_task(self, db: Session, id: int):

        result = db.query(self.model).filter(self.model.id ==
                                             id).delete(synchronize_session=False)
        db.commit()
        return result


task_repo = TaskRepo(Task)
