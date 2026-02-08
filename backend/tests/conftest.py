import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from unittest.mock import AsyncMock

from src.app.main import app
from src.database.engine import engine, AsyncSessionLocal
from src.models.user import User
from src.models.task import Task


@pytest.fixture(scope="module")
def client():
    """Create a test client for the FastAPI app"""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
async def async_session():
    """Create an async database session for testing"""
    # Use an in-memory SQLite database for testing
    test_engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session_local = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_local() as session:
        yield session

    await test_engine.dispose()