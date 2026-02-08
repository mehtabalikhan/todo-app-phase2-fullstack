from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)


class User(UserBase, table=True):
    """
    User model representing an authenticated user in the system.
    Identified by a unique user ID extracted from JWT claims.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str = Field()
    name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")

    # Update updated_at before each update
    def __setattr__(self, name, value):
        if name == 'updated_at':
            # Allow explicit setting of updated_at
            super().__setattr__(name, value)
        elif name in ['email']:  # Add other fields that trigger updated_at
            super().__setattr__(name, value)
            super().__setattr__('updated_at', datetime.utcnow())
        else:
            super().__setattr__(name, value)


class UserRead(UserBase):
    """Schema for reading user data"""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime


class UserCreate(UserBase):
    """Schema for creating a new user"""
    email: str
    pass


class UserUpdate(SQLModel):
    """Schema for updating user data"""
    email: Optional[str] = None