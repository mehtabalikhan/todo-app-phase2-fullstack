from typing import List, Dict, Any
from .task_agent import TaskAgent
from .todo_agent import TodoAgent, Task, Priority, TaskStatus
import asyncio

class TaskSkills:
    """
    Skills that interact with the backend through the agents using real SQLModel queries
    """

    def __init__(self, task_agent: TaskAgent):
        self.task_agent = task_agent

    async def list_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """
        List all tasks for a user
        """
        try:
            tasks = await self.task_agent.get_user_tasks(user_id)
            return [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
                    'status': task.status.value if hasattr(task.status, 'value') else task.status,
                    'created_at': task.created_at.isoformat() if task.created_at else None,
                    'updated_at': task.updated_at.isoformat() if task.updated_at else None,
                    'user_id': task.user_id
                }
                for task in tasks
            ]
        except Exception as e:
            print(f"Error listing tasks: {str(e)}")
            return []

    async def create_task(self, user_id: str, title: str, description: str = "",
                         priority: str = "medium", completed: bool = False) -> Dict[str, Any]:
        """
        Create a new task for a user
        """
        try:
            # Convert priority string to Priority enum
            priority_enum = Priority[priority.upper()] if priority.upper() in [p.name for p in Priority] else Priority.MEDIUM

            task = await self.task_agent.create_user_task(
                user_id=user_id,
                title=title,
                description=description,
                priority=priority_enum,
                completed=completed
            )

            return {
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
                    'status': task.status.value if hasattr(task.status, 'value') else task.status,
                    'created_at': task.created_at.isoformat() if task.created_at else None,
                    'updated_at': task.updated_at.isoformat() if task.updated_at else None,
                    'user_id': task.user_id
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def update_task(self, user_id: str, task_id: str, **kwargs) -> Dict[str, Any]:
        """
        Update a task for a user
        """
        try:
            # Process priority if provided
            if 'priority' in kwargs and kwargs['priority']:
                priority_str = kwargs['priority'].upper()
                if priority_str in [p.name for p in Priority]:
                    kwargs['priority'] = Priority[priority_str]

            task = await self.task_agent.update_user_task(user_id, task_id, **kwargs)

            return {
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
                    'status': task.status.value if hasattr(task.status, 'value') else task.status,
                    'created_at': task.created_at.isoformat() if task.created_at else None,
                    'updated_at': task.updated_at.isoformat() if task.updated_at else None,
                    'user_id': task.user_id
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def delete_task(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Delete a task for a user
        """
        try:
            success = await self.task_agent.delete_user_task(user_id, task_id)
            return {
                'success': success,
                'message': 'Task deleted successfully' if success else 'Failed to delete task'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def toggle_task_completion(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Toggle the completion status of a task
        """
        try:
            task = await self.task_agent.toggle_user_task_completion(user_id, task_id)

            return {
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
                    'status': task.status.value if hasattr(task.status, 'value') else task.status,
                    'created_at': task.created_at.isoformat() if task.created_at else None,
                    'updated_at': task.updated_at.isoformat() if task.updated_at else None,
                    'user_id': task.user_id
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def mark_task_completed(self, user_id: str, task_id: str) -> Dict[str, Any]:
        """
        Mark a task as completed
        """
        try:
            task = await self.task_agent.mark_task_as_completed(user_id, task_id)

            return {
                'success': True,
                'task': {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
                    'status': task.status.value if hasattr(task.status, 'value') else task.status,
                    'created_at': task.created_at.isoformat() if task.created_at else None,
                    'updated_at': task.updated_at.isoformat() if task.updated_at else None,
                    'user_id': task.user_id
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    async def get_completed_tasks(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all completed tasks for a user
        """
        try:
            tasks = await self.task_agent.get_completed_tasks(user_id)
            return [
                {
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'completed': task.completed,
                    'priority': task.priority.value if hasattr(task.priority, 'value') else task.priority,
                    'status': task.status.value if hasattr(task.status, 'value') else task.status,
                    'created_at': task.created_at.isoformat() if task.created_at else None,
                    'updated_at': task.updated_at.isoformat() if task.updated_at else None,
                    'user_id': task.user_id
                }
                for task in tasks
            ]
        except Exception as e:
            print(f"Error getting completed tasks: {str(e)}")
            return []