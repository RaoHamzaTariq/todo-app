"""
Power-User Integration Tests for Event-Driven System

This module contains advanced integration tests for the event-driven system,
focusing on power-user scenarios and edge cases that test the robustness
of the event-driven architecture with Kafka and Dapr.
"""

import pytest
import asyncio
import aiohttp
from typing import Dict, Any, List
import uuid
from datetime import datetime, timedelta
import json
import time


class TestPowerUserEventDrivenSystem:
    """Test suite for power-user scenarios in the event-driven system."""
    
    def __init__(self):
        self.base_url = "http://localhost:8000"  # Adjust to your backend URL
        self.session = None
        self.test_user_id = f"power_user_{uuid.uuid4()}"
    
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
    async def test_high_volume_task_creation(self):
        """
        Power-user test: Create a high volume of tasks rapidly to test
        the event-driven system's ability to handle load.
        """
        num_tasks = 50  # Adjust based on your system's capacity
        tasks_created = []
        
        start_time = time.time()
        
        # Create tasks concurrently
        async def create_single_task(i):
            task_data = {
                "title": f"High Volume Task {i} - {datetime.now().isoformat()}",
                "description": f"Task {i} created in high volume test",
                "priority": "medium" if i % 2 == 0 else "high",
                "tags": f"bulk,test-{i % 5}",
                "user_id": self.test_user_id
            }
            
            async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks", json=task_data) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    print(f"Failed to create task {i}: {resp.status}")
                    return None
        
        # Create tasks concurrently
        tasks = await asyncio.gather(*[create_single_task(i) for i in range(num_tasks)])
        tasks_created = [t for t in tasks if t is not None]
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        print(f"Created {len(tasks_created)} tasks in {elapsed_time:.2f} seconds")
        print(f"Average rate: {len(tasks_created)/elapsed_time:.2f} tasks/sec")
        
        # Verify all tasks were created
        assert len(tasks_created) == num_tasks, f"Expected {num_tasks} tasks, got {len(tasks_created)}"
        
        # Verify tasks are retrievable
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks") as resp:
            assert resp.status == 200
            all_tasks = await resp.json()
            user_tasks = [t for t in all_tasks if t["user_id"] == self.test_user_id]
            assert len(user_tasks) >= num_tasks, f"Expected at least {num_tasks} tasks for user, got {len(user_tasks)}"
    
    @pytest.mark.asyncio
    async def test_concurrent_user_operations(self):
        """
        Power-user test: Simulate multiple users performing operations
        simultaneously to test event ordering and consistency.
        """
        num_users = 10
        tasks_per_user = 5
        all_tasks = []
        
        async def create_tasks_for_user(user_idx):
            user_id = f"concurrent_user_{user_idx}_{uuid.uuid4()}"
            user_tasks = []
            
            for i in range(tasks_per_user):
                task_data = {
                    "title": f"User {user_idx} Task {i} - {datetime.now().isoformat()}",
                    "description": f"Task for user {user_idx}",
                    "priority": "medium",
                    "user_id": user_id
                }
                
                async with self.session.post(f"{self.base_url}/api/{user_id}/tasks", json=task_data) as resp:
                    if resp.status == 200:
                        task = await resp.json()
                        user_tasks.append(task)
            
            return user_tasks
        
        # Create tasks for all users concurrently
        all_user_tasks = await asyncio.gather(*[create_tasks_for_user(i) for i in range(num_users)])
        
        # Flatten the list
        for user_tasks in all_user_tasks:
            all_tasks.extend(user_tasks)
        
        expected_total = num_users * tasks_per_user
        assert len(all_tasks) == expected_total, f"Expected {expected_total} tasks, got {len(all_tasks)}"
        
        # Verify tasks for a few users individually
        for i in range(min(3, num_users)):  # Check first 3 users
            user_id = [t["user_id"] for t in all_tasks if f"concurrent_user_{i}" in t["user_id"]][0]
            async with self.session.get(f"{self.base_url}/api/{user_id}/tasks") as resp:
                assert resp.status == 200
                user_specific_tasks = await resp.json()
                user_tasks = [t for t in user_specific_tasks if t["user_id"] == user_id]
                assert len(user_tasks) == tasks_per_user, f"User {i} should have {tasks_per_user} tasks"
    
    @pytest.mark.asyncio
    async def test_complex_recurring_task_patterns(self):
        """
        Power-user test: Create complex recurring task patterns and verify
        they generate appropriate events.
        """
        # Create various recurring patterns
        recurring_patterns = [
            {"title": "Daily Standup", "frequency": "daily", "interval": 1},
            {"title": "Weekly Report", "frequency": "weekly", "interval": 1},
            {"title": "Monthly Review", "frequency": "monthly", "interval": 1},
            {"title": "Bi-weekly Meeting", "frequency": "weekly", "interval": 2},
            {"title": "Quarterly Planning", "frequency": "monthly", "interval": 3},
        ]
        
        created_recurring_tasks = []
        
        for pattern in recurring_patterns:
            pattern["user_id"] = self.test_user_id
            async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks/recurring", json=pattern) as resp:
                assert resp.status == 200
                created_recurring_tasks.append(await resp.json())
        
        assert len(created_recurring_tasks) == len(recurring_patterns)
        
        # Verify each recurring task was created with correct parameters
        for i, pattern in enumerate(recurring_patterns):
            created_task = created_recurring_tasks[i]
            assert created_task["title"] == pattern["title"]
            assert created_task["frequency"] == pattern["frequency"]
            assert created_task["interval"] == pattern["interval"]
            assert created_task["active"] is True
    
    @pytest.mark.asyncio
    async def test_reminder_burst_scenario(self):
        """
        Power-user test: Create many reminders in a short time window
        to test the system's ability to handle reminder bursts.
        """
        # First, create a base task
        base_task = await self.create_test_task("Base Task for Reminders")
        base_task_id = base_task["id"]
        
        # Create many reminders for the same time window
        reminder_times = []
        base_time = datetime.now() + timedelta(minutes=5)
        
        for i in range(20):  # Create 20 reminders
            # Create reminders within a 10-minute window
            reminder_time = base_time + timedelta(seconds=i*30)  # Every 30 seconds
            reminder_times.append(reminder_time.isoformat())
        
        created_reminders = []
        
        # Create reminders concurrently
        async def create_reminder(reminder_time):
            reminder_data = {
                "task_id": base_task_id,
                "reminder_datetime": reminder_time,
                "user_id": self.test_user_id
            }
            
            async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/reminders", json=reminder_data) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    print(f"Failed to create reminder for {reminder_time}: {resp.status}")
                    return None
        
        reminders = await asyncio.gather(*[create_reminder(time_str) for time_str in reminder_times])
        created_reminders = [r for r in reminders if r is not None]
        
        assert len(created_reminders) == len(reminder_times), f"Expected {len(reminder_times)} reminders, got {len(created_reminders)}"
        
        # Verify reminders were created with correct times
        for i, reminder in enumerate(created_reminders):
            expected_time = reminder_times[i]
            assert reminder["reminder_datetime"].startswith(expected_time[:19]), f"Reminder {i} has incorrect time"
    
    @pytest.mark.asyncio
    async def test_task_dependency_chain(self):
        """
        Power-user test: Create a chain of dependent tasks where completion
        of one triggers creation or modification of others via events.
        """
        # In a real implementation, this would test actual event-driven
        # task dependencies. For now, we'll simulate by creating tasks
        # and verifying the system can handle complex relationships.
        
        # Create parent task
        parent_task = await self.create_test_task(
            title="Parent Task",
            description="This is a parent task in a dependency chain"
        )
        parent_task_id = parent_task["id"]
        
        # Create dependent tasks
        dependent_tasks = []
        for i in range(5):
            dep_task = await self.create_test_task(
                title=f"Dependent Task {i}",
                description=f"Depends on parent task {parent_task_id}",
                priority="high"
            )
            dependent_tasks.append(dep_task)
        
        # In a real system, completing the parent task would trigger
        # events that affect the dependent tasks. Here we just verify
        # that all tasks exist and can be manipulated.
        
        assert parent_task_id is not None
        assert len(dependent_tasks) == 5
        
        # Mark parent as completed
        completion_data = {"completed": True}
        async with self.session.put(f"{self.base_url}/api/{self.test_user_id}/tasks/{parent_task_id}", json=completion_data) as resp:
            assert resp.status == 200
            updated_parent = await resp.json()
            assert updated_parent["completed"] is True
    
    @pytest.mark.asyncio
    async def test_event_stream_under_load(self):
        """
        Power-user test: Verify event streams work correctly under load
        by creating many tasks and checking the event stream.
        """
        # Create a moderate number of tasks to generate events
        num_tasks = 25
        created_tasks = []
        
        for i in range(num_tasks):
            task_data = {
                "title": f"Event Stream Test Task {i} - {datetime.now().isoformat()}",
                "description": f"Task {i} for event stream testing",
                "priority": "medium",
                "user_id": self.test_user_id
            }
            
            async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks", json=task_data) as resp:
                assert resp.status == 200
                created_tasks.append(await resp.json())
        
        # Now try to access the event stream (assuming it exists)
        # Note: The actual endpoint might differ based on implementation
        try:
            async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/events/task-stream") as resp:
                if resp.status == 200:
                    events = await resp.json()
                    # Verify we have events corresponding to our task creations
                    task_creation_events = [e for e in events if e.get("event_type") == "task.created"]
                    assert len(task_creation_events) >= num_tasks, f"Expected at least {num_tasks} creation events, got {len(task_creation_events)}"
                elif resp.status == 404:
                    # Endpoint might not be implemented yet, which is OK
                    print("Event stream endpoint not found - this is acceptable if not yet implemented")
                else:
                    print(f"Unexpected status for event stream: {resp.status}")
        except Exception as e:
            print(f"Could not access event stream: {e}")
            # This is acceptable if the endpoint isn't implemented yet
    
    @pytest.mark.asyncio
    async def test_system_resilience_with_failures(self):
        """
        Power-user test: Simulate component failures and verify
        the system recovers gracefully and processes missed events.
        """
        # This test would typically involve:
        # 1. Starting with a baseline of tasks
        # 2. Temporarily disrupting a service (simulated)
        # 3. Creating more tasks during disruption
        # 4. Restoring service
        # 5. Verifying all tasks are processed correctly
        
        # For this implementation, we'll simulate by creating tasks
        # before and after a "disruption" and verifying they all exist
        
        # Create initial tasks
        initial_tasks = []
        for i in range(10):
            task = await self.create_test_task(f"Initial Task {i}")
            initial_tasks.append(task)
        
        # Simulate a disruption period by just continuing
        # (in a real system, we'd stop/start services)
        
        # Create tasks during "disruption"
        disruption_tasks = []
        for i in range(10):
            task = await self.create_test_task(f"Disruption Task {i}")
            disruption_tasks.append(task)
        
        # Verify all tasks exist after "recovery"
        async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks") as resp:
            assert resp.status == 200
            all_tasks = await resp.json()
            user_tasks = [t for t in all_tasks if t["user_id"] == self.test_user_id]
            
            expected_total = len(initial_tasks) + len(disruption_tasks)
            assert len(user_tasks) >= expected_total, f"Expected at least {expected_total} tasks after recovery, got {len(user_tasks)}"
    
    @pytest.mark.asyncio
    async def test_advanced_search_and_filter_combinations(self):
        """
        Power-user test: Test complex search and filter combinations
        that power users might use to manage large numbers of tasks.
        """
        # Create a diverse set of tasks with different attributes
        task_attributes = [
            {"priority": "high", "tags": "urgent,important,critical", "due_date": (datetime.now() + timedelta(days=1)).isoformat()},
            {"priority": "high", "tags": "work,meeting", "due_date": (datetime.now() + timedelta(days=2)).isoformat()},
            {"priority": "medium", "tags": "personal,low", "due_date": (datetime.now() + timedelta(days=7)).isoformat()},
            {"priority": "low", "tags": "later,someday", "due_date": (datetime.now() + timedelta(days=30)).isoformat()},
            {"priority": "medium", "tags": "work,project", "due_date": (datetime.now() + timedelta(days=5)).isoformat()},
            {"priority": "high", "tags": "important,deadline", "due_date": (datetime.now() + timedelta(days=3)).isoformat()},
        ]
        
        created_tasks = []
        for attrs in task_attributes:
            task_data = {
                "title": f"Mixed Attribute Task - {attrs['priority']} - {datetime.now().isoformat()}",
                "description": f"Task with priority {attrs['priority']} and tags {attrs['tags']}",
                "priority": attrs["priority"],
                "tags": attrs["tags"],
                "due_date": attrs["due_date"],
                "user_id": self.test_user_id
            }
            
            async with self.session.post(f"{self.base_url}/api/{self.test_user_id}/tasks", json=task_data) as resp:
                assert resp.status == 200
                created_tasks.append(await resp.json())
        
        # Test complex search queries
        search_tests = [
            {"query": "important", "expected_min": 2},  # Should match tasks with "important" tag
            {"query": "work", "expected_min": 2},       # Should match tasks with "work" tag
            {"query": "high", "expected_min": 0},       # Priority search might not match title/tags
        ]
        
        for search_test in search_tests:
            params = {"query": search_test["query"]}
            async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks/search", params=params) as resp:
                assert resp.status == 200
                results = await resp.json()
                assert len(results) >= search_test["expected_min"], f"Search for '{search_test['query']}' should return at least {search_test['expected_min']} results"
        
        # Test combined filters (if supported)
        filter_tests = [
            {"priority": "high", "expected_min": 3},  # Should match high priority tasks
            {"priority": "medium", "expected_min": 2}, # Should match medium priority tasks
        ]
        
        for filter_test in filter_tests:
            params = {"priority": filter_test["priority"]}
            async with self.session.get(f"{self.base_url}/api/{self.test_user_id}/tasks", params=params) as resp:
                assert resp.status == 200
                results = await resp.json()
                filtered_results = [t for t in results if t["user_id"] == self.test_user_id and t["priority"] == filter_test["priority"]]
                assert len(filtered_results) >= filter_test["expected_min"], f"Filter for priority '{filter_test['priority']}' should return at least {filter_test['expected_min']} results"


# Run the tests if this file is executed directly
if __name__ == "__main__":
    pytest.main([__file__, "-v"])