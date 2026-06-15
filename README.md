# Pytest-Playwright-BrowserStack Test Automation Framework

A comprehensive Pytest-based automation framework with Playwright for modern web application testing, featuring parallel execution, Page Object Model, and BrowserStack integration for cross-browser cloud testing.

## 🚀 Features

- ✅ **Multi-Browser Support**: Chromium, Firefox, WebKit (Safari), Chrome, Edge
- ✅ **BrowserStack Integration**: Cloud testing on 3000+ browser/OS combinations
- ✅ **Page Object Model**: Well-structured page objects for maintainable tests
- ✅ **Pytest Integration**: Powerful testing framework with fixtures and plugins
- ✅ **Parallel Execution**: Run tests in parallel for faster execution with pytest-xdist
- ✅ **Playwright Power**: Fast, reliable, and modern browser automation
- ✅ **Cross-Platform**: Windows, macOS, Linux support
- ✅ **Local & Cloud**: Run tests locally or on BrowserStack cloud
- ✅ **CI/CD Ready**: Optimized for continuous integration pipelines

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **pip**: Python package manager
- **Git**: For version control
- **BrowserStack Account**: Valid username and access key (for cloud execution)
- **Internet Connection**: For Playwright browsers and BrowserStack

## 🚀 Quick Start

### Automated Setup (Recommended)

Run the automated setup script that handles everything:

```bash
./run_tests.sh
```

This script will:
1. Create virtual environment
2. Install all dependencies
3. Install Playwright browsers
4. Run tests locally (10 parallel workers)
5. Run tests on BrowserStack (10 parallel workers)

### Manual Setup

1. **Create Virtual Environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows
```

2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

3. **Install Playwright Browsers**:
```bash
playwright install
```

4. **Configure BrowserStack**: 
Set environment variables or update `browserstack.yml`:
```bash
export BROWSERSTACK_USERNAME="your_username"
export BROWSERSTACK_ACCESS_KEY="your_access_key"
```

## 🧪 Running Tests

### Local Execution

```bash
# Run all tests locally with 10 parallel workers
pytest tests/ -n 10 -v

# Run specific test file
pytest tests/user_management_test.py -v

# Run specific test
pytest tests/user_management_test.py::test_add_new_user_with_valid_details -v
```

### BrowserStack Execution

```bash
# Run all tests on BrowserStack with 10 parallel workers
browserstack-sdk pytest tests/ -n 10 -v

# Run specific test file on BrowserStack
browserstack-sdk pytest tests/dashboard_test.py -v
```

### Using the Automated Script

```bash
# Run complete test suite (local + BrowserStack)
./run_tests.sh
```

## 📁 Project Structure

```
pytest-playwright-browserstack/
├── pages/                      # Page Object Model classes
│   ├── base_page.py           # Base page with common methods
│   ├── dashboard_page.py      # Dashboard page object
│   ├── orders_page.py         # Orders page object
│   ├── product_management_page.py
│   ├── search_page.py
│   ├── task_management_page.py
│   ├── theme_and_files_page.py
│   └── user_management_page.py
├── tests/                      # Test files
│   ├── application_setup_test.py
│   ├── dashboard_test.py
│   ├── order_management_test.py
│   ├── product_management_test.py
│   ├── search_functionality_test.py
│   ├── simple_application_test.py
│   ├── task_management_test.py
│   ├── theme_and_file_upload_test.py
│   └── user_management_test.py
├── conftest.py                 # Pytest configuration and fixtures
├── browserstack.yml            # BrowserStack configuration
├── requirements.txt            # Python dependencies
└── run_tests.sh               # Automated setup and execution script
```

## ⚙️ Configuration

### BrowserStack Configuration (`browserstack.yml`)

Key configuration options:

- **Platforms**: Define OS, browser, and version combinations
- **Parallel Execution**: Set `parallelsPerPlatform` for concurrent tests
- **Local Testing**: Enable `browserstackLocal` for testing local applications
- **Framework Settings**: Configure Pytest-specific settings

### Pytest Configuration (`conftest.py`)

The framework includes:

- **Fixtures**: Reusable test components and page objects
- **Browser Management**: Automatic browser setup with Playwright
- **Base URL Configuration**: Centralized URL management
- **Timeout Settings**: Customizable timeout values
- **Page Object Fixtures**: Pre-configured page objects with navigation

## 🔧 Test Orchestration & Smart Selection

### For Mono Repo Approach
- Ensure that the **`source`** keyword is commented out in `browserstack.yml`
- Both development code and automation code should reside in a single repository
- If no development code is present, the system will consider the automation code's Git directory

### For Git Cloning Approach
- The development repository should be cloned locally
- Ensure that the **`source`** keyword is used in `browserstack.yml`
- Development repository URLs should be provided in **array** format
- Verify you have switched to a different repository with at least one commit against the **main** branch
- Run tests using: `browserstack-sdk pytest tests/`

### For GitHub App Approach
- Complete GitHub integration through BrowserStack using the same credentials
- The **`test.json`** path should be specified under the **`source`** key as a **string** in `browserstack.yml`
- Ensure configuration is provided in **JSON** format
- Run tests using: `browserstack-sdk pytest tests/`

## 📚 Additional Resources

- **Playwright Documentation**: [Playwright Python Guide](https://playwright.dev/python/)
- **Pytest Documentation**: [Pytest Framework](https://docs.pytest.org/)
- **BrowserStack Documentation**: [BrowserStack Automate](https://www.browserstack.com/docs/automate)
- **BrowserStack SDK**: [BrowserStack SDK Documentation](https://github.com/browserstack/browserstack-sdk)