from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.core.db import get_db
from app.core.security import get_token_user_uuid
from app.core.responses import JSendRoute
from app.schemas.school_branch import SchoolBranchCreate, SchoolBranchResponse
from app.services.school_branch import SchoolBranch

router = APIRouter(
    tags=["School Branches"],
    route_class=JSendRoute
)

school_branch_service = SchoolBranch()


@router.post("/", response_model=SchoolBranchResponse)
async def create_school_branch(
    branch_in: SchoolBranchCreate,
    db: AsyncSession = Depends(get_db),
    actor_id: UUID = Depends(get_token_user_uuid)
) -> SchoolBranchResponse:
    """
    Create a new school branch.
    
    Transaction is committed in the service layer.
    FastAPI dependency will handle rollback on exception.
    """
    return await school_branch_service.create(db, branch_in, actor_id)


@router.get("/{branch_id}", response_model=SchoolBranchResponse)
async def get_school_branch(
    branch_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> SchoolBranchResponse:
    """
    Get a school branch by ID.
    """
    return await school_branch_service.get(db, branch_id)

