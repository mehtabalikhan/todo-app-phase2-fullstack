from typing import List, Optional
from sqlmodel import select, Session, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from uuid import UUID
import uuid

from src.models.task import Task, TaskCreate, TaskUpdate
from src.models.user import User
from src.auth.exceptions import ResourceNotFoundException, InsufficientPermissionsException


class TaskService:
    """Service class for handling task-related business logic with user-based filtering"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_task(self, task_create: TaskCreate, current_user_id: UUID) -> Task:
        """
        Create a new task for the current user.
        Ensures that the task is associated with the current user.
        """
        # Validate that the task is being created for the current user
        if str(task_create.user_id) != str(current_user_id):
            raise InsufficientPermissionsException(
                detail="Cannot create task for another user"
            )

        # Create the task object
        task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=task_create.completed,
            user_id=current_user_id
        )

        # Add to database
        self.db_session.add(task)
        await self.db_session.commit()
        await self.db_session.refresh(task)

        return task

    async def get_user_tasks(self, current_user_id: UUID, skip: int = 0, limit: int = 100) -> List[Task]:
        """
        Retrieve all tasks for the current user.
        This enforces user-based data filtering.
        """
        statement = (
            select(Task)
            .where(Task.user_id == current_user_id)
            .offset(skip)
            .limit(limit)
        )

        result = await self.db_session.execute(statement)
        tasks = result.scalars().all()
        return tasks

    async def get_task_by_id(self, task_id: UUID, current_user_id: UUID) -> Task:
        """
        Retrieve a specific task by ID for the current user.
        Validates that the task belongs to the current user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
        result = await self.db_session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ResourceNotFoundException(detail="Task not found or does not belong to user")

        return task

    async def update_task(self, task_id: UUID, task_update: TaskUpdate, current_user_id: UUID) -> Task:
        """
        Update a specific task for the current user.
        Validates that the task belongs to the current user.
        """
        # First get the task to ensure it exists and belongs to the user
        statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
        result = await self.db_session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ResourceNotFoundException(detail="Task not found or does not belong to user")

        # Update the task with provided values
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self.db_session.commit()
        await self.db_session.refresh(task)

        return task

    async def delete_task(self, task_id: UUID, current_user_id: UUID) -> bool:
        """
        Delete a specific task for the current user.
        Validates that the task belongs to the current user.
        """
        # First get the task to ensure it exists and belongs to the user
        statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
        result = await self.db_session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ResourceNotFoundException(detail="Task not found or does not belong to user")

        # Delete the task
        await self.db_session.delete(task)
        await self.db_session.commit()

        return True

    async def toggle_task_completion(self, task_id: UUID, current_user_id: UUID) -> Task:
        """
        Toggle the completion status of a specific task for the current user.
        Validates that the task belongs to the current user.
        """
        # First get the task to ensure it exists and belongs to the user
        statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
        result = await self.db_session.execute(statement)
        task = result.scalar_one_or_none()

        if not task:
            raise ResourceNotFoundException(detail="Task not found or does not belong to user")

        # Toggle the completion status
        task.completed = not task.completed

        await self.db_session.commit()
        await self.db_session.refresh(task)

        return task

    async def get_user_task_count(self, current_user_id: UUID) -> int:
        """
        Get the total count of tasks for the current user.
        """
        statement = select(func.count(Task.id)).where(Task.user_id == current_user_id)
        result = await self.db_session.execute(statement)
        count = result.scalar_one()
        return count