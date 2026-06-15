def test_search_input_field_placeholder_text(search_page):
    """Verify search input field displays correct placeholder text"""
    assert search_page.is_search_input_field_visible(), "Search input field should be visible"

    expected_placeholder_text = "Search users, products, tasks..."
    actual_placeholder_text = search_page.get_search_input_placeholder_text()

    assert actual_placeholder_text == expected_placeholder_text, \
        "Search input field should display correct placeholder text to guide users on search scope"

    assert "users" in actual_placeholder_text, "Placeholder text should mention 'users' as searchable content"
    assert "products" in actual_placeholder_text, "Placeholder text should mention 'products' as searchable content"
    assert "tasks" in actual_placeholder_text, "Placeholder text should mention 'tasks' as searchable content"



def test_search_execution_with_valid_search_terms(search_page):
    """Verify search execution with valid search terms"""
    search_terms = ["user", "product", "task"]

    for search_term in search_terms:
        search_page.perform_search(search_term)
        search_page.page.wait_for_timeout(1000)

        assert search_page.verify_search_executed(search_term), \
            f"Search operation should be triggered and display results or 'no results found' message for term: {search_term}"

        has_results = search_page.is_search_results_heading_displayed()
        assert has_results, f"Search results heading message should be displayed for term: {search_term}"

        heading_text = search_page.get_search_results_heading_text()
        assert search_term in heading_text, \
            f"Search results heading should contain the search term: {search_term}"

    assert search_page.is_search_button_visible(), "Search button should be visible"
    assert search_page.is_search_button_clickable(), "Search button should be clickable"


def test_no_results_found_message_for_non_matching_queries(search_page):
    """Verify 'no results found' message display for non-matching queries"""
    non_matching_queries = ["xyz123", "nonexistent", "@#$%", "verylongnonmatchingquery", "NoMatch"]

    for query in non_matching_queries:
        search_page.perform_search(query)
        search_page.page.wait_for_timeout(1000)

        assert search_page.is_no_results_message_displayed(), \
            f"No results found message should be displayed for non-matching query: {query}"

        actual_message = search_page.get_no_results_message_text()
        assert len(actual_message) > 0, \
            f"No results found message text should not be empty for query: {query}"

        assert query in actual_message, \
            f"No results found message should contain the search query '{query}'. Actual message: {actual_message}"

        assert "no results found" in actual_message.lower(), \
            f"Message should contain 'no results found' text. Actual message: {actual_message}"

        assert len(actual_message) > len(query), \
            f"Message should provide more context than just the query term. Actual message: {actual_message}"

        has_proper_format = (f'"{query}"' in actual_message or
                             f"'{query}'" in actual_message or
                             query in actual_message)
        assert has_proper_format, \
            f"Message should properly format the query term. Expected format: 'No results found for \"{query}\"'. Actual: {actual_message}"

    assert search_page.is_search_button_visible(), "Search button should be visible"
    assert search_page.is_search_button_clickable(), "Search button should be clickable"