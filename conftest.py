import pytest

from pages.base_page import BasePage
from pages.dashboard_page import DashboardPage
from pages.orders_page import OrdersPage
from pages.product_management_page import ProductManagementPage
from pages.search_page import SearchPage
from pages.task_management_page import TaskManagementPage
from pages.theme_and_files_page import ThemeAndFilesPage
from pages.user_management_page import UserManagementPage

# Application URL Fixtures
@pytest.fixture
def app_base_url():
    """Base URL for the localhost application under test"""
    return "http://localhost:3000"


@pytest.fixture
def app_api_url():
    """API URL for the localhost application under test"""
    return "http://localhost:3000/api"


# Timeout Configuration Fixtures
@pytest.fixture
def localhost_timeout():
    """Timeout configuration for localhost testing"""
    return 15000  # 15 seconds - reasonable for localhost


# Test Data Fixtures
@pytest.fixture
def test_data():
    """Common test data for application testing"""
    return {
        "valid_titles": ["App", "Application", "Dashboard", "Home"],
        "error_patterns": ["error", "404", "500", "not found", "cannot connect", "timeout"],
        "success_patterns": ["welcome", "dashboard", "login", "home"],
        "api_endpoints": ["/health", "/status", "/api/v1", "/ping"]
    }


# Auto-navigation hook - runs before each test
@pytest.fixture(autouse=True)
def auto_navigate(page, app_base_url, localhost_timeout):
    """Automatically navigate to base URL before each test"""
    page.goto(app_base_url, timeout=localhost_timeout)
    page.wait_for_load_state('domcontentloaded', timeout=localhost_timeout)
    yield


# Page Object Model Fixtures
@pytest.fixture
def dashboard_page(page, localhost_timeout):
    """Dashboard page object"""
    return DashboardPage(page, localhost_timeout)


@pytest.fixture
def orders_page(page, localhost_timeout):
    """Orders page object - automatically navigates to orders page"""
    orders_page = OrdersPage(page, localhost_timeout)
    orders_page.navigate_to_orders_page()
    return orders_page


@pytest.fixture
def search_page(page, localhost_timeout):
    """Search page object - automatically navigates to search page"""
    search_page = SearchPage(page)
    search_page.navigate_to_search_page()
    return search_page

@pytest.fixture
def task_management_page(page, localhost_timeout):
    """Task management page object - automatically navigates to tasks page"""
    task_page = TaskManagementPage(page, localhost_timeout)
    task_page.navigate_to_tasks_page()
    return task_page

@pytest.fixture
def product_management_page(page, localhost_timeout):
    """Product management page object - automatically navigates to products page"""
    product_page = ProductManagementPage(page, localhost_timeout)
    product_page.navigate_to_products_page()
    return product_page

@pytest.fixture
def base_page(page, localhost_timeout):
    """Base page object with common functionality"""
    return BasePage(page, localhost_timeout)

@pytest.fixture
def theme_and_files_page(page, localhost_timeout):
    """Theme and files page object - automatically navigates to themes page"""
    theme_page = ThemeAndFilesPage(page, localhost_timeout)
    theme_page.navigate_to_themes_section()
    return theme_page

@pytest.fixture
def user_management_page(page, localhost_timeout):
    """User management page object - automatically navigates to users page"""
    user_page = UserManagementPage(page, localhost_timeout)
    user_page.navigate_to_users_page()
    return user_page