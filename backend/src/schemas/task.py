from pydantic import BaseModel, validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

    @validator('title')
    def title_must_not_be_empty(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title must not be empty')
        if len(v) > 255:
            raise ValueError('Title must be at most 255 characters')
        return v

    @validator('description')
    def description_max_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be at most 1000 characters')
        return v


class TaskCreate(TaskBase):
    user_id: UUID
    title: str  # Required field

    class Config:
        schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Need to buy milk, bread, and eggs",
                "completed": False,
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    @validator('title')
    def title_max_length(cls, v):
        if v and len(v) > 255:
            raise ValueError('Title must be at most 255 characters')
        return v

    @validator('description')
    def description_max_length(cls, v):
        if v and len(v) > 1000:
            raise ValueError('Description must be at most 1000 characters')
        return v


class TaskRead(TaskBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class TaskToggleComplete(BaseModel):
    completed: Optional[bool] = None


class TaskToggleResponse(BaseModel):
    id: UUID
    completed: bool
    updated_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "completed": True,
                "updated_at": "2026-01-28T10:00:00Z"
            }
        }


class TaskListResponse(BaseModel):
    tasks: list[TaskRead]
    total_count: int

    class Config:
        schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Buy groceries",
                        "description": "Need to buy milk, bread, and eggs",
                        "completed": False,
                        "user_id": "987e6543-e21b-32d1-c876-426614174999",
                        "created_at": "2026-01-28T10:00:00Z",
                        "updated_at": "2026-01-28T10:00:00Z"
                    }
                ],
                "total_count": 1
            }
        }


class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    timestamp: str

    class Config:
        schema_extra = {
            "example": {
                "detail": "Invalid authentication credentials",
                "error_code": "AUTH_001",
                "timestamp": "2026-01-28T10:00:00Z"
            }
        }