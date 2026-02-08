from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from .engine import get_session as get_db_session


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get database session for dependency injection
    This is a wrapper around the engine's get_session function
    """
    async for session in get_db_session():
        try:
            yield session
        finally:
            await session.close()


# Convenience function to get session for direct use
async def get_direct_session() -> AsyncSession:
    """
    Get a direct database session without context management
    Remember to close the session when done
    """
    async for session in get_db_session():
        return session