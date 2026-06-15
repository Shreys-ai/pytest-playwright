import re

from playwright.sync_api import expect

from pages.base_page import BasePage


class OrdersPage(BasePage):
    """Orders page object with all order-related functionality"""

    def __init__(self, page, timeout=15000):
        super().__init__(page, timeout)

        # Page Elements - Using same locator strategies as TestNG
        self.order_page_locator = "xpath=//button[contains(text(), 'Orders')]"
        self.create_order_title_selector = "//h2[contains(text(), 'Create New Order')]"
        self.user_dropdown_selector = "//option[text()='Select User']//parent::select"
        self.product_dropdown_selector = "xpath=//option[text()='Select Product']//parent::select"
        self.quantity_input_selector = "xpath=//input[@placeholder='Quantity']"
        self.create_order_button_selector = "xpath=//button[contains(text(), 'Create Order')]"
        self.orders_counter_selector = "xpath=//div[@class='orders-section']//h2"
        self.success_notification_selector = "div.Toastify__toast-icon"
        self.insufficient_stock_error_selector = "xpath=//div[text()='Error: Insufficient stock']"

    def navigate_to_orders_page(self):
        """Navigate to orders page and wait for it to load"""
        orders_link = self.page.locator(self.order_page_locator)

        expect(orders_link).to_be_visible()
        orders_link.click()
        self.page.wait_for_selector(self.create_order_title_selector)

    def is_page_loaded(self):
        """Check if orders page is loaded"""
        self.page.wait_for_selector(self.create_order_title_selector)
        return self.page.locator(self.create_order_title_selector).is_visible()

    def is_create_order_form_visible(self):
        """Check if create order form is visible with all elements"""
        # Check if all form elements are visible
        title_visible = self.page.locator(self.create_order_title_selector).is_visible()
        user_dropdown_visible = self.page.locator(self.user_dropdown_selector).is_visible()
        product_dropdown_visible = self.page.locator(self.product_dropdown_selector).is_visible()
        quantity_input_visible = self.page.locator(self.quantity_input_selector).is_visible()
        create_button_visible = self.page.locator(self.create_order_button_selector).is_visible()
        return title_visible and user_dropdown_visible and product_dropdown_visible and quantity_input_visible and create_button_visible

    def select_user(self, user_name):
        """Select user from dropdown"""
        dropdown = self.page.locator(self.user_dropdown_selector)
        dropdown.first.select_option(label=user_name)

    def select_product(self, product_name):
        """Select product from dropdown"""
        # Find the dropdown first
        dropdown = self.page.locator(self.product_dropdown_selector)

        # Find and select the option that contains the product name (partial match)
        product_option_selector = f"xpath=//option[text()='Select Product']//parent::select//option[contains(text(),'{product_name}')]"
        product_option = self.page.locator(product_option_selector)
        # Get the full text of the matching option
        option_text = product_option.first.text_content()
        # Select by the full label text
        dropdown.select_option(label=option_text)

    def enter_quantity(self, quantity):
        """Enter quantity in the input field"""
        quantity_input = self.page.locator(self.quantity_input_selector)
        quantity_input.first.fill(quantity)

    def click_create_order(self):
        """Click the create order button"""
        button = self.page.locator(self.create_order_button_selector)
        button.first.click()

    def create_order(self, user_name, product_name, quantity):
        """Create order with given details"""
        self.select_user(user_name)
        self.select_product(product_name)
        self.enter_quantity(quantity)
        self.click_create_order()

    def get_orders_count(self):
        """Get the current count of orders"""
        counter_element = self.page.locator(self.orders_counter_selector)
        counter_text = counter_element.first.text_content()
        # Extract number from text like "Orders (2)"
        numbers = re.findall(r'\d+', counter_text)
        if numbers:
            return int(numbers[0])
        return 0

    def is_order_created_successfully(self):
        notification = self.page.locator(self.success_notification_selector)
        return notification.first.is_visible()

    def clear_form(self):
        """Clear the order form"""
        # Reset user dropdown
        dropdown = self.page.locator(self.user_dropdown_selector)
        dropdown.first.select_option(label="Select User")

        # Reset product dropdown
        dropdown = self.page.locator(self.product_dropdown_selector)
        dropdown.first.select_option(label="Select Product")

        # Reset quantity to 1
        quantity_input = self.page.locator(self.quantity_input_selector)
        quantity_input.first.fill("1")

    def get_available_users(self):
        """Get list of available users from dropdown"""
        dropdown = self.page.locator(self.user_dropdown_selector)
        options = dropdown.locator('option').all()
        users = []
        for option in options:
            text = option.text_content()
            if text and text != "Select User":
                users.append(text)
        return users

    def get_available_products(self):
        """Get list of available products from dropdown"""
        dropdown = self.page.locator(self.product_dropdown_selector)
        options = dropdown.locator('option').all()
        products = []
        for option in options:
            text = option.text_content()
            if text and text != "Select Product":
                products.append(text)
        return products

    def insufficient_stock_notification_visible(self):
        """Check if insufficient stock error message is visible"""
        error_message = self.page.locator(self.insufficient_stock_error_selector)
        return error_message.first.is_visible()