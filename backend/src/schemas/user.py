from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID



class UserCreate(BaseModel):
    email: str
    password: str
    name: Optional[str] = None



class UserRead(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None