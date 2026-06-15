import pytest

# Test constants
EXPECTED_TOAST_MESSAGE = 'Please fill in all required fields: name, price, and category'
TEST_CATEGORY = 'Electronics'
SEARCH_TERM = 'Laptop'
SUCCESS = 'success'


# Simple product data structure to replace ProductsPage.Product class
class Product:
    def __init__(self, name, price, category, stock, description):
        self.name = name
        self.price = price
        self.category = category
        self.stock = stock
        self.description = description


invalid_product_data = [
    ('', '99.99', 'Electronics', '10', 'Test Description', 'Name required'),
    ('Test Product', '', 'Electronics', '10', 'Test Description', 'Price required'),
    ('Test Product', '99.99', '', '10', 'Test Description', 'Category required'),
    ('Test Product', '', '', '10', 'Test Description', 'Price must be positive'),
    ('', '', '', '01', 'Test Description', 'Stock required'),
    ('', '', 'Electronics', '-5', 'Test Description', 'Stock must be positive'),
    ('', 'invalid', '', '10', 'Test Description', 'Invalid price format'),
]


@pytest.mark.parametrize('name,price,category,stock,description,expectedValidation', invalid_product_data)
def test_product_form_validation(product_management_page, name, price, category, stock, description, expectedValidation):
    """Test product form validation with invalid data"""
    product = Product(name, price, category, stock, description)
    product_management_page.fill_product_form(product)
    product_management_page.submit_product_form()

    actual_message = product_management_page.get_toast_message()
    assert actual_message == EXPECTED_TOAST_MESSAGE, f"Expected validation message: '{EXPECTED_TOAST_MESSAGE}', got: '{actual_message}'"


def test_add_new_product_with_valid_details(product_management_page):
    """Test adding a new product with valid details"""
    product = Product('Test Laptop', '999.99', 'Electronics', '10', 'High-performance laptop for testing')
    product_management_page.fill_product_form(product)
    product_management_page.submit_product_form()

    notification_text = product_management_page.get_toast_message()
    assert SUCCESS in notification_text.lower(), f"Expected success notification, got: '{notification_text}'"

    page_content = product_management_page.get_page_content()
    assert product.name in page_content, f"Product '{product.name}' should appear in page content"


def test_product_category_filtering(product_management_page):
    """Test product category filtering functionality"""
    electronics_product = Product('Test Laptop', '999.99', 'Electronics', '5', 'Test electronics product')
    product_management_page.fill_product_form(electronics_product)
    product_management_page.submit_product_form()

    books_product = Product('Test Book', '29.99', 'Books', '10', 'Test books product')
    product_management_page.fill_product_form(books_product)
    product_management_page.submit_product_form()

    product_management_page.select_category_filter(TEST_CATEGORY)
    is_selected_category_product_visible = product_management_page.verify_products_from_category_shown(TEST_CATEGORY)
    assert is_selected_category_product_visible, f"Products from category '{TEST_CATEGORY}' should be visible after filtering"

    product_management_page.clear_category_filter()
    is_applied_filter_clear = product_management_page.verify_all_products_shown()
    assert is_applied_filter_clear, "All products should be visible after clearing filter"


def test_default_product_details(product_management_page):
    """Test default product details visibility"""
    is_default_product_exist = product_management_page.verify_default_product_exist()
    assert is_default_product_exist, "Default products should exist on the products page"


def test_product_search_functionality(product_management_page):
    """Test product search functionality"""
    product_management_page.search_product(SEARCH_TERM)
    actual_term = product_management_page.verify_search_results()

    assert SEARCH_TERM == actual_term, f"Search should work correctly for term: '{SEARCH_TERM}'"