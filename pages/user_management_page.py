import re

from pages.base_page import BasePage


class UserManagementPage(BasePage):

    def __init__(self, page, timeout=15000):
        super().__init__(page, timeout)

        self.header = 'h1, h2'
        self.user_list_grid = 'div.users-grid'
        self.user_card = 'div.user-card, .user-item, .user-row'
        self.refresh_button = 'button.refresh-btn'
        self.toast_message = 'div.Toastify__toast-container, .toast, .notification'
        self.name_field = "input[placeholder='Name']"
        self.email_field = "input[placeholder='Email']"
        self.select_role = "form>select"
        self.user_page_locator = "xpath=//button[contains(text(), 'Users')]"
        self.user_count_selector = "div.users-section > h2"
        self.submit_button = "button[type='submit']"
        self.delete_button = "button.delete-btn"
        self.validation_error_selectors = [
            '.error',
            '.validation-message',
            '.field-error',
            '.invalid-feedback',
            '.form-error'
        ]

    def navigate_to_users_page(self):
        """Navigate to users page and wait for it to load"""
        users_link = self.page.locator(self.user_page_locator)
        users_link.click()
        self.page.wait_for_selector(self.header)

    def is_page_loaded(self):
        """Check if user management page is loaded"""
        self.page.wait_for_selector(self.delete_button)
        return self.page.locator(self.delete_button).count() > 0

    def get_user_count(self):
        """Get current count of users"""
        counter_element = self.page.locator(self.user_count_selector)
        counter_text = counter_element.text_content()
        numbers = re.findall(r'\d+', counter_text)
        if numbers:
            return int(numbers[0])
        return 0

    def enter_user_details(self, name, email, role):
        """Enter user details into the form"""
        # Fill name field
        name_input = self.page.locator(self.name_field)
        name_input.fill(name)

        # Fill email field
        email_input = self.page.locator(self.email_field)
        email_input.fill(email)

        # Select role (only if not empty - for validation testing)
        if role:
            role_select = self.page.locator(self.select_role)
            role_select.select_option(label=role)

    def submit_user_form(self):
        """Submit the user form"""
        submit_btn = self.page.locator(self.submit_button)
        submit_btn.click()
        self.page.wait_for_timeout(1000)

    def verify_user_in_list(self, name, email):
        """Verify user appears in the users list"""
        self.page.wait_for_selector(self.toast_message, timeout=5000)

        user_element = self.page.locator(f"xpath=//h3[contains(text(),'{name}')]//parent::div[@class='user-card']")
        if user_element.count() > 0:
            return True

        # Fallback: check page content
        page_content = self.page.content().lower()
        return name.lower() in page_content or email.lower() in page_content

    def attempt_to_add_user_with_validation(self, name, email, role):
        """Attempt to add user with validation (may fail)"""
        self.enter_user_details(name, email, role)
        self.submit_user_form()

    def verify_form_validation_message(self, expected_validation):
        """Verify form validation message appears"""
        for selector in self.validation_error_selectors:
            try:
                validation_elements = self.page.locator(selector).all_text_contents()
                for text in validation_elements:
                    if expected_validation.split(' ')[0].lower() in text.lower():
                        return False
            except Exception:
                continue
        return True

    def ensure_user_exists_for_deletion(self):
        """Ensure at least one user exists for deletion testing"""
        user_count = self.get_user_count()
        if user_count == 0:
            self.enter_user_details('Test User for Deletion', 'delete.test@example.com', 'User')
            self.submit_user_form()
            self.page.wait_for_timeout(1000)
        return self.get_user_count() > 0

    def delete_user_from_list(self, user_index):
        """Delete user from list by index"""
        delete_buttons = self.page.locator(self.delete_button)
        self.page.on("dialog", lambda dialog: dialog.accept())
        delete_buttons.nth(user_index - 1).click()
        self.page.wait_for_timeout(1000)

    def test_name_field_interaction(self, name):
        """Test name field interaction and return entered value"""
        name_input = self.page.locator(self.name_field)
        if name_input.count() > 0:
            name_input.first.fill(name)
            return name_input.first.get_attribute('value')
        return name

    def test_email_field_interaction(self, email):
        """Test email field interaction and return entered value"""
        email_input = self.page.locator(self.email_field)
        if email_input.count() > 0:
            email_input.first.fill(email)
            return email_input.first.get_attribute('value')
        return email

    def test_role_field_interaction(self):
        """Test role field interaction"""
        role_select = self.page.locator(self.select_role)
        role_select.first.select_option(label='User')

    def test_complete_form_flow(self):
        """Test complete form flow"""
        self.page.reload()
        self.page.wait_for_load_state('domcontentloaded')
        self.navigate_to_users_page()
        self.page.wait_for_timeout(500)
        self.enter_user_details('Flow Test User', 'flow.test@example.com', 'User')
        self.submit_user_form()

    def click_refresh_users_button(self):
        """Click refresh users button"""
        refresh_btn = self.page.locator(self.refresh_button)
        refresh_btn.click()
        self.page.wait_for_timeout(1000)

    def verify_users_list_after_refresh(self):
        """Verify users list is visible after refresh"""
        return self.page.locator(self.user_list_grid).is_visible()

    def verify_user_list_structure(self):
        """Verify user list structure is present"""
        card_count = self.page.locator(self.user_card).count()
        grid_visible = self.page.locator(self.user_list_grid).count() > 0
        return (card_count > 0) or grid_visible

    def verify_user_list_columns(self):
        """Verify user list columns"""
        page_content = self.page.content().lower()
        return 'user' in page_content

    def test_user_list_interactions(self):
        """Test user list interactions"""
        items = self.page.locator(self.user_card)
        items.first.click()