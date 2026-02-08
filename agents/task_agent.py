from typing import List, Optional
from datetime import datetime
from .todo_agent import TodoAgent, Task, Priority, TaskStatus

class TaskAgent:
    """
    TaskAgent that manages task operations using the TodoAgent
    """

    def __init__(self, todo_agent: TodoAgent):
        self.todo_agent = todo_agent

    async def get_user_tasks(self, user_id: str) -> List[Task]:
        """Get all tasks for a specific user"""
        return await self.todo_agent.get_tasks(user_id)

    async def create_user_task(self, user_id: str, title: str, description: str = "",
                              priority: Priority = Priority.MEDIUM, completed: bool = False) -> Task:
        """Create a new task for a specific user"""
        return await self.todo_agent.create_task(user_id, title, description, priority, completed)

    async def update_user_task(self, user_id: str, task_id: str, title: str = None,
                              description: str = None, completed: bool = None,
                              priority: Priority = None, status: TaskStatus = None) -> Task:
        """Update a task for a specific user"""
        update_data = {}
        if title is not None:
            update_data['title'] = title
        if description is not None:
            update_data['description'] = description
        if completed is not None:
            update_data['completed'] = completed
        if priority is not None:
            update_data['priority'] = priority.value if isinstance(priority, Priority) else priority
        if status is not None:
            update_data['status'] = status.value if isinstance(status, TaskStatus) else status

        return await self.todo_agent.update_task(user_id, task_id, **update_data)

    async def delete_user_task(self, user_id: str, task_id: str) -> bool:
        """Delete a task for a specific user"""
        return await self.todo_agent.delete_task(user_id, task_id)

    async def toggle_user_task_completion(self, user_id: str, task_id: str) -> Task:
        """Toggle completion status of a task for a specific user"""
        return await self.todo_agent.toggle_task_completion(user_id, task_id)

    async def get_completed_tasks(self, user_id: str) -> List[Task]:
        """Get only completed tasks for a user"""
        all_tasks = await self.get_user_tasks(user_id)
        return [task for task in all_tasks if task.completed]

    async def get_pending_tasks(self, user_id: str) -> List[Task]:
        """Get only pending (non-completed) tasks for a user"""
        all_tasks = await self.get_user_tasks(user_id)
        return [task for task in all_tasks if not task.completed]

    async def mark_task_as_completed(self, user_id: str, task_id: str) -> Task:
        """Mark a specific task as completed"""
        return await self.update_user_task(user_id, task_id, completed=True)

    async def mark_task_as_pending(self, user_id: str, task_id: str) -> Task:
        """Mark a specific task as pending (not completed)"""
        return await self.update_user_task(user_id, task_id, completed=False)