from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.core.security import get_token_user_name
from app.core.responses import JSendRoute
from app.core.logging import get_logger
from app.schemas.user import UserCreate, UserResponse
from app.services.user import User

router = APIRouter(route_class=JSendRoute)
user_service = User()
logger = get_logger(__name__)


@router.post("/", response_model=UserResponse)
async def create_user_endpoint(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db),
    actor_name: str = Depends(get_token_user_name)
) -> UserResponse:
    logger.info(f"Creating user - actor: {actor_name}")
    try:
        result = await user_service.create(db, user_in, actor_name)
        await db.commit()
        logger.info(f"User created successfully - actor: {actor_name}")
        return result
    except Exception:
        await db.rollback()
        raise


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_endpoint(
    user_id: int,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    logger.info(f"Getting user - user_id: {user_id}")
    result = await user_service.get(db, user_id)
    logger.info(f"User retrieved successfully - user_id: {user_id}")
    return result

