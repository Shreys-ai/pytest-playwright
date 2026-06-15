def test_dashboard_page_and_navigation(dashboard_page, app_base_url, localhost_timeout, test_data):
    """Test dashboard page loading and navigation functionality"""
    is_loaded = dashboard_page.verify_dashboard_loaded(test_data)
    assert is_loaded, "Dashboard should be loaded with a valid title"

    buttons_present = dashboard_page.verify_navigation_buttons()
    assert buttons_present, "All navigation buttons should be present"


def test_backend_health_status_display(dashboard_page, app_base_url, localhost_timeout):
    """Test backend health status display on dashboard"""
    health_status_valid = dashboard_page.verify_health_status_display()
    assert health_status_valid, "Health status display should be valid"


def test_analytics_dashboard_functionality(dashboard_page, app_base_url, localhost_timeout):
    """Test analytics dashboard functionality and section visibility"""
    analytics_valid = dashboard_page.verify_analytics_dashboard_functionality()
    assert analytics_valid, "Analytics dashboard functionality should be valid"


def test_dashboard_tab_content_updates(dashboard_page, app_base_url, localhost_timeout):
    """Test dashboard tab content updates when navigating between sections"""
    content_updates_valid = dashboard_page.test_tab_content_updates()
    assert content_updates_valid, "Dashboard tab content should update correctly"