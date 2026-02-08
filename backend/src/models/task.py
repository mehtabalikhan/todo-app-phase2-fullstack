from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    """
    Task model representing a personal task owned by a single user.
    Contains title, description, completion status, and timestamps.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")

    # Update updated_at before each update
    def __setattr__(self, name, value):
        if name == 'updated_at':
            # Allow explicit setting of updated_at
            super().__setattr__(name, value)
        elif name in ['title', 'description', 'completed']:  # Add other fields that trigger updated_at
            super().__setattr__(name, value)
            super().__setattr__('updated_at', datetime.utcnow())
        else:
            super().__setattr__(name, value)


class TaskRead(TaskBase):
    """Schema for reading task data"""
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    title: str
    user_id: uuid.UUID


class TaskUpdate(SQLModel):
    """Schema for updating task data"""
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskToggleComplete(SQLModel):
    """Schema for toggling task completion status"""
    completed: Optional[bool] = None