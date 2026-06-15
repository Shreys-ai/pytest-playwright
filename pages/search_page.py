import time

from playwright.sync_api import expect

from pages.base_page import BasePage


class SearchPage(BasePage):
    """Search page object with all search-related functionality"""

    def __init__(self, page, timeout=15000):
        super().__init__(page, timeout)

        # Page Elements - Using same locator strategies as TestNG
        self.search_page_navigation = "xpath=//button[contains(text(), 'Search')]"
        self.search_heading_selector = "xpath=//h2[contains(text(), 'Search')]"
        self.search_input_field_selector = "xpath=//input[@placeholder='Search users, products, tasks...']"
        self.search_button_selector = "xpath=//form//button[contains(text(), 'Search')] | //div[contains(@class, 'search')]//button[contains(text(), 'Search')]"
        self.search_results_heading_selector = "xpath=//h3[contains(text(), 'Search Results for')]"
        self.no_results_message_selector = "xpath=//p[contains(text(), 'No results found')]"

    def navigate_to_search_page(self):
        """Navigate to orders page and wait for it to load"""
        search_link = self.page.locator(self.search_page_navigation)

        expect(search_link).to_be_visible()
        search_link.click()
        self.page.wait_for_selector(self.search_heading_selector)

    def is_page_loaded(self):
        """Check if search page is loaded"""
        self.page.wait_for_selector(self.search_heading_selector)
        return self.page.locator(self.search_heading_selector).is_visible()

    def is_search_input_field_visible(self):
        """Check if search input field is visible"""
        return self.page.locator(self.search_input_field_selector).is_visible()

    def get_search_input_placeholder_text(self):
        """Get the placeholder text of the search input field"""
        input_field = self.page.locator(self.search_input_field_selector)
        return input_field.first.get_attribute('placeholder')

    def is_search_button_visible(self):
        """Check if search button is visible"""
        return self.page.locator(self.search_button_selector).is_visible()

    def is_search_button_clickable(self, timeout=None):
        """Check if search button is clickable"""
        button = self.page.locator(self.search_button_selector)
        if button.count() > 0:
            expect(button.first).to_be_enabled(timeout=timeout)
            return True
        return False

    def click_search_button(self):
        """Click the search button"""
        button = self.page.locator(self.search_button_selector)
        button.last.click()  # Use last button to avoid navigation button

    def enter_search_text(self, search_text):
        """Enter text in the search input field"""
        input_field = self.page.locator(self.search_input_field_selector)
        input_field.first.fill(search_text)

    def is_search_results_heading_displayed(self):
        """Check if search results heading is displayed"""
        return self.page.locator(self.search_results_heading_selector).is_visible()

    def get_search_results_heading_text(self):
        """Get the text of the search results heading"""
        heading = self.page.locator(self.search_results_heading_selector)
        return heading.first.text_content()

    def is_no_results_message_displayed(self):
        """Check if no results message is displayed"""
        return self.page.locator(self.no_results_message_selector).is_visible()

    def get_no_results_message_text(self):
        """Get the text of the no results message"""
        message = self.page.locator(self.no_results_message_selector)
        return message.first.text_content()

    def perform_search(self, search_term):
        """Perform search operation with given search term"""
        self.enter_search_text(search_term)
        self.click_search_button()
        time.sleep(2)  # Allow time for search operation
        return self

    def verify_search_executed(self, search_term):
        """Verify that search was executed for the given search term"""
        if self.is_search_results_heading_displayed():
            heading_text = self.get_search_results_heading_text()
            return search_term in heading_text

        # Alternative check - if no results message is displayed with the search term
        if self.is_no_results_message_displayed():
            message_text = self.get_no_results_message_text()
            if search_term in message_text:
                return True

        return False