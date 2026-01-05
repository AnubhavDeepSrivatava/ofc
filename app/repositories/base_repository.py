from typing import Generic, TypeVar, Type, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.exceptions import logic_exception
from app.core.error_codes import ErrorCodes
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """
    Base repository class providing common CRUD operations.
    
    This layer handles:
    - Dictionary to ORM model mapping
    - Database operations (add, flush)
    - Returns ORM objects (not Pydantic schemas)
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the repository with a SQLAlchemy model.
        
        Args:
            model: The SQLAlchemy model class
        """
        self.model = model
    
    async def get_by_id(
        self,
        db: AsyncSession,
        id_value: int,
        id_field_name: str = "id"
    ) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            db: Database session
            id_value: The ID value to search for
            id_field_name: Name of the ID field (default: "id")
            
        Returns:
            The ORM model instance or None if not found
        """
        id_column = getattr(self.model, id_field_name)
        result = await db.execute(select(self.model).where(id_column == id_value))
        return result.scalar_one_or_none()
    
    async def get_by_id_or_raise(
        self,
        db: AsyncSession,
        id_value: int,
        id_field_name: str = "id"
    ) -> ModelType:
        """
        Get a record by ID or raise exception if not found.
        
        Args:
            db: Database session
            id_value: The ID value to search for
            id_field_name: Name of the ID field (default: "id")
            
        Returns:
            The ORM model instance
            
        Raises:
            logic_exception: If record not found
        """
        db_obj = await self.get_by_id(db, id_value, id_field_name)
        if not db_obj:
            raise logic_exception(
                code=ErrorCodes.not_found,
                message=f"Record with {id_field_name} {id_value} not found",
                status_code=404
            )
        return db_obj
    
    async def create(
        self,
        db: AsyncSession,
        data: dict,
        actor_name: str
    ) -> ModelType:
        """
        Create a new record from a dictionary.
        
        This method:
        - Maps dictionary to ORM model
        - Adds created_by and updated_by fields
        - Executes db.add() and db.flush()
        - Returns the ORM object (with ID populated)
        
        Args:
            db: Database session
            data: Dictionary containing model fields
            actor_name: Name of the user performing the action
            
        Returns:
            The created ORM model instance (with ID populated after flush)
        """
        # Add audit fields
        data['created_by'] = actor_name
        data['updated_by'] = actor_name
        
        # Create database object from dictionary
        db_obj = self.model(**data)
        db.add(db_obj)
        await db.flush()  # Flush to get the ID, but don't commit yet
        
        return db_obj
    
    async def check_exists(
        self,
        db: AsyncSession,
        field_name: str,
        field_value: any
    ) -> bool:
        """
        Check if a record with given field value exists.
        
        Args:
            db: Database session
            field_name: Name of the field to check
            field_value: Value to check for
            
        Returns:
            True if record exists, False otherwise
        """
        field_column = getattr(self.model, field_name)
        result = await db.execute(select(self.model).where(field_column == field_value))
        return result.scalar_one_or_none() is not None
    
    async def check_exists_or_raise(
        self,
        db: AsyncSession,
        field_name: str,
        field_value: any,
        error_message: Optional[str] = None
    ) -> None:
        """
        Check if a record exists and raise exception if it does.
        
        Args:
            db: Database session
            field_name: Name of the field to check
            field_value: Value to check for
            error_message: Custom error message (optional)
            
        Raises:
            logic_exception: If record already exists
        """
        if await self.check_exists(db, field_name, field_value):
            message = error_message or f"Record with {field_name} {field_value} already exists"
            raise logic_exception(
                code=ErrorCodes.user_exists,
                message=message,
                status_code=400
            )

