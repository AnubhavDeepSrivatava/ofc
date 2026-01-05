from fastapi import APIRouter
from app.api.v1.endpoints import batches, users, students, school_branches, schools

api_router = APIRouter()
api_router.include_router(batches.router, prefix="/batches", tags=["batches"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(school_branches.router, prefix="/school-branches", tags=["school-branches"])
api_router.include_router(schools.router, prefix="/schools", tags=["schools"])
