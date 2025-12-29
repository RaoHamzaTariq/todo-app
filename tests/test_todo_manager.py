# SDD: Implements Task ID: T009
"""Unit tests for TodoManager.

This module contains tests for the core business logic.
"""

import pytest

from src.core.models import Task, TaskStatus
from src.core.todo_manager import TodoManager


class TestTodoManager:
    """Test cases for TodoManager class."""

    def test_init(self) -> None:
        """Test TodoManager initialization."""
        manager = TodoManager()
        assert manager._tasks == []
        assert manager._next_id == 1
