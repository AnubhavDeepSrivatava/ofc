from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.school_branch import SchoolBranchCreate, SchoolBranchResponse
from app.repositories.school_branch_repository import SchoolBranchRepository
from app.services.utils import orm_to_pydantic


class SchoolBranch:
    """
    SchoolBranch service class with school branch-specific business logic.
    
    This layer handles:
    - Business logic validation
    - Pydantic to Dictionary conversion
    - Transaction management (commit)
    - ORM to Pydantic response conversion
    """
    
    def __init__(self):
        self.repository = SchoolBranchRepository()
    
    async def create(
        self,
        db: AsyncSession,
        branch_schema: SchoolBranchCreate,
        actor_name: UUID
    ) -> SchoolBranchResponse:
        """
        Creates a new school branch.
        
        Args:
            db: Database session
            branch_schema: Pydantic schema with school branch creation data
            actor_name: UUID of the user performing the action
            
        Returns:
            SchoolBranchResponse: Pydantic response schema
        """
        # Transform: Pydantic → Dictionary
        data = branch_schema.model_dump(exclude_none=True)
        
        # Repository: Dictionary → ORM (with flush)
        db_branch = await self.repository.create(db, data, actor_name)
        
        # Commit transaction (permanent save)
        await db.commit()
        
        # Transform: ORM → Pydantic Response
        return orm_to_pydantic(db_branch, SchoolBranchResponse)
    
    async def get(self, db: AsyncSession, branch_id: UUID) -> SchoolBranchResponse:
        """
        Get school branch by ID.
        
        Args:
            db: Database session
            branch_id: The branch UUID to retrieve
            
        Returns:
            SchoolBranchResponse: Pydantic response schema
            
        Raises:
            logic_exception: If branch not found
        """
        # Repository: Get ORM object
        db_branch = await self.repository.get_by_branch_id(db, branch_id)
        
        # Transform: ORM → Pydantic Response
        return orm_to_pydantic(db_branch, SchoolBranchResponse)

