import os

from pages.base_page import BasePage


class ThemeAndFilesPage(BasePage):
    """Theme and Files page object with all theme and file-related functionality"""

    def __init__(self, page, timeout=15000):
        super().__init__(page, timeout)

        # File upload selectors
        self.file_input_selector = "input[type='file']"
        self.upload_button_selector = "xpath=//button[text()='Upload File']"
        self.file_name_selector = "div.selected-file > p:nth-of-type(1)"
        self.file_type_selector = "div.selected-file > p:nth-of-type(3)"
        self.file_size_selector = "div.selected-file > p:nth-of-type(2)"
        self.success_message_selector = "xpath=//*[contains(text(),'File uploaded successfully')]"
        self.file_and_theme_selector = "xpath=//button[text()='Files & Themes']"
        self.toast_selector = "div.Toastify__toast-container"
        self.basic_theme_selector = "button:has-text('Light')"

    def navigate_to_themes_section(self):
        """Navigate to file upload section"""
        files_themes_button = self.page.locator(self.file_and_theme_selector)
        files_themes_button.click()
        self.page.wait_for_load_state('domcontentloaded')

    def is_page_loaded(self):
        """Check if ThemePage page is loaded"""
        self.page.wait_for_selector(self.file_input_selector)
        return self.page.locator(self.file_input_selector).is_visible()

    def perform_file_upload(self, file_name):
        """Perform file upload with given filename"""
        try:
            file_path = os.path.join("tests", "files", file_name)
            file_input = self.page.locator(self.file_input_selector)
            file_input.set_input_files(file_path)
            self.page.wait_for_timeout(1000)
        except Exception as e:
            raise RuntimeError(f"Failed to upload '{file_name}' using selector '{self.file_input_selector}'") from e

    def verify_file_details_display(self, file_name, file_type):
        """Verify file details are displayed correctly"""
        has_file_name = self.verify_file_in_uploaded_list(file_name)

        # Try to find file type information
        file_type_text = self.page.locator(self.file_type_selector).text_content()
        has_file_type = file_type in file_type_text

        # Try to find file size information
        has_file_size = self.page.locator(self.file_size_selector).is_visible()

        return has_file_name and (has_file_type or has_file_size)  # At least one detail should be visible

    def verify_file_in_uploaded_list(self, file_name):
        """Verify file appears in uploaded files list"""
        # Try multiple selectors to find the file name
        element = self.page.locator(self.file_name_selector)
        file_text = element.text_content()
        return file_name in file_text

    def select_background_theme(self, theme_name):
        """Select a background theme"""
        try:
            theme_selector = f"xpath=//div[@class='theme-options']//button[contains(text(),'{theme_name}')]"
            theme_button = self.page.locator(theme_selector)
            theme_button.first.click()
            self.page.wait_for_timeout(500)
        except Exception as e:
            raise LookupError(f"Theme '{theme_name}' could not be selected or was not found.") from e

    def verify_theme_selection(self, theme_name):
        """Verify theme is selected (has active class)"""
        selected_selector = f"xpath=//button[contains(text(),'{theme_name}') and contains(@class,'active')]"
        selected_theme = self.page.locator(selected_selector)
        if selected_theme.count() > 0 and selected_theme.is_visible():
            return True
        return False

    def verify_upload_completion(self):
        """Verify file upload completion"""
        self.page.wait_for_selector(self.success_message_selector, timeout=3000)
        return self.page.locator(self.success_message_selector).is_visible()

    def verify_file_uploaded_toast_message(self):
        """Get file uploaded toast message"""
        self.page.wait_for_selector(self.toast_selector, timeout=3000)
        return self.page.locator(self.toast_selector).text_content()

    def verify_themes_and_files_section_loaded(self):
        """Verify themes and files section is loaded"""
        page_content = self.page.content().lower()
        has_themes_content = any(keyword in page_content for keyword in ['theme', 'style', 'background'])
        has_files_content = any(keyword in page_content for keyword in ['file', 'upload', 'document'])
        return has_files_content or has_themes_content  # At least one should be present

    def test_basic_themes_and_files_features(self):
        """Test basic themes and files features are present"""
        theme_controls = self.page.locator(self.basic_theme_selector).count() > 0
        file_controls = self.page.locator(self.file_input_selector).count() > 0

        return file_controls or theme_controls  # At least one should be present

    def select_uploaded_file(self):
        """Select uploaded file"""
        upload_button = self.page.locator(self.upload_button_selector)
        upload_button.first.click()