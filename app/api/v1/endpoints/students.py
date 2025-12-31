from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.security import get_token_user_name
from app.core.responses import JSendRoute
from app.schemas.student import StudentCreate, StudentResponse
from app.services.student import Student

router = APIRouter(route_class=JSendRoute)
student_service = Student()


@router.post("/", response_model=StudentResponse)
async def create_student_endpoint(
    student_in: StudentCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
) -> StudentResponse:
    """
    Create a new student.
    Transaction is handled automatically - commits on success, rolls back on exception.
    """
    try:
        result = await student_service.create(db, student_in, actor_name)
        await db.commit()
        return result
    except Exception:
        await db.rollback()
        raise


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student_endpoint(
    student_id: int,
    db: AsyncSession = Depends(get_db)
) -> StudentResponse:
    """
    Get a student by ID.
    """
    return await student_service.get(db, student_id)

