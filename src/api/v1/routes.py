from fastapi import APIRouter

from .endpoints import auth, todo, users, tasks

api_router = APIRouter()

# fmt: off
api_router.include_router(auth.router, prefix='', tags=['Auth'])
api_router.include_router(users.router, prefix='/users', tags=['Users'])
api_router.include_router(todo.router, prefix='/todo', tags=['Todos'])
api_router.include_router(tasks.router,prefix="/tasks",tags=["Tasks"])