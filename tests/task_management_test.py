from datetime import datetime

import pytest

HIGH_PRIORITY = 'High Priority'
MEDIUM_PRIORITY = 'Medium Priority'

task_priority_data = [
    ('High Priority', 'High priority task for urgent items'),
    ('Medium Priority', 'Medium priority task for normal items'),
    ('Low Priority', 'Low priority task for non-urgent items'),
]


@pytest.mark.parametrize('priority,title', task_priority_data)
def test_task_creation_with_different_priorities(task_management_page, priority, title):
    """Test creating tasks with different priority levels"""
    is_task_created_toast_present = task_management_page.create_task_with_details(title, priority)
    assert is_task_created_toast_present, f"Task creation toast should be present for {priority}"

    is_new_task_created = task_management_page.verify_task_in_list(title)
    assert is_new_task_created, f"Task '{title}' should appear in the tasks list"


def test_create_new_task_with_assignment(task_management_page):
    """Test creating a new task with assignment"""
    title = 'Test Task'
    is_task_created_toast_present = task_management_page.create_task_with_details(title, HIGH_PRIORITY)
    assert is_task_created_toast_present, "Task creation toast should be present"

    is_new_task_created = task_management_page.verify_task_in_list(title)
    assert is_new_task_created, f"Task '{title}' should appear in the tasks list"


def test_complete_existing_task(task_management_page):
    """Test completing an existing task"""
    timestamp = str(int(datetime.now().timestamp()))
    title = f'Task to Complete {timestamp}'
    is_task_created_toast_present = task_management_page.create_task_with_details(title, MEDIUM_PRIORITY)
    assert is_task_created_toast_present, "Task creation toast should be present"

    is_new_task_created = task_management_page.verify_task_in_list(title)
    assert is_new_task_created, f"Task '{title}' should be created before completion"

    task_management_page.complete_task(title)
    is_completed_task_verified = task_management_page.verify_task_is_completed(title)
    assert is_completed_task_verified, f"Task '{title}' should be marked as completed"

def test_task_assignment_functionality(task_management_page):
    """Test task assignment functionality"""
    timestamp = str(int(datetime.now().timestamp()))
    title = f'Assignment Test Task {timestamp}'
    task_management_page.create_task_with_user_assignment(title, HIGH_PRIORITY, 1)

    is_new_task_created = task_management_page.verify_task_in_list(title)
    assert is_new_task_created, f"Assigned task '{title}' should appear in the tasks list"