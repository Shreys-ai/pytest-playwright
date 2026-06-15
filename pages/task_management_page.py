from pages.base_page import BasePage


class TaskManagementPage(BasePage):
    """Task Management page object with all task-related functionality"""

    def __init__(self, page, timeout=15000):
        super().__init__(page, timeout)

        self.tasks_page_header_selector = 'h1, h2'
        self.task_management_selector = "xpath=//button[contains(text(), 'Tasks')]"
        self.option_selector = "form > select:nth-of-type(2)"
        self.task_title_selector = "input[placeholder='Task Title']"
        self.task_priority_selector = "form > select:nth-of-type(1)"
        self.submit_button_selector = "button[type='submit']"
        self.toast_selector = "div.Toastify__toast-container"
        self.user_option_selector = "form > select:nth-of-type(2) > option"

    def navigate_to_tasks_page(self):
        """Navigate to tasks page and wait for it to load"""
        tasks_link = self.page.locator(self.task_management_selector)
        tasks_link.click()
        self.page.wait_for_selector(self.tasks_page_header_selector)

    def is_page_loaded(self):
        """Check if orders page is loaded"""
        self.page.wait_for_selector(self.task_title_selector)
        return self.page.locator(self.task_title_selector).is_visible()

    def create_task_with_details(self, title, priority):
        """Create a task with given title and priority"""
        self.page.locator(self.task_title_selector).fill(title)
        self.page.locator(self.task_priority_selector).select_option(label=priority)
        
        # Select first available user (required field)
        self.page.locator(self.option_selector).select_option(value="1")
        
        self.page.locator(self.submit_button_selector).click()
        self.page.wait_for_timeout(1000)
        
        self.page.wait_for_selector(self.toast_selector, timeout=3000)
        notification_text = self.page.locator(self.toast_selector).text_content()
        return 'added' in notification_text.lower()

    def verify_task_in_list(self, title):
        """Verify task appears in the tasks list"""
        self.page.wait_for_timeout(2000)  # Wait for list to update
        task_locator = self.page.locator(f"xpath=//div[@class='task-item ']//h3[text()='{title}']")
        return task_locator.first.is_visible()

    def complete_task(self, title):
        """Complete a task by clicking its completion button"""
        try:
            complete_button = self.page.locator(f"xpath=//h3[text()='{title}']//parent::div//following-sibling::button")
            complete_button.first.click()
            self.page.wait_for_timeout(1000)  # Wait for completion to process
        except Exception as e:
            raise RuntimeError(f"Could not complete task: '{title}'. Check if the task exists and is clickable.") from e

    def verify_task_is_completed(self, title):
        """Verify task is marked as completed"""
        self.page.wait_for_timeout(2000)  # Wait for status update
        completed_task = self.page.locator(
            f"xpath=//h3[text()='{title}']//ancestor::div[contains(@class,'completed')]")
        return completed_task.is_visible()

    def create_task_with_user_assignment(self, title, priority, user_index):
        """Create a task with user assignment"""
        # Fill task form
        self.page.locator(self.task_title_selector).fill(title)
        self.page.locator(self.task_priority_selector).select_option(label=priority)

        # Select user assignment
        user_options = self.page.locator(self.user_option_selector).all()
        if len(user_options) > user_index:
            option_value = user_options[user_index].get_attribute('value')
            self.page.locator(self.option_selector).select_option(value=option_value)

        # Submit the form
        self.page.locator(self.submit_button_selector).click()