from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import Student as StudentModel
from app.schemas.student import StudentCreate, StudentResponse
from app.services.base_service import BaseService
from app.services.user import User as UserService
from app.core.exceptions import logic_exception
from app.core.error_codes import ErrorCodes


class Student(BaseService):
    """
    Student service class with student-specific business logic.
    """
    
    def __init__(self):
        super().__init__(StudentModel, StudentResponse)
        self.user_service = UserService()
    
    async def create(
        self,
        db: AsyncSession,
        student_schema: StudentCreate,
        actor_name: str
    ) -> StudentResponse:
        """
        Creates a new student with user validation.
        """
        # Verify user exists (this will raise if not found)
        await self.user_service.get(db, student_schema.user_id)
        
        # Check if student already exists for this user
        await self.check_exists(
            db,
            "user_id",
            student_schema.user_id,
            ErrorCodes.user_exists,
            f"Student already exists for user ID {student_schema.user_id}"
        )
        
        # Use base create method
        return await super().create(db, student_schema, actor_name)
    
    async def get(self, db: AsyncSession, student_id: int) -> StudentResponse:
        """
        Get student by ID.
        """
        db_student = await self.get_by_id(db, student_id, "student_id", f"Student with ID {student_id} not found")
        
        data = {}
        for field_name in self.response_schema.model_fields.keys():
            value = getattr(db_student, field_name, None)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            elif hasattr(value, 'value'):
                value = value.value
            data[field_name] = value
        return self.response_schema(**data)

