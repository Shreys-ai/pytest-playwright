import requests
from playwright.sync_api import expect


def test_ApplicationSetupAndNavigation(page, app_base_url, localhost_timeout) -> None:
    """Test application setup and navigation functionality for localhost"""
    current_url = page.url
    assert app_base_url in current_url, f"Expected {app_base_url} to be in {current_url}"

    title = page.title()
    assert title is not None and len(title.strip()) > 0, f"Page title should not be empty, got: '{title}'"

    expect(page.locator('body')).to_be_visible(timeout=localhost_timeout)

    body_content = page.locator('body').text_content()
    assert body_content is not None and len(body_content.strip()) > 0, "Page should have meaningful content"

    error_indicators = page.locator('div[class*="error"], span[class*="error"], .error, [role="alert"]')
    error_count = error_indicators.count()
    assert error_count == 0, f"Found {error_count} error indicators on page: {error_indicators.all_text_contents()}"

def test_backend_api_configuration(page, app_base_url, app_api_url, localhost_timeout) -> None:
    """Test backend API configuration and connectivity for localhost"""
    current_url = page.url
    assert app_base_url in current_url, f"Expected {app_base_url} to be in {current_url}"

    assert 'localhost' in app_api_url, f"API URL should contain 'localhost', got: {app_api_url}"
    assert 'api' in app_api_url.lower(), f"API URL should contain 'api', got: {app_api_url}"

    try:
        response = requests.get(app_api_url, timeout=5)
        assert 200 <= response.status_code < 300, f"Unexpected status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        raise AssertionError(f"API endpoint unreachable at {app_api_url}: {str(e)}")
