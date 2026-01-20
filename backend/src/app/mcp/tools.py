"""
MCP tools for task operations using FastMCP patterns.

Implements the MCP tools that the AI agent can call to perform task operations.
Follows MCP Builder best practices for tool registration and error handling using FastMCP.
"""

from typing import Dict, Any, Optional
import asyncio
from sqlmodel import Session
from ..database import get_session_context
from ..models.task import Task
from ..models.conversation import Conversation
from ..models.message import Message
from ..services.task_service import TaskService


def register_mcp_tools(mcp):
    """
    Register all MCP tools with the FastMCP server using FastMCP patterns.

    Args:
        mcp: The FastMCP server instance to register tools with

    Returns:
        FastMCP instance with registered tools
    """

    # Define common error responses
    def create_error_response(error_msg: str, task_id: Optional[int] = None) -> Dict[str, Any]:
        """Helper function to create standardized error responses."""
        response = {
            "success": False,
            "error": error_msg,
            "message": error_msg
        }
        if task_id is not None:
            response["task_id"] = task_id
        return response

    def create_success_response(task_id: Optional[int] = None, message: str = "", **kwargs) -> Dict[str, Any]:
        """Helper function to create standardized success responses."""
        response = {
            "success": True,
            "message": message
        }
        if task_id is not None:
            response["task_id"] = task_id
        response.update(kwargs)
        return response

    @mcp.tool(
        name="add_task",
        description="Create a new task with title, description, priority, and starred status"
    )
    async def add_task(
        user_id: str,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium",
        is_starred: bool = False
    ) -> Dict[str, Any]:
        """
        MCP tool to add a new task following MCP Builder patterns.

        Args:
            user_id: The ID of the user creating the task
            title: The title of the task
            description: Optional description of the task
            priority: Task priority (low, medium, high)
            is_starred: Whether the task should be starred

        Returns:
            Dictionary containing the created task details
        """
        try:
            # Validate inputs
            if not title or len(title.strip()) == 0:
                return create_error_response("Title is required and cannot be empty")

            if len(title) > 200:
                return create_error_response("Title must be 200 characters or less")

            if description and len(description) > 1000:
                return create_error_response("Description must be 1000 characters or less")

            if priority not in ["low", "medium", "high"]:
                return create_error_response("Priority must be one of: low, medium, high")

            with get_session_context() as session:
                task_service = TaskService(session)
                task = task_service.create_task(user_id, title, description, priority, is_starred)

                return create_success_response(
                    task_id=task.id,
                    message=f"Task '{task.title}' created successfully",
                    task_details={
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "priority": task.priority,
                        "is_starred": task.is_starred,
                        "completed": task.completed
                    }
                )
        except Exception as e:
            return create_error_response(f"Failed to create task: {str(e)}")

    @mcp.tool(
        name="list_tasks",
        description="Get a list of tasks for a user with optional status filtering"
    )
    async def list_tasks(
        user_id: str,
        status: str = "all"
    ) -> Dict[str, Any]:
        """
        MCP tool to list tasks following MCP Builder patterns.

        Args:
            user_id: The ID of the user whose tasks to list
            status: Status filter (all, pending, completed, starred)

        Returns:
            Dictionary containing the list of tasks
        """
        try:
            # Validate status parameter
            if status not in ["all", "pending", "completed", "starred"]:
                return create_error_response("Status must be one of: all, pending, completed, starred")

            with get_session_context() as session:
                task_service = TaskService(session)

                # Map status to completed parameter for the service
                completed_param = None
                if status == "pending":
                    completed_param = False
                elif status == "completed":
                    completed_param = True

                tasks = task_service.get_tasks_by_user(user_id, completed_param)

                task_list = []
                for task in tasks:
                    task_dict = {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "priority": task.priority,
                        "is_starred": task.is_starred,
                        "created_at": task.created_at.isoformat(),
                        "updated_at": task.updated_at.isoformat()
                    }
                    task_list.append(task_dict)

                return create_success_response(
                    message=f"Retrieved {len(tasks)} tasks for user",
                    task_count=len(tasks),
                    tasks=task_list,
                    status_filter=status
                )
        except Exception as e:
            return create_error_response(f"Failed to list tasks: {str(e)}")

    @mcp.tool(
        name="complete_task",
        description="Mark a task as completed by its ID"
    )
    async def complete_task(
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        MCP tool to complete a task following MCP Builder patterns.

        Args:
            user_id: The ID of the user owning the task
            task_id: The ID of the task to complete

        Returns:
            Dictionary indicating success or failure
        """
        try:
            # Validate inputs
            if task_id <= 0:
                return create_error_response("Task ID must be a positive integer", task_id=task_id)

            with get_session_context() as session:
                task_service = TaskService(session)
                task = task_service.get_task_by_id_and_user(task_id, user_id)

                if not task:
                    return create_error_response("Task not found or unauthorized access", task_id=task_id)

                updated_task = task_service.toggle_complete(task, user_id)

                return create_success_response(
                    task_id=updated_task.id,
                    message=f"Task '{updated_task.title}' marked as completed",
                    task_details={
                        "id": updated_task.id,
                        "title": updated_task.title,
                        "completed": updated_task.completed
                    }
                )
        except Exception as e:
            return create_error_response(f"Failed to complete task: {str(e)}", task_id=task_id)

    @mcp.tool(
        name="delete_task",
        description="Delete a task by its ID"
    )
    async def delete_task(
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        MCP tool to delete a task following MCP Builder patterns.

        Args:
            user_id: The ID of the user owning the task
            task_id: The ID of the task to delete

        Returns:
            Dictionary indicating success or failure
        """
        try:
            # Validate inputs
            if task_id <= 0:
                return create_error_response("Task ID must be a positive integer", task_id=task_id)

            with get_session_context() as session:
                task_service = TaskService(session)
                task = task_service.get_task_by_id_and_user(task_id, user_id)

                if not task:
                    return create_error_response("Task not found or unauthorized access", task_id=task_id)

                task_service.delete_task(task, user_id)

                return create_success_response(
                    task_id=task_id,
                    message="Task deleted successfully"
                )
        except Exception as e:
            return create_error_response(f"Failed to delete task: {str(e)}", task_id=task_id)

    @mcp.tool(
        name="update_task",
        description="Update a task's properties by its ID"
    )
    async def update_task(
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[str] = None,
        is_starred: Optional[bool] = None,
        completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        MCP tool to update a task following MCP Builder patterns.

        Args:
            user_id: The ID of the user owning the task
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            is_starred: New starred status (optional)
            completed: New completion status (optional)

        Returns:
            Dictionary containing the updated task details
        """
        try:
            # Validate inputs
            if task_id <= 0:
                return create_error_response("Task ID must be a positive integer", task_id=task_id)

            if title and (len(title) == 0 or len(title) > 200):
                return create_error_response("Title must be between 1 and 200 characters if provided", task_id=task_id)

            if description and len(description) > 1000:
                return create_error_response("Description must be 1000 characters or less", task_id=task_id)

            if priority and priority not in ["low", "medium", "high"]:
                return create_error_response("Priority must be one of: low, medium, high", task_id=task_id)

            with get_session_context() as session:
                task_service = TaskService(session)
                task = task_service.get_task_by_id_and_user(task_id, user_id)

                if not task:
                    return create_error_response("Task not found or unauthorized access", task_id=task_id)

                updated_task = task_service.update_task(
                    task,
                    user_id,
                    title=title,
                    description=description,
                    priority=priority,
                    starred=is_starred,
                    completed=completed
                )

                return create_success_response(
                    task_id=updated_task.id,
                    message=f"Task '{updated_task.title}' updated successfully",
                    task_details={
                        "id": updated_task.id,
                        "title": updated_task.title,
                        "description": updated_task.description,
                        "completed": updated_task.completed,
                        "priority": updated_task.priority,
                        "is_starred": updated_task.is_starred
                    }
                )
        except Exception as e:
            return create_error_response(f"Failed to update task: {str(e)}", task_id=task_id)

    # Additional utility tools for MCP Builder patterns
    @mcp.tool(
        name="get_task",
        description="Get details of a specific task by its ID"
    )
    async def get_task(
        user_id: str,
        task_id: int
    ) -> Dict[str, Any]:
        """
        MCP tool to get details of a specific task following MCP Builder patterns.

        Args:
            user_id: The ID of the user owning the task
            task_id: The ID of the task to retrieve

        Returns:
            Dictionary containing the task details
        """
        try:
            if task_id <= 0:
                return create_error_response("Task ID must be a positive integer", task_id=task_id)

            with get_session_context() as session:
                task_service = TaskService(session)
                task = task_service.get_task_by_id_and_user(task_id, user_id)

                if task:
                    return create_success_response(
                        task_id=task.id,
                        message=f"Retrieved task '{task.title}'",
                        task_details={
                            "id": task.id,
                            "title": task.title,
                            "description": task.description,
                            "completed": task.completed,
                            "priority": task.priority,
                            "is_starred": task.is_starred,
                            "created_at": task.created_at.isoformat(),
                            "updated_at": task.updated_at.isoformat()
                        }
                    )
                else:
                    return create_error_response("Task not found or unauthorized access", task_id=task_id)
        except Exception as e:
            return create_error_response(f"Failed to retrieve task: {str(e)}", task_id=task_id)

    return mcp