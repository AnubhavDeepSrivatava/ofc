from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.core.security import get_token_user_uuid
from app.core.responses import JSendRoute
from app.schemas.school import SchoolCreate, SchoolResponse
from app.services.school import School

router = APIRouter(
    tags=["Schools"],
    route_class=JSendRoute
)

school_service = School()


@router.post("/", response_model=SchoolResponse)
async def create_school(
    school_in: SchoolCreate,
    db: AsyncSession = Depends(get_db),
    actor_id: UUID = Depends(get_token_user_uuid)
) -> SchoolResponse:
    """
    Create a new school.
    
    Transaction is committed in the service layer.
    FastAPI dependency will handle rollback on exception.
    """
    return await school_service.create(db, school_in, actor_id)


@router.get("/{school_id}", response_model=SchoolResponse)
async def get_school(
    school_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> SchoolResponse:
    """
    Get a school by ID.
    """
    return await school_service.get(db, school_id)

