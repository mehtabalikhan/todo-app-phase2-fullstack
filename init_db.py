#!/usr/bin/env python3
"""
Script to initialize the database tables
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the path so we can import our models
sys.path.append(str(Path(__file__).parent / "backend"))

# Import after adding to path
from sqlmodel import SQLModel
from src.database.engine import engine
from src.models.user import User
from src.models.task import Task

async def create_tables():
    """Create all database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Database tables created successfully!")

if __name__ == "__main__":
    asyncio.run(create_tables())