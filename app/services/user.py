from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User as UserModel
from app.schemas.user import UserCreate, UserResponse
from app.services.base_service import BaseService


class User(BaseService):
    """
    User service class with user-specific business logic.
    """
    
    def __init__(self):
        super().__init__(UserModel, UserResponse)
    
    async def create(
        self,
        db: AsyncSession,
        user_schema: UserCreate,
        actor_name: str
    ) -> UserResponse:
        """
        Creates a new user with email uniqueness check.
        """
        # Check email uniqueness
        await self.check_exists(db, "user_email", user_schema.user_email)
        
        # Use base create method
        return await super().create(db, user_schema, actor_name)
    
    async def get(self, db: AsyncSession, user_id: int) -> UserResponse:
        """
        Get user by ID.
        """
        db_user = await self.get_by_id(db, user_id, "user_id")
        return self._model_to_response(db_user)

