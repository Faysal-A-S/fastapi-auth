from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    task: Optional[str] = None


class TaskIn(TaskBase):
    pass


class TaskDBIn(TaskBase):
    user_id: int


class TaskOut(TaskBase):
    user_id: int
    id: int

    class Config:
        orm_mode = True


class TaskOutUser(TaskBase):
    id: int

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    title: str
    task: Optional[str] = None
