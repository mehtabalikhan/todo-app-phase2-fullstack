from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

from src.models.user import User, UserCreate as UserCreateModel
from src.schemas.user import UserCreate

# Password hashing context - using pbkdf2 instead of bcrypt to avoid byte length issues
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by their email address."""
        result = await self.db.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        """Get a user by their ID."""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        return user

    async def verify_password(self, email: str, password: str) -> Optional[User]:
        """Verify user credentials."""
        user = await self.get_user_by_email(email)

        # Ensure password is not longer than 72 characters for bcrypt
        if len(password.encode('utf-8')) > 72:
            password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')

        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        return user

    async def create_user(self, user_create: UserCreate) -> User:
        """Create a new user."""
        try:
            # Ensure password is not longer than 72 characters for bcrypt
            password = user_create.password
            if len(password.encode('utf-8')) > 72:
                password = password[:72]  # Truncate to 72 characters

            # Hash the password with proper error handling
            try:
                hashed_password = pwd_context.hash(password)
            except ValueError as ve:
                # Handle bcrypt password length error
                if "password cannot be longer than 72 bytes" in str(ve):
                    # Ensure it's definitely under 72 bytes
                    password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
                    hashed_password = pwd_context.hash(password)
                else:
                    raise ve

            # Create a new user instance
            db_user = User(
                email=user_create.email,
                hashed_password=hashed_password,
                name=getattr(user_create, 'name', None)
            )

            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)

            return db_user
        except IntegrityError:
            # Handle case where user already exists
            await self.db.rollback()
            raise ValueError(f"User with email {user_create.email} already exists")
        except Exception as e:
            await self.db.rollback()
            raise e

    async def update_user(self, user_id: UUID, user_update: dict) -> Optional[User]:
        """Update a user's information."""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None

            # Update user attributes
            for key, value in user_update.items():
                setattr(user, key, value)

            await self.db.commit()
            await self.db.refresh(user)

            return user
        except Exception as e:
            await self.db.rollback()
            raise e

    async def delete_user(self, user_id: UUID) -> bool:
        """Delete a user."""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False

            await self.db.delete(user)
            await self.db.commit()

            return True
        except Exception as e:
            await self.db.rollback()
            raise e