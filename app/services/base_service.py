from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Any
from app.core.exceptions import logic_exception
from app.core.error_codes import ErrorCodes


class BaseService:
    def __init__(self, model, response_schema):
        self.model = model
        self.response_schema = response_schema
    
    async def get_by_id(self, db: AsyncSession, id_value: int, id_field_name: str = "id", not_found_message: str = None):
        id_column = getattr(self.model, id_field_name)
        result = await db.execute(select(self.model).where(id_column == id_value))
        db_obj = result.scalar_one_or_none()
        
        if not db_obj:
            message = not_found_message or f"{self.model.__name__} with {id_field_name} {id_value} not found"
            raise logic_exception(code=ErrorCodes.not_found, message=message, status_code=404)
        
        return db_obj
    
    async def create(self, db: AsyncSession, create_schema, actor_name: str, **kwargs):
        schema_dict = create_schema.model_dump(exclude_none=True)
        schema_dict.update({'created_by': actor_name, 'updated_by': actor_name, **kwargs})
        
        db_obj = self.model(**schema_dict)
        db.add(db_obj)
        await db.flush()
        
        data = {}
        for field_name in self.response_schema.model_fields.keys():
            value = getattr(db_obj, field_name, None)
            if hasattr(value, 'isoformat'):
                value = value.isoformat()
            elif hasattr(value, 'value'):
                value = value.value
            data[field_name] = value
        return self.response_schema(**data)
    
    async def check_exists(self, db: AsyncSession, field_name: str, field_value: Any, error_code: str = ErrorCodes.user_exists, error_message: str = None, status_code: int = 400):
        field_column = getattr(self.model, field_name)
        result = await db.execute(select(self.model).where(field_column == field_value))
        existing = result.scalar_one_or_none()
        
        if existing:
            message = error_message or f"{self.model.__name__} with {field_name} {field_value} already exists"
            raise logic_exception(code=error_code, message=message, status_code=status_code)
