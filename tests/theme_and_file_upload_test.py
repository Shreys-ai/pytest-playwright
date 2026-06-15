import pytest

valid_file_data = [
    ("image/jpeg", "test-document.jpg"),
    ("image/png", "test-document.png"),
    ("text/plain", "test-document.txt"),
    ("application/pdf", "test-document.pdf"),
]

@pytest.mark.parametrize("fileType,fileName", valid_file_data)
def test_file_upload_with_valid_files(theme_and_files_page, fileType, fileName):
    """Test file upload with various valid file types"""
    theme_and_files_page.perform_file_upload(fileName)

    is_file_detailed_display = theme_and_files_page.verify_file_details_display(fileName, fileType)
    assert is_file_detailed_display, f"File details should be displayed for {fileName}"

    is_uploaded_file_present_in_list = theme_and_files_page.verify_file_in_uploaded_list(fileName)
    assert is_uploaded_file_present_in_list, f"File {fileName} should appear in uploaded list"


def test_background_theme_selection(theme_and_files_page):
    """Test background theme selection functionality"""
    themes = ["Light Mode", "Default Dark", "Ocean Blue", "Royal Purple"]
    successful_themes = []

    for theme in themes:
        try:
            theme_and_files_page.select_background_theme(theme)
            theme_applied = theme_and_files_page.verify_theme_selection(theme)
            if theme_applied:
                successful_themes.append(theme)
        except Exception:
            continue

    assert len(successful_themes) > 0, "At least one theme should be selectable"


def test_image_file_upload_and_auto_background(theme_and_files_page):
    """Test image file upload and automatic background setting"""
    image_file_name = 'test-document.jpg'
    theme_and_files_page.perform_file_upload(image_file_name)

    actual_toast_message = theme_and_files_page.verify_file_uploaded_toast_message()
    assert actual_toast_message, "Toast message should be displayed after file upload"
    
    theme_and_files_page.select_uploaded_file()
    is_file_visible_in_background = theme_and_files_page.verify_upload_completion()
    assert is_file_visible_in_background, "File upload should be completed successfully"


def test_themes_and_files_section_functionality(theme_and_files_page):
    """Test themes and files section functionality"""
    is_theme_and_files_section_visible = theme_and_files_page.verify_themes_and_files_section_loaded()
    assert is_theme_and_files_section_visible, "Themes and files section should be loaded and visible"

    basic_theme_visible = theme_and_files_page.test_basic_themes_and_files_features()
    assert basic_theme_visible, "Basic themes and files features should be present"