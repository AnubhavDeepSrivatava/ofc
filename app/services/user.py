from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.repositories.user_repository import UserRepository
from app.services.utils import orm_to_pydantic


class User:
    """
    User service class with user-specific business logic.
    
    This layer handles:
    - Business logic validation
    - Pydantic to Dictionary conversion
    - Transaction management (commit)
    - ORM to Pydantic response conversion
    """
    
    def __init__(self):
        self.repository = UserRepository()
    
    async def create(
        self,
        db: AsyncSession,
        user_schema: UserCreate,
        actor_name: str
    ) -> UserResponse:
        """
        Creates a new user with email uniqueness check.
        
        Args:
            db: Database session
            user_schema: Pydantic schema with user creation data
            actor_name: Name of the user performing the action
            
        Returns:
            UserResponse: Pydantic response schema
            
        Raises:
            logic_exception: If email already exists
        """
        # Business logic: Check email uniqueness
        await self.repository.check_exists_or_raise(
            db,
            "user_email",
            user_schema.user_email
        )
        
        # Transform: Pydantic → Dictionary
        data = user_schema.model_dump(exclude_none=True)
        
        # Repository: Dictionary → ORM (with flush)
        db_user = await self.repository.create(db, data, actor_name)
        
        # Commit transaction (permanent save)
        await db.commit()
        
        # Transform: ORM → Pydantic Response
        return orm_to_pydantic(db_user, UserResponse)
    
    async def get(self, db: AsyncSession, user_id: int) -> UserResponse:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: The user ID to retrieve
            
        Returns:
            UserResponse: Pydantic response schema
            
        Raises:
            logic_exception: If user not found
        """
        # Repository: Get ORM object
        db_user = await self.repository.get_by_user_id(db, user_id)
        
        # Transform: ORM → Pydantic Response
        return orm_to_pydantic(db_user, UserResponse)

