from typing import Dict, List, Optional
from datetime import datetime
import asyncio
import aiohttp
import os
from enum import Enum

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(Enum):
    TODO = "todo"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"

class Task:
    def __init__(self, id: str, title: str, description: str = "", completed: bool = False,
                 priority: Priority = Priority.MEDIUM, status: TaskStatus = TaskStatus.TODO,
                 created_at: datetime = None, updated_at: datetime = None, user_id: str = ""):
        self.id = id
        self.title = title
        self.description = description
        self.completed = completed
        self.priority = priority
        self.status = status
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.user_id = user_id

class TodoAgent:
    """
    TodoAgent that connects to the backend API to manage tasks
    """

    def __init__(self, base_url: str = None, auth_token: str = None):
        self.base_url = base_url or os.getenv('NEXT_PUBLIC_API_BASE', 'http://localhost:8000')
        self.auth_token = auth_token
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def set_auth_token(self, token: str):
        """Set the authentication token for API calls"""
        self.auth_token = token

    async def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make an HTTP request to the backend API"""
        if not self.session:
            raise RuntimeError("Agent not initialized. Use 'async with TodoAgent() as agent'")

        headers = {
            'Content-Type': 'application/json',
        }

        if self.auth_token:
            headers['Authorization'] = f'Bearer {self.auth_token}'

        url = f"{self.base_url}{endpoint}"

        async with self.session.request(method, url, json=data, headers=headers) as response:
            if response.status >= 400:
                error_text = await response.text()
                raise Exception(f"API request failed with status {response.status}: {error_text}")

            return await response.json()

    async def get_tasks(self, user_id: str) -> List[Task]:
        """Get all tasks for a user"""
        response = await self._make_request('GET', f'/api/{user_id}/tasks')

        tasks_data = response.get('tasks', [])
        tasks = []

        for task_data in tasks_data:
            task = Task(
                id=task_data.get('id'),
                title=task_data.get('title'),
                description=task_data.get('description', ''),
                completed=task_data.get('completed', False),
                user_id=task_data.get('user_id', user_id),
                created_at=datetime.fromisoformat(task_data.get('created_at')) if task_data.get('created_at') else None,
                updated_at=datetime.fromisoformat(task_data.get('updated_at')) if task_data.get('updated_at') else None
            )
            tasks.append(task)

        return tasks

    async def create_task(self, user_id: str, title: str, description: str = "",
                         priority: Priority = Priority.MEDIUM, completed: bool = False) -> Task:
        """Create a new task"""
        task_data = {
            'title': title,
            'description': description,
            'completed': completed,
            'user_id': user_id
        }

        response = await self._make_request('POST', f'/api/{user_id}/tasks', task_data)

        task_data_response = response.get('task', response)  # Handle different response formats
        task = Task(
            id=task_data_response.get('id'),
            title=task_data_response.get('title'),
            description=task_data_response.get('description', ''),
            completed=task_data_response.get('completed', False),
            user_id=task_data_response.get('user_id', user_id),
            created_at=datetime.fromisoformat(task_data_response.get('created_at')) if task_data_response.get('created_at') else None,
            updated_at=datetime.fromisoformat(task_data_response.get('updated_at')) if task_data_response.get('updated_at') else None
        )

        return task

    async def update_task(self, user_id: str, task_id: str, **kwargs) -> Task:
        """Update a task"""
        task_data = {k: v for k, v in kwargs.items() if v is not None}

        response = await self._make_request('PUT', f'/api/{user_id}/tasks/{task_id}', task_data)

        task_data_response = response.get('task', response)
        task = Task(
            id=task_data_response.get('id'),
            title=task_data_response.get('title'),
            description=task_data_response.get('description', ''),
            completed=task_data_response.get('completed', False),
            user_id=task_data_response.get('user_id', user_id),
            created_at=datetime.fromisoformat(task_data_response.get('created_at')) if task_data_response.get('created_at') else None,
            updated_at=datetime.fromisoformat(task_data_response.get('updated_at')) if task_data_response.get('updated_at') else None
        )

        return task

    async def delete_task(self, user_id: str, task_id: str) -> bool:
        """Delete a task"""
        try:
            await self._make_request('DELETE', f'/api/{user_id}/tasks/{task_id}')
            return True
        except Exception:
            return False

    async def toggle_task_completion(self, user_id: str, task_id: str) -> Task:
        """Toggle the completion status of a task"""
        response = await self._make_request('PATCH', f'/api/{user_id}/tasks/{task_id}/complete')

        task_data = response.get('task', response)
        task = Task(
            id=task_data.get('id'),
            title=task_data.get('title'),
            description=task_data.get('description', ''),
            completed=task_data.get('completed', False),
            user_id=task_data.get('user_id', user_id),
            created_at=datetime.fromisoformat(task_data.get('created_at')) if task_data.get('created_at') else None,
            updated_at=datetime.fromisoformat(task_data.get('updated_at')) if task_data.get('updated_at') else None
        )

        return task