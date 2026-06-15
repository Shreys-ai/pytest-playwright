import pytest

# Test data matching TestNG framework
TEST_USER = "John Doe"
TEST_PRODUCT = "Laptop"

valid_order_data = [
    ("John Doe", "Laptop", "1"),
    ("Jane Smith", "Smartphone", "2"),
    ("Bob Johnson", "Headphones", "3"),
    ("John Doe", "Coffee Maker", "1"),
    ("Jane Smith", "Book", "5")
]


def test_orders_page_load_and_form_elements(orders_page):
    """Verify orders page loads with all form elements"""
    assert orders_page.is_page_loaded(), "Orders page should be loaded"
    assert orders_page.is_create_order_form_visible(), "Create order form should be visible"

    available_users = orders_page.get_available_users()
    assert len(available_users) > 0, "User dropdown should have options"

    available_products = orders_page.get_available_products()
    assert len(available_products) > 0, "Product dropdown should have options"


def test_create_order_with_valid_details(orders_page):
    """Test creating order with valid details"""
    initial_order_count = orders_page.get_orders_count()

    orders_page.create_order(TEST_USER, TEST_PRODUCT, "2")
    orders_page.page.wait_for_timeout(500)

    order_created = orders_page.is_order_created_successfully()
    assert order_created, "Order should be created successfully"

    final_order_count = orders_page.get_orders_count()
    assert final_order_count > initial_order_count, "Order count should increase after creating order"


@pytest.mark.parametrize('user,product,quantity', valid_order_data)
def test_create_order_with_different_products(orders_page, user, product, quantity):
    """Test order creation with different products"""
    initial_order_count = orders_page.get_orders_count()

    orders_page.create_order(user, product, quantity)
    orders_page.page.wait_for_timeout(500)

    order_created = orders_page.is_order_created_successfully()
    assert order_created, "Order should be created successfully"

    orders_page.page.wait_for_timeout(3000)
    final_order_count = orders_page.get_orders_count()
    assert final_order_count > initial_order_count, "Order count should increase after creating order"


def test_quantity_field_boundary_values(orders_page):
    """Test quantity field boundary values"""
    initial_order_count = orders_page.get_orders_count()

    orders_page.select_user(TEST_USER)
    orders_page.select_product(TEST_PRODUCT)
    orders_page.enter_quantity("0")
    orders_page.click_create_order()

    after_zero_count = orders_page.get_orders_count()
    assert initial_order_count == after_zero_count, "Zero quantity should be rejected"

    orders_page.clear_form()
    orders_page.select_user(TEST_USER)
    orders_page.select_product(TEST_PRODUCT)
    orders_page.enter_quantity("-1")
    orders_page.click_create_order()

    after_negative_count = orders_page.get_orders_count()
    assert initial_order_count == after_negative_count, "Negative quantity should be rejected"

    orders_page.clear_form()
    orders_page.select_user(TEST_USER)
    orders_page.select_product(TEST_PRODUCT)
    orders_page.enter_quantity("999")
    orders_page.click_create_order()
    orders_page.page.wait_for_timeout(1000)

    insufficient_stock_visible = orders_page.insufficient_stock_notification_visible()
    assert insufficient_stock_visible, "Large quantity should show insufficient stock message"


def test_multiple_order_creation(orders_page):
    """Test multiple order creation"""
    initial_order_count = orders_page.get_orders_count()

    orders_page.create_order("John Doe", "Laptop", "1")
    orders_page.page.wait_for_timeout(1000)
    first_order_count = orders_page.get_orders_count()

    orders_page.clear_form()
    orders_page.create_order("Jane Smith", "Smartphone", "2")
    orders_page.page.wait_for_timeout(1000)
    second_order_count = orders_page.get_orders_count()

    assert second_order_count > first_order_count, "Second order should increase the count"
    assert second_order_count >= initial_order_count + 2, "Should have at least 2 more orders than initial"