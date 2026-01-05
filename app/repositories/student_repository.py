from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import Student as StudentModel
from app.repositories.base_repository import BaseRepository
from uuid import UUID   

class StudentRepository(BaseRepository[StudentModel]):
    """
    Repository for Student model.
    
    Handles all database operations for Student entities.
    """
    
    def __init__(self):
        super().__init__(StudentModel)
    
    async def get_by_student_id(
        self,
        db: AsyncSession,
        student_id: UUID
    ) -> StudentModel:
        """
        Get student by student_id or raise exception if not found.
        
        Args:
            db: Database session
            student_id: The student ID to search for
            
        Returns:
            The Student ORM model instance
            
        Raises:
            logic_exception: If student not found
        """
        return await self.get_by_id_or_raise(db, student_id, "student_id")

