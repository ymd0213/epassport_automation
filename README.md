# Web Automation Script with Selenium

A Python-based web automation framework using Selenium WebDriver for automating web interactions like form filling, clicking, and navigation.

## Features

- **Easy Setup**: Automatic ChromeDriver management
- **Flexible Locators**: Support for multiple element locator strategies
- **Error Handling**: Comprehensive logging and error management
- **Configurable**: Customizable settings for different use cases
- **Examples**: Ready-to-use example scripts for common scenarios

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Chrome Browser**: Make sure you have Google Chrome installed on your system.

## Quick Start

### Basic Usage

```python
from web_automation import WebAutomation

# Initialize automation
automation = WebAutomation(headless=False)

try:
    # Setup driver
    automation.setup_driver()
    
    # Navigate to a webpage
    automation.navigate_to_url("https://example.com")
    
    # Find and interact with elements
    automation.input_text("id", "username", "your_username")
    automation.input_text("id", "password", "your_password")
    automation.click_element("id", "login-button")
    
    # Take a screenshot
    automation.take_screenshot("result.png")
    
finally:
    # Always close the driver
    automation.close_driver()
```

### Running Examples

```bash
# Run the main example
python web_automation.py

# Run specific examples
python example_scripts.py
```

## Available Methods

### Navigation
- `navigate_to_url(url)` - Navigate to a specific URL
- `get_page_title()` - Get the current page title

### Element Interaction
- `find_element(locator_type, locator_value)` - Find an element
- `click_element(locator_type, locator_value)` - Click an element
- `input_text(locator_type, locator_value, text)` - Input text into an element

### Waiting
- `wait_for_element_visible(locator_type, locator_value)` - Wait for element to be visible

### Utilities
- `take_screenshot(filename)` - Take a screenshot
- `close_driver()` - Close the browser

## Locator Types

The script supports these locator types:

- `id` - Element ID
- `name` - Element name attribute
- `class_name` - CSS class name
- `xpath` - XPath expression
- `css_selector` - CSS selector
- `tag_name` - HTML tag name
- `link_text` - Link text
- `partial_link_text` - Partial link text

## Configuration

Edit `config.py` to customize:

- Headless mode (run browser in background)
- Wait timeouts
- Chrome options
- Logging settings

## Example Scenarios

### 1. Google Search
```python
automation.navigate_to_url("https://www.google.com")
automation.input_text("name", "q", "search term")
automation.click_element("name", "btnK")
```

### 2. Form Filling
```python
automation.input_text("id", "username", "john_doe")
automation.input_text("id", "email", "john@example.com")
automation.click_element("id", "submit-btn")
```

### 3. Login Automation
```python
automation.input_text("name", "username", "your_username")
automation.input_text("name", "password", "your_password")
automation.click_element("xpath", "//button[@type='submit']")
```

## Troubleshooting

### Common Issues

1. **ChromeDriver not found**: The script automatically downloads ChromeDriver, but ensure you have internet access.

2. **Element not found**: 
   - Check if the locator is correct
   - Increase wait timeout
   - Ensure the page has loaded completely

3. **Browser crashes**: 
   - Try running in headless mode
   - Check available system memory
   - Update Chrome browser

### Debug Mode

Enable debug logging by modifying the logging level in `config.py`:

```python
LOGGING_CONFIG = {
    'level': 'DEBUG',  # Change from 'INFO' to 'DEBUG'
    # ...
}
```

## File Structure

```
├── web_automation.py      # Main automation class
├── example_scripts.py     # Example usage scenarios
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Best Practices

1. **Always close the driver** in a `finally` block
2. **Use explicit waits** instead of `time.sleep()` when possible
3. **Handle exceptions** gracefully
4. **Take screenshots** for debugging
5. **Use meaningful locators** (prefer ID and name over XPath when possible)

## License

This project is open source and available under the MIT License.
