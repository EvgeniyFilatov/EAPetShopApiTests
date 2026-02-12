"""JSON схемы для валидации ответов API

Схемы соответствуют спецификации OpenAPI (Swagger) PetStore
"""

from .pet_schema import PET_SCHEMA
from .store_schema import STORE_SCHEMA, INVENTORY_SCHEMA

__all__ = ['PET_SCHEMA', 'STORE_SCHEMA', 'INVENTORY_SCHEMA']