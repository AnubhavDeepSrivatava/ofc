from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.student import StudentCreate, StudentResponse
from app.repositories.student_repository import StudentRepository
from app.services.user import User as UserService
from app.services.utils import orm_to_pydantic
from uuid import UUID

class Student:
    """
    Student service class with student-specific business logic.
    
    This layer handles:
    - Business logic validation
    - Pydantic to Dictionary conversion
    - Transaction management (commit)
    - ORM to Pydantic response conversion
    """
    
    def __init__(self):
        self.repository = StudentRepository()
        self.user_service = UserService()
    
    async def create(
        self,
        db: AsyncSession,
        student_schema: StudentCreate,
        actor_name: UUID             
    ) -> StudentResponse:
        """
        Creates a new student with user validation.
        
        Args:
            db: Database session
            student_schema: Pydantic schema with student creation data
            actor_name: Name of the user performing the action
            
        Returns:
            StudentResponse: Pydantic response schema
            
        Raises:
            logic_exception: If user doesn't exist or student already exists for user
        """
        # Business logic: Verify user exists (this will raise if not found)
        await self.user_service.get(db, student_schema.user_id)
        
        # Business logic: Check if student already exists for this user
        await self.repository.check_exists_or_raise(
            db,
            "user_id",
            student_schema.user_id
        )
        
        # Transform: Pydantic → Dictionary
        data = student_schema.model_dump(exclude_none=True)
        
        # Repository: Dictionary → ORM (with flush)
        db_student = await self.repository.create(db, data, actor_name)
        
        # Commit transaction (permanent save)
        await db.commit()
        
        # Transform: ORM → Pydantic Response
        return orm_to_pydantic(db_student, StudentResponse)
    
    async def get(self, db: AsyncSession, student_id: UUID) -> StudentResponse:
        """
        Get student by ID.
        
        Args:
            db: Database session
            student_id: The student ID to retrieve
            
        Returns:
            StudentResponse: Pydantic response schema
            
        Raises:
            logic_exception: If student not found
        """
        # Repository: Get ORM object
        db_student = await self.repository.get_by_student_id(db, student_id)
        
        # Transform: ORM → Pydantic Response
        return orm_to_pydantic(db_student, StudentResponse)

