from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.core.security import get_token_user_uuid
from app.core.responses import JSendRoute
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student import Student

router = APIRouter(
    prefix="/students",
    tags=["Students"],
    route_class=JSendRoute
)

student_service = Student()


@router.post("/", response_model=StudentResponse)
async def create_student(
    student_in: StudentCreate,
    db: AsyncSession = Depends(get_db),
    actor_id: UUID = Depends(get_token_user_uuid)
):
    return await student_service.create(db, student_in, actor_id)


@router.get("/{user_id}", response_model=StudentResponse)
async def get_student(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    return await student_service.get(db, user_id)
