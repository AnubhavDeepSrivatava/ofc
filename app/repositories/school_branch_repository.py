from sqlalchemy.ext.asyncio import AsyncSession
from app.models.school_branch import SchoolBranch as SchoolBranchModel
from app.repositories.base_repository import BaseRepository
from uuid import UUID


class SchoolBranchRepository(BaseRepository[SchoolBranchModel]):
    """
    Repository for SchoolBranch model.
    
    Handles all database operations for SchoolBranch entities.
    """
    
    def __init__(self):
        super().__init__(SchoolBranchModel)
    
    async def get_by_branch_id(
        self,
        db: AsyncSession,
        branch_id: UUID
    ) -> SchoolBranchModel:
        """
        Get school branch by branch_id or raise exception if not found.
        
        Args:
            db: Database session
            branch_id: The branch ID to search for
            
        Returns:
            The SchoolBranch ORM model instance
            
        Raises:
            logic_exception: If branch not found
        """
        return await self.get_by_id_or_raise(db, branch_id, "id")

