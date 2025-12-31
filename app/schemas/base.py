from pydantic import BaseModel, model_validator, ConfigDict
from typing import Any
import re


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    @model_validator(mode='before')
    @classmethod
    def validate_name_fields(cls, data: Any):
        if isinstance(data, dict):
            for field_name, value in data.items():
                if 'name' in field_name.lower() and value is not None and isinstance(value, str):
                    special_chars_pattern = r'[@#$%&*()\[\]{}|\\/<>?!~`^]'
                    if re.search(special_chars_pattern, value):
                        raise ValueError(f"{field_name} cannot contain special characters")
        return data
