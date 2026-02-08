"""
End-to-End Tests for Critical User Workflows

This module contains end-to-end tests for critical user workflows in the Todo Chatbot application.
These tests verify that the complete user journeys work as expected, including:
- Creating tasks with advanced features (recurring, due dates, reminders)
- Managing tasks through the UI
- Verifying event-driven behavior
"""

import pytest
import asyncio
import aiohttp
from typing import Dict, Any
import uuid
from datetime import datetime, timedelta


class TestEndToEndWorkflows:
    """Test suite for critical end-to-end user workflows."""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"  # Adjust to your backend URL
        self.session = None
        self.test_user_id = f"test_user_{uuid.uuid4()}"
    
    @pytest.fixture(autouse=True)
    async def setup_session(self):
        """Setup aiohttp session for all tests."""
        self.session = aiohttp.ClientSession()
        yield
        await self.session.close()
    
    async def create_test_task(self, title: str, description: str = "", due_date: str = None, priority: str = "medium"):
        """Helper method to create a test task."""
        task_data = {
            "title": title,
            "description": description,
            "due_date": due_date,
            "priority": priority,
            "user_id": self.test_user_id
        }
        
        async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks", json=task_data) as resp:
            assert resp.status == 200
            return await resp.json()
    
    async def create_test_recurring_task(self, title: str, frequency: str = "daily", interval: int = 1):
        """Helper method to create a recurring task."""
        recurring_data = {
            "title": title,
            "frequency": frequency,
            "interval": interval,
            "active": True,
            "user_id": self.test_user_id
        }
        
        async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks/recurring", json=recurring_data) as resp:
            assert resp.status == 200
            return await resp.json()
    
    async def create_test_reminder(self, task_id: int, reminder_datetime: str):
        """Helper method to create a reminder for a task."""
        reminder_data = {
            "task_id": task_id,
            "reminder_datetime": reminder_datetime,
            "user_id": self.test_user_id
        }
        
        async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/reminders", json=reminder_data) as resp:
            assert resp.status == 200
            return await resp.json()
    
    @pytest.mark.asyncio
    async def test_complete_task_workflow(self):
        """
        Test the complete workflow for managing a task:
        1. Create a task
        2. Retrieve the task
        3. Update the task
        4. Mark as completed
        5. Verify completion
        """
        # Step 1: Create a task
        task_title = f"Test Task - {datetime.now().isoformat()}"
        task_desc = "This is a test task for the end-to-end workflow"
        due_date = (datetime.now() + timedelta(days=1)).isoformat()
        
        task_response = await self.create_test_task(
            title=task_title,
            description=task_desc,
            due_date=due_date,
            priority="high"
        )
        
        task_id = task_response.get("id")
        assert task_id is not None, "Task should be created successfully"
        
        # Step 2: Retrieve the task
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks/{task_id}") as resp:
            assert resp.status == 200
            retrieved_task = await resp.json()
            assert retrieved_task["title"] == task_title
            assert retrieved_task["description"] == task_desc
            assert retrieved_task["completed"] is False
        
        # Step 3: Update the task
        updated_data = {
            "title": f"Updated - {task_title}",
            "description": f"Updated - {task_desc}",
            "priority": "low",
            "completed": False
        }
        
        async with self.session.put(f"{self.base_url}/api/{self.test_user_id}/tasks/{task_id}", json=updated_data) as resp:
            assert resp.status == 200
            updated_task = await resp.json()
            assert updated_task["title"] == f"Updated - {task_title}"
            assert updated_task["priority"] == "low"
        
        # Step 4: Mark as completed
        completion_data = {"completed": True}
        async with self.session.put(f"{self.base_url}/api/{self.test_user_id}/tasks/{task_id}", json=completion_data) as resp:
            assert resp.status == 200
            completed_task = await resp.json()
            assert completed_task["completed"] is True
        
        # Step 5: Verify completion
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks/{task_id}") as resp:
            assert resp.status == 200
            final_task = await resp.json()
            assert final_task["completed"] is True
    
    @pytest.mark.asyncio
    async def test_recurring_task_workflow(self):
        """
        Test the complete workflow for managing recurring tasks:
        1. Create a recurring task
        2. Verify it was created
        3. Update the recurring task
        4. Verify the update
        """
        # Step 1: Create a recurring task
        recurring_title = f"Recurring Task - {datetime.now().isoformat()}"
        recurring_freq = "weekly"
        recurring_interval = 1
        
        recurring_response = await self.create_test_recurring_task(
            title=recurring_title,
            frequency=recurring_freq,
            interval=recurring_interval
        )
        
        recurring_id = recurring_response.get("id")
        assert recurring_id is not None, "Recurring task should be created successfully"
        
        # Step 2: Verify it was created
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks/recurring/{recurring_id}") as resp:
            assert resp.status == 200
            retrieved_recurring = await resp.json()
            assert retrieved_recurring["title"] == recurring_title
            assert retrieved_recurring["frequency"] == recurring_freq
            assert retrieved_recurring["active"] is True
        
        # Step 3: Update the recurring task
        updated_recurring_data = {
            "title": f"Updated - {recurring_title}",
            "frequency": "daily",
            "interval": 2,
            "active": True
        }
        
        async with self.session.put(f"{self.base_url}/api/{self.test_user_id}/tasks/recurring/{recurring_id}", json=updated_recurring_data) as resp:
            assert resp.status == 200
            updated_recurring = await resp.json()
            assert updated_recurring["title"] == f"Updated - {recurring_title}"
            assert updated_recurring["frequency"] == "daily"
            assert updated_recurring["interval"] == 2
        
        # Step 4: Verify the update
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks/recurring/{recurring_id}") as resp:
            assert resp.status == 200
            final_recurring = await resp.json()
            assert final_recurring["title"] == f"Updated - {recurring_title}"
            assert final_recurring["frequency"] == "daily"
    
    @pytest.mark.asyncio
    async def test_reminder_workflow(self):
        """
        Test the complete workflow for managing reminders:
        1. Create a task
        2. Create a reminder for the task
        3. Retrieve the reminder
        4. Cancel the reminder
        """
        # Step 1: Create a task
        task_title = f"Task with Reminder - {datetime.now().isoformat()}"
        task_response = await self.create_test_task(title=task_title)
        task_id = task_response.get("id")
        assert task_id is not None, "Task should be created successfully"
        
        # Step 2: Create a reminder for the task
        reminder_time = (datetime.now() + timedelta(hours=1)).isoformat()
        reminder_response = await self.create_test_reminder(task_id, reminder_time)
        
        reminder_id = reminder_response.get("id")
        assert reminder_id is not None, "Reminder should be created successfully"
        
        # Step 3: Retrieve the reminder
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/reminders/{reminder_id}") as resp:
            assert resp.status == 200
            retrieved_reminder = await resp.json()
            assert retrieved_reminder["task_id"] == task_id
            assert retrieved_reminder["sent"] is False
        
        # Step 4: Cancel the reminder
        async with self.session.delete(f"{self.base_url}/api/{self.test_user_id}/reminders/{reminder_id}") as resp:
            assert resp.status == 200
            result = await resp.json()
            assert result["success"] is True
        
        # Verify the reminder was deleted
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/reminders/{reminder_id}") as resp:
            # Should return 404 or similar error since it's deleted
            assert resp.status != 200
    
    @pytest.mark.asyncio
    async def test_advanced_task_features_workflow(self):
        """
        Test the workflow for advanced task features:
        1. Create a task with priority and tags
        2. Search for the task using tags
        3. Filter tasks by priority
        4. Verify all advanced features work together
        """
        # Step 1: Create a task with advanced features
        task_title = f"Advanced Task - {datetime.now().isoformat()}"
        task_data = {
            "title": task_title,
            "description": "Task with advanced features",
            "priority": "high",
            "tags": "important,work,urgent",
            "user_id": self.test_user_id
        }
        
        async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks", json=task_data) as resp:
            assert resp.status == 200
            created_task = await resp.json()
            assert created_task["title"] == task_title
            assert created_task["priority"] == "high"
            assert "important" in created_task["tags"]
        
        task_id = created_task["id"]
        
        # Step 2: Search for the task using tags
        search_params = {"query": "important"}
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks/search", params=search_params) as resp:
            assert resp.status == 200
            search_results = await resp.json()
            found_task = next((t for t in search_results if t["id"] == task_id), None)
            assert found_task is not None, "Task should be found in search results"
        
        # Step 3: Filter tasks by priority
        filter_params = {"priority": "high"}
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks", params=filter_params) as resp:
            assert resp.status == 200
            filtered_results = await resp.json()
            high_priority_task = next((t for t in filtered_results if t["id"] == task_id), None)
            assert high_priority_task is not None, "Task should be found in priority filter"
    
    @pytest.mark.asyncio
    async def test_full_user_journey(self):
        """
        Test a complete user journey combining all features:
        1. Create multiple tasks with different features
        2. Create recurring tasks
        3. Set up reminders
        4. Organize with tags and priorities
        5. Search and filter
        6. Complete tasks
        """
        # Step 1: Create multiple tasks with different features
        tasks_data = [
            {
                "title": f"High Priority Task - {datetime.now().isoformat()}",
                "description": "High priority task",
                "priority": "high",
                "tags": "important,work",
                "due_date": (datetime.now() + timedelta(days=1)).isoformat()
            },
            {
                "title": f"Low Priority Task - {datetime.now().isoformat()}",
                "description": "Low priority task",
                "priority": "low",
                "tags": "personal,low",
                "due_date": (datetime.now() + timedelta(days=7)).isoformat()
            },
            {
                "title": f"Medium Priority Task - {datetime.now().isoformat()}",
                "description": "Medium priority task",
                "priority": "medium",
                "tags": "work,medium",
                "due_date": (datetime.now() + timedelta(days=3)).isoformat()
            }
        ]
        
        created_tasks = []
        for task_data in tasks_data:
            task_data["user_id"] = self.test_user_id
            async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks", json=task_data) as resp:
                assert resp.status == 200
                created_tasks.append(await resp.json())
        
        # Step 2: Create a recurring task
        recurring_data = {
            "title": f"Weekly Review - {datetime.now().isoformat()}",
            "frequency": "weekly",
            "interval": 1,
            "active": True,
            "user_id": self.test_user_id
        }
        
        async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks/recurring", json=recurring_data) as resp:
            assert resp.status == 200
            recurring_task = await resp.json()
        
        # Step 3: Set up a reminder for the high priority task
        high_priority_task = next(t for t in created_tasks if t["priority"] == "high")
        reminder_time = (datetime.now() + timedelta(minutes=30)).isoformat()
        
        reminder_data = {
            "task_id": high_priority_task["id"],
            "reminder_datetime": reminder_time,
            "user_id": self.test_user_id
        }
        
        async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/reminders", json=reminder_data) as resp:
            assert resp.status == 200
            reminder = await resp.json()
        
        # Step 4: Search for important tasks
        search_params = {"query": "important"}
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks/search", params=search_params) as resp:
            assert resp.status == 200
            search_results = await resp.json()
            assert len(search_results) >= 1, "Should find at least one important task"
        
        # Step 5: Filter by high priority
        filter_params = {"priority": "high"}
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks", params=filter_params) as resp:
            assert resp.status == 200
            high_priority_results = await resp.json()
            assert len(high_priority_results) >= 1, "Should find at least one high priority task"
        
        # Step 6: Complete the low priority task
        low_priority_task = next(t for t in created_tasks if t["priority"] == "low")
        completion_data = {"completed": True}
        
        async with self.session.put(f"{self.base_url}/api/{self.test_user_id}/tasks/{low_priority_task['id']}", json=completion_data) as resp:
            assert resp.status == 200
            completed_task = await resp.json()
            assert completed_task["completed"] is True
        
        # Verify the task is completed
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks/{low_priority_task['id']}") as resp:
            assert resp.status == 200
            final_task = await resp.json()
            assert final_task["completed"] is True


# Run the tests if this file is executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])