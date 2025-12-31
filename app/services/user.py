from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User as UserModel
from app.schemas.user import UserCreate, UserResponse
from app.services.base_service import BaseService
from app.core.exceptions import logic_exception
from app.core.error_codes import ErrorCodes


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
        await self.check_exists(
            db,
            "user_email",
            user_schema.user_email,
            ErrorCodes.user_exists,
            f"User with email {user_schema.user_email} already exists"
        )
        
        # Use base create method
        return await super().create(db, user_schema, actor_name)
    
    async def get(self, db: AsyncSession, user_id: int) -> UserResponse:
        """
        Get user by ID.
        """
        db_user = await self.get_by_id(db, user_id, "user_id", f"User with ID {user_id} not found")
        
        data = {}
        for field_name in self.response_schema.model_fields.keys():
            value = getattr(db_user, field_name, None)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            elif hasattr(value, 'value'):
                value = value.value
            data[field_name] = value
        return self.response_schema(**data)

