from fastapi import APIRouter
from app.api.v1.endpoints import batches, users, students

api_router = APIRouter()
api_router.include_router(batches.router, prefix="/batches", tags=["batches"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
