from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.security import get_token_user_uuid
from app.core.responses import JSendRoute
from uuid import UUID
from app.schemas.user import UserCreate, UserResponse
from app.services.user import User


router = APIRouter(route_class=JSendRoute)
user_service = User()


@router.post("/", response_model=UserResponse)
async def create_user_endpoint(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    actor_name : UUID = Depends(get_token_user_uuid)
) -> UserResponse:
    """
    Create a new user.
    
    Transaction is committed in the service layer.
    FastAPI dependency will handle rollback on exception.
    """
    return await user_service.create(db, user_in, actor_name)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_endpoint(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Get a user by ID.
    """
    return await user_service.get(db, user_id)

