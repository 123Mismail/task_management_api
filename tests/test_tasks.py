import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app
from database import create_db_and_tables
from models import TaskStatus, TaskPriority


@pytest.fixture
def client():
    """Create a test client for the API"""
    create_db_and_tables()
    with TestClient(app) as test_client:
        yield test_client


def test_create_task(client):
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "priority": "medium"
    }

    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["status"] == "pending"
    assert data["priority"] == "medium"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.parametrize("priority", ["low", "medium", "high"])
def test_create_task_with_different_priorities(client, priority):
    """Test creating tasks with different priorities"""
    task_data = {
        "title": f"Task with {priority} priority",
        "description": f"Task with {priority} priority",
        "priority": priority
    }

    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201

    data = response.json()
    assert data["priority"] == priority


@pytest.mark.parametrize("status", ["pending", "in_progress", "completed"])
def test_create_task_with_different_statuses(client, status):
    """Test creating tasks with different statuses by updating after creation"""
    task_data = {
        "title": f"Task with {status} status",
        "description": f"Task with {status} status",
        "priority": "medium"
    }

    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201

    task_id = response.json()["id"]

    # Update the status
    update_data = {"status": status}
    update_response = client.put(f"/tasks/{task_id}", json=update_data)
    assert update_response.status_code == 200

    updated_data = update_response.json()
    assert updated_data["status"] == status


def test_get_tasks(client):
    """Test getting a list of tasks"""
    # First create a task
    task_data = {
        "title": "Get Tasks Test",
        "description": "Test for getting tasks",
        "priority": "high"
    }

    client.post("/tasks/", json=task_data)

    # Get all tasks
    response = client.get("/tasks/")
    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1
    assert any(task["title"] == "Get Tasks Test" for task in data)


def test_get_tasks_with_pagination(client):
    """Test getting tasks with pagination parameters"""
    # Create multiple tasks
    for i in range(5):
        task_data = {
            "title": f"Paginated Task {i}",
            "description": f"Task {i} for pagination test",
            "priority": "medium"
        }
        client.post("/tasks/", json=task_data)

    # Test with skip and limit
    response = client.get("/tasks/?skip=1&limit=3")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 3  # Should return 3 tasks


def test_get_tasks_with_multiple_tasks(client):
    """Test getting tasks when multiple exist"""
    # Create multiple tasks first
    for i in range(3):
        task_data = {
            "title": f"Multiple Task {i}",
            "description": f"Task {i} for multiple tasks test",
            "priority": "medium"
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201

    # Get all tasks
    response = client.get("/tasks/")
    assert response.status_code == 200

    data = response.json()
    # Should have at least 3 tasks (could be more from other tests)
    assert len(data) >= 3
    assert any(task["title"] == "Multiple Task 0" for task in data)
    assert any(task["title"] == "Multiple Task 1" for task in data)
    assert any(task["title"] == "Multiple Task 2" for task in data)


def test_create_task_validation_errors(client):
    """Test validation errors for task creation"""
    # Test with empty title
    invalid_task_data = {
        "title": "",  # Empty title should fail validation
        "description": "Test description",
        "priority": "medium"
    }

    response = client.post("/tasks/", json=invalid_task_data)
    assert response.status_code == 422  # Validation error

    # Test with title too long
    long_title = "a" * 256  # Exceeds max length of 255
    invalid_task_data = {
        "title": long_title,
        "description": "Test description",
        "priority": "medium"
    }

    response = client.post("/tasks/", json=invalid_task_data)
    assert response.status_code == 422  # Validation error

    # Test with invalid priority
    invalid_task_data = {
        "title": "Test Task",
        "description": "Test description",
        "priority": "invalid_priority"  # Should fail validation
    }

    response = client.post("/tasks/", json=invalid_task_data)
    assert response.status_code == 422  # Validation error


def test_get_task_by_id(client):
    """Test getting a specific task by ID"""
    # Create a task first
    task_data = {
        "title": "Specific Task",
        "description": "Test for specific task retrieval",
        "priority": "low"
    }

    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Get the specific task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Specific Task"
    assert data["description"] == "Test for specific task retrieval"


def test_update_task(client):
    """Test updating a task completely"""
    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Original description",
        "priority": "medium"
    }

    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": "in_progress",
        "priority": "high"
    }

    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Task"
    assert data["description"] == "Updated description"
    assert data["status"] == "in_progress"
    assert data["priority"] == "high"


def test_update_task_validation_errors(client):
    """Test validation errors for task updates"""
    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Original description",
        "priority": "medium"
    }

    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Test update with empty title
    invalid_update_data = {
        "title": ""  # Empty title should fail validation
    }

    response = client.put(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == 422  # Validation error

    # Test update with title too long
    long_title = "a" * 256  # Exceeds max length of 255
    invalid_update_data = {
        "title": long_title
    }

    response = client.put(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == 422  # Validation error

    # Test update with invalid status
    invalid_update_data = {
        "status": "invalid_status"  # Should fail validation
    }

    response = client.put(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == 422  # Validation error

    # Test update with invalid priority
    invalid_update_data = {
        "priority": "invalid_priority"  # Should fail validation
    }

    response = client.put(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == 422  # Validation error


def test_partial_update_task(client):
    """Test partially updating a task"""
    # Create a task first
    task_data = {
        "title": "Partial Update Task",
        "description": "Original description for partial update",
        "priority": "low"
    }

    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Partially update the task (only title)
    partial_update_data = {
        "title": "Partially Updated Task"
    }

    response = client.patch(f"/tasks/{task_id}", json=partial_update_data)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Partially Updated Task"
    assert data["description"] == "Original description for partial update"  # Should remain unchanged
    assert data["status"] == "pending"  # Should remain unchanged


def test_partial_update_task_validation_errors(client):
    """Test validation errors for partial task updates"""
    # Create a task first
    task_data = {
        "title": "Original Task",
        "description": "Original description",
        "priority": "medium"
    }

    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Test partial update with empty title
    invalid_update_data = {
        "title": ""  # Empty title should fail validation
    }

    response = client.patch(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == 422  # Validation error

    # Test partial update with title too long
    long_title = "a" * 256  # Exceeds max length of 255
    invalid_update_data = {
        "title": long_title
    }

    response = client.patch(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == 422  # Validation error

    # Test partial update with invalid status
    invalid_update_data = {
        "status": "invalid_status"  # Should fail validation
    }

    response = client.patch(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == 422  # Validation error

    # Test partial update with invalid priority
    invalid_update_data = {
        "priority": "invalid_priority"  # Should fail validation
    }

    response = client.patch(f"/tasks/{task_id}", json=invalid_update_data)
    assert response.status_code == 422  # Validation error


def test_delete_task(client):
    """Test deleting a task"""
    # Create a task first
    task_data = {
        "title": "Task to Delete",
        "description": "This task will be deleted",
        "priority": "medium"
    }

    create_response = client.post("/tasks/", json=task_data)
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Verify the task is gone
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_timestamps_consistency(client):
    """Test that timestamps are properly set and updated"""
    # Create a task
    task_data = {
        "title": "Timestamp Test Task",
        "description": "Task to test timestamps",
        "priority": "medium"
    }

    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201

    data = response.json()
    assert "created_at" in data
    assert "updated_at" in data

    original_created_at = data["created_at"]
    original_updated_at = data["updated_at"]

    task_id = data["id"]

    # Wait a moment and update the task
    import time
    time.sleep(0.01)  # Small delay to ensure timestamp difference

    update_data = {
        "title": "Updated Timestamp Test Task"
    }

    update_response = client.patch(f"/tasks/{task_id}", json=update_data)
    assert update_response.status_code == 200

    updated_data = update_response.json()
    assert updated_data["created_at"] == original_created_at  # Should remain the same
    assert updated_data["updated_at"] != original_updated_at  # Should be updated


def test_multiple_tasks_isolation(client):
    """Test that operations on one task don't affect others"""
    # Create multiple tasks
    tasks = []
    for i in range(3):
        task_data = {
            "title": f"Isolation Test Task {i}",
            "description": f"Task {i} for isolation test",
            "priority": "medium" if i % 2 == 0 else "high"
        }

        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201

        task_data = response.json()
        tasks.append(task_data)

    # Update only the second task
    update_data = {
        "title": "Updated Isolation Test Task 1",
        "status": "completed"
    }

    response = client.put(f"/tasks/{tasks[1]['id']}", json=update_data)
    assert response.status_code == 200

    updated_task = response.json()
    assert updated_task["title"] == "Updated Isolation Test Task 1"
    assert updated_task["status"] == "completed"

    # Verify other tasks remain unchanged
    for i, original_task in enumerate(tasks):
        if i != 1:  # Skip the updated task
            get_response = client.get(f"/tasks/{original_task['id']}")
            assert get_response.status_code == 200

            retrieved_task = get_response.json()
            assert retrieved_task["title"] == original_task["title"]  # Should be unchanged
            assert retrieved_task["status"] == original_task["status"]  # Should be unchanged


def test_get_nonexistent_task(client):
    """Test getting a task that doesn't exist"""
    response = client.get("/tasks/999999")
    assert response.status_code == 404


def test_update_nonexistent_task(client):
    """Test updating a task that doesn't exist"""
    update_data = {
        "title": "Updated Task",
        "description": "Updated description"
    }

    response = client.put("/tasks/999999", json=update_data)
    assert response.status_code == 404


def test_delete_nonexistent_task(client):
    """Test deleting a task that doesn't exist"""
    response = client.delete("/tasks/999999")
    assert response.status_code == 404


def test_health_check(client):
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_root_endpoint(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Task Management API"
    assert data["status"] == "running"