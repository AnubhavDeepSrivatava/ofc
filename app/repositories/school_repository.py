from sqlalchemy.ext.asyncio import AsyncSession
from app.models.school import School as SchoolModel
from app.repositories.base_repository import BaseRepository
from uuid import UUID


class SchoolRepository(BaseRepository[SchoolModel]):
    """
    Repository for School model.
    
    Handles all database operations for School entities.
    """
    
    def __init__(self):
        super().__init__(SchoolModel)
    
    async def get_by_school_id(
        self,
        db: AsyncSession,
        school_id: UUID
    ) -> SchoolModel:
        """
        Get school by school_id or raise exception if not found.
        
        Args:
            db: Database session
            school_id: The school ID to search for
            
        Returns:
            The School ORM model instance
            
        Raises:
            logic_exception: If school not found
        """
        return await self.get_by_id_or_raise(db, school_id, "id")

