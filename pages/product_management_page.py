from playwright.sync_api import expect
from pages.base_page import BasePage


class ProductManagementPage(BasePage):
    """Product Management page object with all product-related functionality"""

    def __init__(self, page, timeout=15000):
        super().__init__(page, timeout)

        # Product form selectors
        self.product_selector = "xpath=//button[contains(text(), 'Products')]"
        self.enter_product_name = "input[placeholder='Product Name']"
        self.product_price_selector = "input[placeholder='Price']"
        self.product_category_selector = "input[placeholder='Category']"
        self.product_stock_selector = "input[placeholder='Stock']"
        self.product_description_selector = "textarea[placeholder='Description']"
        self.submit_button_selector = "button[type='submit']"
        self.toast_selector = "div.Toastify__toast-container"
        self.select_filter_selector = 'select, div[role="combobox"]'
        self.product_card_selector = "div.product-card"
        self.all_products_selector = "text=/Electronics|Education|Home/i"
        self.search_input_selector = "input.product-search-input"

    def navigate_to_products_page(self):
        """Navigate to products page and wait for it to load"""
        files_themes_button = self.page.locator(self.product_selector)
        files_themes_button.click()
        self.page.wait_for_load_state('domcontentloaded')
        self.page.wait_for_selector('h1, h2')

    def is_page_loaded(self, timeout=None):
        """Check if orders page is loaded"""
        timeout = timeout or self.timeout
        self.page.wait_for_selector(self.enter_product_name, timeout=timeout)
        return self.page.locator(self.enter_product_name).is_visible()

    def fill_product_form(self, product):
        """Fill product form with given product data"""
        self.page.locator(self.enter_product_name)
        self.page.locator(self.enter_product_name).fill(product.name)
        price_input = self.page.locator(self.product_price_selector)
        input_type = price_input.get_attribute('type')
        if input_type == 'number' and product.price == 'invalid':
            self.page.evaluate(f"document.querySelector(\"{self.product_price_selector}\").value = '{product.price}'")
        else:
            price_input.fill(product.price)
        self.page.locator(self.product_category_selector).fill(product.category)
        self.page.locator(self.product_stock_selector).fill(product.stock)
        self.page.locator(self.product_description_selector).fill(product.description)

    def submit_product_form(self):
        """Submit the product form"""
        submit_button = self.page.locator(self.submit_button_selector)
        expect(submit_button).to_be_visible(timeout=5000)
        submit_button.first.click()

    def get_toast_message(self):
        """Get toast notification message"""
        self.page.wait_for_selector(self.toast_selector, timeout=5000)
        return self.page.locator(self.toast_selector).first.text_content()

    def get_page_content(self):
        return self.page.content()

    def select_category_filter(self, category):
        """Select category from filter dropdown"""
        select_element = self.page.locator(self.select_filter_selector)
        select_element.first.select_option(label=category)

    def verify_products_from_category_shown(self, category):
        """Verify products from selected category are shown"""
        self.page.wait_for_selector(self.product_card_selector, timeout=5000)
        category_elements = self.page.locator(self.product_card_selector)
        if category_elements.count() > 0:
            category_texts = category_elements.all_text_contents()
            lowered = category.lower()
            return any(lowered in text.lower() for text in category_texts)
        return False

    def clear_category_filter(self):
        """Clear category filter by selecting 'All Categories'"""
        select_element = self.page.locator('select')
        select_element.first.select_option(label='All Categories')

    def verify_all_products_shown(self):
        """Verify all product categories are shown"""
        category_indicators = self.page.locator(self.all_products_selector)
        return category_indicators.count() >= 2  # At least 2 different categories

    def verify_default_product_exist(self):
        product_cards = self.page.locator(self.product_card_selector)
        return product_cards.count() > 0

    def search_product(self, product_name):
        """Search for a product"""
        self.page.wait_for_selector(self.product_selector)
        # Find search input
        search_input = self.page.locator(self.search_input_selector)
        search_input.first.fill(product_name)

    def verify_search_results(self):
        """Verify search results and return the first product title"""
        self.page.wait_for_selector(self.product_card_selector, timeout=5000)
        first_product = self.page.locator(self.product_card_selector).first
        title_element = first_product.locator('h3')
        return title_element.first.inner_text()