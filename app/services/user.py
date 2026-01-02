from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User as UserModel
from app.core.logging import get_logger
from app.schemas.user import UserCreate, UserResponse
from app.services.base_service import BaseService

logger = get_logger(__name__)


class User(BaseService):
    
    def __init__(self):
        super().__init__(UserModel, UserResponse)
    
    async def create(
        self,
        db: AsyncSession,
        user_schema: UserCreate,
        actor_name: str
    ) -> UserResponse:
        
        logger.info(f"Creating user - email: {user_schema.user_email}")
        await self.check_exists(db, "user_email", user_schema.user_email)
        
        
        result = await super().create(db, user_schema, actor_name)
        logger.info(f"User created - email: {user_schema.user_email}")
        return result
    
    async def get(self, db: AsyncSession, user_id: int) -> UserResponse:
        
        logger.info(f"Getting user - user_id: {user_id}")
        db_user = await self.get_by_id(db, user_id, "user_id")
        logger.info(f"User retrieved - user_id: {user_id}")
        return self._model_to_response(db_user)

