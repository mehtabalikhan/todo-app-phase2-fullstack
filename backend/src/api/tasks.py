from fastapi import APIRouter, Depends, HTTPException, status, Path, Body
from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_session
from src.services.task_service import TaskService
from src.auth.dependencies import get_current_user
from src.schemas.task import TaskCreate, TaskUpdate, TaskRead, TaskListResponse, TaskToggleResponse, ErrorResponse
from src.auth.exceptions import InvalidCredentialsException, InsufficientPermissionsException, ResourceNotFoundException
from src.utils.logging import log_security_event

router = APIRouter()

@router.get("/{user_id}/tasks", response_model=TaskListResponse, responses={
    401: {"model": ErrorResponse, "description": "Unauthorized - invalid or expired JWT"},
    403: {"model": ErrorResponse, "description": "Forbidden - user_id in URL doesn't match authenticated user"},
    404: {"model": ErrorResponse, "description": "Not Found - user does not exist"}
})
async def get_user_tasks(
    user_id: str = Path(..., description="User ID to retrieve tasks for"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve all tasks for the specified user.

    Returns a list of all tasks belonging to the specified user.
    The authenticated user must match the user_id in the URL.
    """
    authenticated_user_id = current_user["user_id"]

    # Verify that the authenticated user matches the requested user_id
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id in URL doesn't match authenticated user"
        )

    # Create task service instance
    task_service = TaskService(db)

    try:
        # Get user's tasks
        tasks = await task_service.get_user_tasks(UUID(user_id))

        # Get total count
        total_count = await task_service.get_user_task_count(UUID(user_id))

        # Prepare response
        task_list = [TaskRead.from_orm(task) if hasattr(TaskRead, 'from_orm') else
                     TaskRead(
                         id=task.id,
                         title=task.title,
                         description=task.description,
                         completed=task.completed,
                         user_id=str(task.user_id),
                         created_at=task.created_at,
                         updated_at=task.updated_at
                     ) for task in tasks]

        return TaskListResponse(tasks=task_list, total_count=total_count)

    except Exception as e:
        log_security_event("FAILED_TASK_RETRIEVAL", str(e), user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving tasks"
        )


@router.post("/{user_id}/tasks", response_model=TaskRead, responses={
    201: {"model": TaskRead, "description": "Task created successfully"},
    400: {"model": ErrorResponse, "description": "Bad Request - invalid input data"},
    401: {"model": ErrorResponse, "description": "Unauthorized - invalid or expired JWT"},
    403: {"model": ErrorResponse, "description": "Forbidden - user_id in URL doesn't match authenticated user"},
    422: {"model": ErrorResponse, "description": "Unprocessable Entity - validation errors"}
})
async def create_user_task(
    user_id: str = Path(..., description="User ID to create task for"),
    task_create: TaskCreate = Body(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Create a new task for the specified user.

    Creates a new task associated with the specified user.
    The authenticated user must match the user_id in the URL.
    """
    authenticated_user_id = current_user["user_id"]

    # Verify that the authenticated user matches the requested user_id
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id in URL doesn't match authenticated user"
        )

    # Verify that the task is being created for the correct user
    if str(task_create.user_id) != user_id:
        raise InsufficientPermissionsException(
            detail="Cannot create task for another user"
        )

    # Create task service instance
    task_service = TaskService(db)

    try:
        # Create the task
        task = await task_service.create_task(task_create, UUID(user_id))

        # Return the created task
        return TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        log_security_event("FAILED_TASK_CREATION", str(e), user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the task"
        )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskRead, responses={
    200: {"model": TaskRead, "description": "Successful response with the requested task"},
    401: {"model": ErrorResponse, "description": "Unauthorized - invalid or expired JWT"},
    403: {"model": ErrorResponse, "description": "Forbidden - user_id in URL doesn't match authenticated user"},
    404: {"model": ErrorResponse, "description": "Not Found - task does not exist"}
})
async def get_user_task(
    user_id: str = Path(..., description="User ID that owns the task"),
    task_id: UUID = Path(..., description="Task ID to retrieve"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Retrieve a specific task for the specified user.

    Returns a specific task if it belongs to the specified user.
    The authenticated user must match the user_id in the URL.
    """
    authenticated_user_id = current_user["user_id"]

    # Verify that the authenticated user matches the requested user_id
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id in URL doesn't match authenticated user"
        )

    # Create task service instance
    task_service = TaskService(db)

    try:
        # Get the specific task
        task = await task_service.get_task_by_id(task_id, UUID(user_id))

        # Return the task
        return TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        log_security_event("FAILED_TASK_RETRIEVAL", str(e), user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the task"
        )


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskRead, responses={
    200: {"model": TaskRead, "description": "Task updated successfully"},
    400: {"model": ErrorResponse, "description": "Bad Request - invalid input data"},
    401: {"model": ErrorResponse, "description": "Unauthorized - invalid or expired JWT"},
    403: {"model": ErrorResponse, "description": "Forbidden - user_id in URL doesn't match authenticated user"},
    404: {"model": ErrorResponse, "description": "Not Found - task does not exist"},
    422: {"model": ErrorResponse, "description": "Unprocessable Entity - validation errors"}
})
async def update_user_task(
    user_id: str = Path(..., description="User ID that owns the task"),
    task_id: UUID = Path(..., description="Task ID to update"),
    task_update: TaskUpdate = Body(...),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Update a specific task for the specified user.

    Updates a specific task if it belongs to the specified user.
    The authenticated user must match the user_id in the URL.
    """
    authenticated_user_id = current_user["user_id"]

    # Verify that the authenticated user matches the requested user_id
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id in URL doesn't match authenticated user"
        )

    # Create task service instance
    task_service = TaskService(db)

    try:
        # Update the task
        task = await task_service.update_task(task_id, task_update, UUID(user_id))

        # Return the updated task
        return TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        log_security_event("FAILED_TASK_UPDATE", str(e), user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the task"
        )


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, responses={
    204: {"description": "Task deleted successfully"},
    401: {"model": ErrorResponse, "description": "Unauthorized - invalid or expired JWT"},
    403: {"model": ErrorResponse, "description": "Forbidden - user_id in URL doesn't match authenticated user"},
    404: {"model": ErrorResponse, "description": "Not Found - task does not exist"}
})
async def delete_user_task(
    user_id: str = Path(..., description="User ID that owns the task"),
    task_id: UUID = Path(..., description="Task ID to delete"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Delete a specific task for the specified user.

    Deletes a specific task if it belongs to the specified user.
    The authenticated user must match the user_id in the URL.
    """
    authenticated_user_id = current_user["user_id"]

    # Verify that the authenticated user matches the requested user_id
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id in URL doesn't match authenticated user"
        )

    # Create task service instance
    task_service = TaskService(db)

    try:
        # Delete the task
        await task_service.delete_task(task_id, UUID(user_id))

        # Return 204 No Content on success
        return

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        log_security_event("FAILED_TASK_DELETION", str(e), user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the task"
        )


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskRead, responses={
    200: {"model": TaskRead, "description": "Task completion status toggled successfully"},
    401: {"model": ErrorResponse, "description": "Unauthorized - invalid or expired JWT"},
    403: {"model": ErrorResponse, "description": "Forbidden - user_id in URL doesn't match authenticated user"},
    404: {"model": ErrorResponse, "description": "Not Found - task does not exist"}
})
async def complete_user_task(
    user_id: str = Path(..., description="User ID that owns the task"),
    task_id: UUID = Path(..., description="Task ID to toggle completion for"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_session)
):
    """
    Toggle the completion status of a specific task.

    Toggles the completion status of a specific task for the specified user.
    The authenticated user must match the user_id in the URL.
    """
    authenticated_user_id = current_user["user_id"]

    # Verify that the authenticated user matches the requested user_id
    if authenticated_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id in URL doesn't match authenticated user"
        )

    # Create task service instance
    task_service = TaskService(db)

    try:
        # Toggle the task completion status
        task = await task_service.toggle_task_completion(task_id, UUID(user_id))

        # Return the updated task
        return TaskRead(
            id=task.id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            user_id=str(task.user_id),
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise

    except Exception as e:
        log_security_event("FAILED_TASK_TOGGLE", str(e), user_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while toggling the task completion status"
        )