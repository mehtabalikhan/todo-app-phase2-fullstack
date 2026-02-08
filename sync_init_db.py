#!/usr/bin/env python3
"""
Script to initialize the database tables synchronously
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlmodel import SQLModel, create_engine
from backend.src.models.user import User
from backend.src.models.task import Task

def create_tables_sync():
    """Create all database tables synchronously."""
    # Use synchronous SQLite engine
    DATABASE_URL = "sqlite:///./todo_app.db"
    sync_engine = create_engine(DATABASE_URL)

    # Import the models to make sure they're registered with SQLModel
    from backend.src.models.user import User
    from backend.src.models.task import Task

    # Create all tables
    SQLModel.metadata.create_all(sync_engine)
    print("Database tables created successfully with sync engine!")

if __name__ == "__main__":
    create_tables_sync()