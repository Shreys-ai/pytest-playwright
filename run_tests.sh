#!/usr/bin/env bash
set -e

echo "Setting up test environment..."

# Create virtual environment
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install Playwright browsers
playwright install

echo ""
echo "Running tests locally..."
pytest tests/ -n 10 -v

echo ""
echo "Running tests on BrowserStack..."
browserstack-sdk pytest tests/ -n 10 -v

deactivate
echo ""
echo "Tests completed!"
