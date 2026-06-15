import logging
import os


class BasePage:
    """Base page class with common functionality for all page objects"""

    def __init__(self, page, timeout=15000):
        self.page = page
        self.timeout = timeout
        # Enhanced framework features
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self.debug_mode = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))
        self.retry_delay = int(os.getenv('RETRY_DELAY', '1000'))
        self.toast_selector = "div.Toastify__toast-container"

        # Configure logger if not already configured
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO if not self.debug_mode else logging.DEBUG)

    def get_toast_message(self):
        """Get toast notification message"""
        self.page.wait_for_selector(self.toast_selector, timeout=3000)
        return self.page.locator(self.toast_selector).text_content()

    def verify_element_visible(self, primary_selector, fallback_selectors=None):
        """Verify element is visible with fallback strategies"""
        selectors = [primary_selector] + (fallback_selectors or [])

        for selector in selectors:
            element = self.page.locator(selector)
            if element.count() > 0 and element.first.is_visible():
                return True
        return False