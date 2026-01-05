from typing import TypeVar, Type
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
SchemaType = TypeVar("SchemaType", bound=BaseModel)


def orm_to_pydantic(
    db_obj: ModelType,
    response_schema: Type[SchemaType]
) -> SchemaType:
    """
    Convert SQLAlchemy ORM model to Pydantic response schema.
    
    This function handles:
    - Extracting field values from ORM model
    - Converting datetime objects to ISO format strings
    - Converting enum values to strings
    - Creating Pydantic response schema instance
    - UUIDs are kept as UUID objects (Pydantic handles serialization)
    
    Args:
        db_obj: The SQLAlchemy ORM model instance
        response_schema: The Pydantic response schema class
        
    Returns:
        Pydantic response schema instance
    """
    data = {}
    for field_name in response_schema.model_fields.keys():
        value = getattr(db_obj, field_name, None)
        # Convert datetime to string
        if hasattr(value, 'isoformat'):
            value = value.isoformat()
        # Convert enum to string
        elif hasattr(value, 'value'):
            value = value.value
        # UUIDs are kept as-is, Pydantic will serialize them properly
        data[field_name] = value
    return response_schema(**data)

