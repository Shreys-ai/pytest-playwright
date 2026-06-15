import time

import pytest

USER_ADDED_TOAST_MESSAGE = 'user added successfully'


valid_user_data = [
    ('John Doe', 'Admin'),
    ('Jane Smith', 'User'),
    ('Bob Johnson', 'User')
]

invalid_user_data = [
    ('', 'test@example.com', 'User', 'Name required'),
    ('Test User', '', 'User', 'Email required'),
    ('Test User', 'invalid-email', 'User', 'Valid email required'),
    ('Test User', 'test@example.com', '', 'Role required'),
    ('', '', '', 'All fields required')
]

@pytest.mark.parametrize('name,role', valid_user_data)
def test_add_new_user_with_valid_details(user_management_page, name, role):
    """Test adding new user with valid details"""
    timestamp = int(time.time() * 1000)
    email = f"{name.lower().replace(' ', '.')}{timestamp}@example.com"
    unique_name = name + f" {timestamp}"

    initial_user_count = user_management_page.get_user_count()
    user_management_page.enter_user_details(unique_name, email, role)
    user_management_page.submit_user_form()

    actual_toast_message = user_management_page.get_toast_message()
    assert USER_ADDED_TOAST_MESSAGE in actual_toast_message.lower(), f"Expected success message in: {actual_toast_message}"

    user_management_page.page.wait_for_timeout(1000)
    is_user_present_in_list = user_management_page.verify_user_in_list(unique_name, email)
    assert is_user_present_in_list, f"User {unique_name} should appear in the users list"

    final_user_count = user_management_page.get_user_count()
    assert final_user_count > initial_user_count, "User count should increase after adding user"


@pytest.mark.parametrize('name,email,role,expectedValidation', invalid_user_data)
def test_user_form_validation(user_management_page, name, email, role, expectedValidation):
    """Test user form validation with invalid data"""
    user_management_page.attempt_to_add_user_with_validation(name, email, role)

    is_validation_displayed = user_management_page.verify_form_validation_message(expectedValidation)
    assert is_validation_displayed, f"Form validation message should be displayed for: {expectedValidation}"

def test_delete_user_from_list(user_management_page):
    """Test deleting user from list"""
    check_existing_user_count = user_management_page.ensure_user_exists_for_deletion()
    assert check_existing_user_count, "At least one user should exist for deletion testing"

    delete_successful = user_management_page.delete_user_from_list(1)
    user_management_page.page.wait_for_timeout(1000)
    
    assert delete_successful is not False, "User deletion should be attempted successfully"


def test_user_form_field_interactions(user_management_page):
    """Test user form field interactions"""
    name = 'Test Name'
    entered_value = user_management_page.test_name_field_interaction(name)
    assert entered_value == name, f"Name field should accept and retain value: {name}"

    email = 'test@example.com'
    entered_value = user_management_page.test_email_field_interaction(email)
    assert entered_value == email, f"Email field should accept and retain value: {email}"

    user_management_page.test_role_field_interaction()
    user_management_page.test_complete_form_flow()

    actual_toast_message = user_management_page.get_toast_message()
    assert USER_ADDED_TOAST_MESSAGE in actual_toast_message.lower(), f"Expected success message in: {actual_toast_message}"


def test_refresh_users_functionality(user_management_page):
    """Test refresh users functionality"""
    initial_user_count = user_management_page.get_user_count()
    user_management_page.click_refresh_users_button()
    users_list_visible = user_management_page.verify_users_list_after_refresh()
    assert users_list_visible, "Users list should be visible after refresh"

    refreshed_user_count = user_management_page.get_user_count()
    assert initial_user_count == refreshed_user_count, "User count should remain same after refresh"


def test_user_list_display_and_structure(user_management_page):
    """Test user list display and structure"""
    is_list_structure_present = user_management_page.verify_user_list_structure()
    assert is_list_structure_present, "User list structure should be present"

    is_user_list_present = user_management_page.verify_user_list_columns()
    assert is_user_list_present, "User list columns should be present"

    user_management_page.test_user_list_interactions()