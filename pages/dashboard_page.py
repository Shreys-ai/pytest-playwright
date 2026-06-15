from playwright.sync_api import expect

from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Dashboard page object with all dashboard-related functionality"""

    def __init__(self, page, timeout=15000):
        super().__init__(page, timeout)

        # Dashboard sections for analytics testing
        self.dashboard_sections = ["User", "Products", "Tasks", "Orders"]
        self.header = 'h1, h2'
        self.health_info = 'div.health-info'
        self.health_status_text = 'span.status-ok'
        # Navigation button selectors
        self.navigation_buttons = {
            "Dashboard": "xpath=//button[contains(text(), 'Dashboard')]",
            "Products": "xpath=//button[contains(text(), 'Products')]",
            "Orders": "xpath=//button[contains(text(), 'Orders')]",
            "Users": "xpath=//button[contains(text(), 'Users')]",
            "Tasks": "xpath=//button[contains(text(), 'Tasks')]"
        }
        self.analytics_section = 'div.analytics-section'
        self.body_of_page = 'domcontentloaded'

    def verify_dashboard_loaded(self, test_data):
        """Verify dashboard page is loaded with proper title"""
        self.page.wait_for_selector(self.header)
        title_locator = self.page.locator(self.header).first
        expect(title_locator).to_be_visible()
        actual_title = title_locator.text_content().strip()

        valid_titles = test_data["valid_titles"]
        title_is_valid = any(valid.lower() in actual_title.lower() for valid in valid_titles)

        is_valid_dashboard = bool(actual_title) and title_is_valid
        return is_valid_dashboard

    def verify_navigation_buttons(self):
        """Verify all navigation buttons are present"""
        missing_buttons = []

        for button_name, button_selector in self.navigation_buttons.items():
            button_locator = self.page.locator(button_selector)
            if not button_locator.is_visible():
                missing_buttons.append(button_name)

        return len(missing_buttons) == 0

    def verify_health_status_display(self):
        """Verify backend health status display on dashboard"""
        self.page.wait_for_selector(self.health_status_text)

        health_status_locator = self.page.locator(self.health_info)
        health_status_ok_locator = self.page.locator(self.health_status_text)

        is_health_status_displayed = health_status_locator.count() > 0 and health_status_ok_locator.count() > 0
        is_health_status_text_displayed = health_status_ok_locator.is_visible()

        return is_health_status_displayed and is_health_status_text_displayed

    def verify_analytics_dashboard_functionality(self):
        """Verify analytics dashboard functionality and section visibility"""
        analytics_section = self.page.locator(self.analytics_section)
        try:
            analytics_section.scroll_into_view_if_needed()
            expect(analytics_section).to_be_visible()
        except Exception:
            return False  # analytics section not found or not visible

        # Verify analytics subsections
        sections_found = []
        for section in self.dashboard_sections:
            section_locator = self.page.locator(
                f"xpath=//h3[contains(text(), '{section}')]//parent::div[@class='analytics-card']")
            try:
                expect(section_locator).to_be_visible(timeout=3000)
                sections_found.append(section)
            except Exception:
                continue

        return bool(sections_found)

    def test_tab_content_updates(self):
        """Test dashboard tab content updates when navigating between sections"""
        dashboard_content = self.page.content()

        products_link = self.page.locator(self.navigation_buttons["Products"])
        products_link.click()
        self.page.wait_for_load_state(self.body_of_page)
        self.page.wait_for_timeout(500)

        products_content = self.page.content()
        content_changed = dashboard_content != products_content

        # Navigate back to Dashboard
        dashboard_link = self.page.locator(self.navigation_buttons["Dashboard"])
        dashboard_link.click()
        self.page.wait_for_load_state(self.body_of_page)
        dashboard_loaded = self.page.locator(self.header).first.is_visible()

        return content_changed and dashboard_loaded