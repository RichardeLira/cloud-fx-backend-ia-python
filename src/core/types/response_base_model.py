from typing import Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class ApiResponse(GenericModel, Generic[T]):
    """
    A generic response schema for API responses.
    """
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    error: Optional[str] = None