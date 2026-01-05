from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.school import SchoolCreate, SchoolResponse
from app.repositories.school_repository import SchoolRepository
from app.services.utils import orm_to_pydantic


class School:
    """
    School service class with school-specific business logic.
    
    This layer handles:
    - Business logic validation
    - Pydantic to Dictionary conversion
    - Transaction management (commit)
    - ORM to Pydantic response conversion
    """
    
    def __init__(self):
        self.repository = SchoolRepository()
    
    async def create(
        self,
        db: AsyncSession,
        school_schema: SchoolCreate,
        actor_name: UUID
    ) -> SchoolResponse:
        """
        Creates a new school.
        
        Args:
            db: Database session
            school_schema: Pydantic schema with school creation data
            actor_name: UUID of the user performing the action
            
        Returns:
            SchoolResponse: Pydantic response schema
        """
        # Transform: Pydantic → Dictionary
        data = school_schema.model_dump(exclude_none=True)
        
        # Repository: Dictionary → ORM (with flush)
        db_school = await self.repository.create(db, data, actor_name)
        
        # Commit transaction (permanent save)
        await db.commit()
        
        # Transform: ORM → Pydantic Response
        return orm_to_pydantic(db_school, SchoolResponse)
    
    async def get(self, db: AsyncSession, school_id: UUID) -> SchoolResponse:
        """
        Get school by ID.
        
        Args:
            db: Database session
            school_id: The school UUID to retrieve
            
        Returns:
            SchoolResponse: Pydantic response schema
            
        Raises:
            logic_exception: If school not found
        """
        # Repository: Get ORM object
        db_school = await self.repository.get_by_school_id(db, school_id)
        
        # Transform: ORM → Pydantic Response
        return orm_to_pydantic(db_school, SchoolResponse)

