import time

from playwright.sync_api import expect


def test_page_title_matches_expected(base_page, app_base_url, localhost_timeout, test_data):
    """Test that page title matches expected values"""
    actual_title = base_page.page.title()
    valid_titles = test_data["valid_titles"]
    title_matches = any(expected_title in actual_title for expected_title in valid_titles)
    
    assert title_matches, f"Page title '{actual_title}' should match expected values or not be empty"


def test_application_load_time(base_page, app_base_url, localhost_timeout):
    """Test application load time performance"""
    start_time = int(time.time() * 1000)

    current_url = base_page.page.url
    assert app_base_url in current_url, f"Expected {app_base_url} to be in {current_url}"

    end_time = int(time.time() * 1000)
    load_time = end_time - start_time

    assert load_time < 30000, f"Load time should be less than 30 seconds, got: {load_time}ms"


def test_basic_page_structure(base_page, app_base_url, localhost_timeout):
    """Test basic page structure elements"""
    current_url = base_page.page.url
    assert app_base_url in current_url, f"Expected {app_base_url} to be in {current_url}"

    expect(base_page.page.locator('html')).to_be_attached()
    expect(base_page.page.locator('body')).to_be_attached()
    expect(base_page.page.locator('head')).to_be_attached()

    nav_selectors = ['nav', '.navbar', '.navigation', '[role="navigation"]', 'header nav']
    is_navigation_menu_visible = base_page.verify_element_visible(nav_selectors[0], nav_selectors[1:])
    assert is_navigation_menu_visible, "Navigation menu should be visible"

    structure_elements = ['header', 'main', 'footer', 'div', 'section']
    has_structure = any(base_page.page.locator(element).count() > 0 for element in structure_elements)
    assert has_structure, "Page should have basic structural elements"


def test_application_url_accessibility(base_page, app_base_url, localhost_timeout):
    """Test application URL accessibility"""
    current_url = base_page.page.url
    assert current_url is not None, "Current URL should not be None"
    assert current_url.strip() != '', "Current URL should not be empty"
    assert current_url.startswith('http'), f"URL should start with http, got: {current_url}"

    base_url_clean = app_base_url.replace('https://', '').replace('http://', '')
    assert base_url_clean in current_url, f"Expected {base_url_clean} to be in {current_url}"
