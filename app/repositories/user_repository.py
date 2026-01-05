from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User as UserModel
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel]):
    """
    Repository for User model.
    
    Handles all database operations for User entities.
    """
    
    def __init__(self):
        super().__init__(UserModel)
    
    async def get_by_user_id(
        self,
        db: AsyncSession,
        user_id: int
    ) -> UserModel:
        """
        Get user by user_id or raise exception if not found.
        
        Args:
            db: Database session
            user_id: The user ID to search for
            
        Returns:
            The User ORM model instance
            
        Raises:
            logic_exception: If user not found
        """
        return await self.get_by_id_or_raise(db, user_id, "user_id")

