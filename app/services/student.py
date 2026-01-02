from sqlalchemy.ext.asyncio import AsyncSession
from app.models.student import Student as StudentModel
from app.core.logging import get_logger
from app.schemas.student import StudentCreate, StudentResponse
from app.services.base_service import BaseService
from app.services.user import User as UserService
from app.core.exceptions import logic_exception
from app.core.error_codes import ErrorCodes

logger = get_logger(__name__)


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
        
        logger.info(f"Creating student - user_id: {student_schema.user_id}")
        await self.user_service.get(db, student_schema.user_id)
        await self.check_exists(db, "user_id", student_schema.user_id)
        result = await super().create(db, student_schema, actor_name)
        logger.info(f"Student created - user_id: {student_schema.user_id}")
        return result
    
    async def get(self, db: AsyncSession, student_id: int) -> StudentResponse:
        logger.info(f"Getting student - student_id: {student_id}")
        db_student = await self.get_by_id(db, student_id, "student_id")
        logger.info(f"Student retrieved - student_id: {student_id}")
        return self._model_to_response(db_student)

