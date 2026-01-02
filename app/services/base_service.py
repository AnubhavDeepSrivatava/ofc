from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.logging import get_logger
from app.core.exceptions import logic_exception
from app.core.error_codes import ErrorCodes

logger = get_logger(__name__)


class BaseService:
    def __init__(self, model, response_schema):
        self.model = model
        self.response_schema = response_schema
    
    async def get_by_id(self, db: AsyncSession, id_value: int, id_field_name: str = "id"):
        
        id_column = getattr(self.model, id_field_name)
        result = await db.execute(select(self.model).where(id_column == id_value))
        db_obj = result.scalar_one_or_none()
        
        if not db_obj:
            raise logic_exception(
                code=ErrorCodes.not_found,
                message=f"Record not found",
                status_code=404
            )
        
        return db_obj
    
    async def create(self, db: AsyncSession, create_schema, actor_name: str):
        logger.info(f"Creating {self.model.__name__} - actor: {actor_name}")
        data = create_schema.model_dump(exclude_none=True)
        
        data['created_by'] = actor_name
        data['updated_by'] = actor_name

        db_obj = self.model(**data)
        db.add(db_obj)
        await db.flush()
            
        result = self._model_to_response(db_obj)
        logger.info(f"{self.model.__name__} created successfully - actor: {actor_name}")
        return result
    
    def _model_to_response(self, db_obj):
        data = {}
        for field_name in self.response_schema.model_fields.keys():
            value = getattr(db_obj, field_name, None)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            elif hasattr(value, 'value'):
                value = value.value
            data[field_name] = value
        return self.response_schema(**data)
    
    async def check_exists(self, db: AsyncSession, field_name: str, field_value):
        
        field_column = getattr(self.model, field_name)
        result = await db.execute(select(self.model).where(field_column == field_value))
        existing = result.scalar_one_or_none()
        
        if existing:
            raise logic_exception(
                code=ErrorCodes.user_exists,
                message=f"User already exists",
                status_code=405
            )
