"""
Base step class for passport automation steps
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BaseStep:
    """Base class for all automation steps"""
    
    def __init__(self, driver, step_name):
        """
        Initialize the base step
        
        Args:
            driver: WebDriver instance
            step_name (str): Name of the step for logging
        """
        self.driver = driver
        self.step_name = step_name
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, element_selector, description="element"):
        """
        Find an element using various selector strategies
        
        Args:
            element_selector (dict): Dictionary containing selector strategies
            description (str): Description of the element for logging
            
        Returns:
            WebElement: The found element, or None if not found
        """
        try:
            # Try different selector strategies
            selectors = []
            
            # Add selectors in order of specificity
            if element_selector.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, element_selector.get('css_selector')))
            
            if element_selector.get('xpath'):
                selectors.append((By.XPATH, element_selector.get('xpath')))
            
            # Add data-testid selector using CSS selector
            if element_selector.get('data_testid'):
                selectors.append((By.CSS_SELECTOR, f'[data-testid="{element_selector.get("data_testid")}"]'))
            
            if element_selector.get('class_name'):
                selectors.append((By.CLASS_NAME, element_selector.get('class_name')))
            
            if element_selector.get('id'):
                selectors.append((By.ID, element_selector.get('id')))
            
            element = None
            for by, selector in selectors:
                if selector:
                    try:
                        element = self.wait.until(EC.presence_of_element_located((by, selector)))
                        return element
                    except:
                        continue
            
            return None
                
        except Exception as e:
            return None
    
    def find_and_click_button(self, button_selector, description="button"):
        """
        Find and click a button using various selector strategies
        
        Args:
            button_selector (dict): Dictionary containing selector strategies
            description (str): Description of the button for logging
            
        Returns:
            bool: True if button was found and clicked, False otherwise
        """
        try:
            # Try different selector strategies
            selectors = []
            
            # Add selectors in order of specificity
            if button_selector.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, button_selector.get('css_selector')))
            
            if button_selector.get('xpath'):
                selectors.append((By.XPATH, button_selector.get('xpath')))
            
            # Add data-testid selector using CSS selector
            if button_selector.get('data_testid'):
                selectors.append((By.CSS_SELECTOR, f'[data-testid="{button_selector.get("data_testid")}"]'))
            
            if button_selector.get('class_name'):
                selectors.append((By.CLASS_NAME, button_selector.get('class_name')))
            
            if button_selector.get('id'):
                selectors.append((By.ID, button_selector.get('id')))
            
            # Add some generic fallback selectors (more specific to avoid expandable buttons)
            selectors.extend([
                (By.CSS_SELECTOR, 'button[data-testid="button"]:not([aria-expanded])'),
                (By.CSS_SELECTOR, 'button.usa-button:not([aria-expanded])'),
                (By.CSS_SELECTOR, 'button[type="button"]:not([aria-expanded])'),
                (By.CSS_SELECTOR, 'button[data-testid="button"]'),
                (By.CSS_SELECTOR, 'button.usa-button'),
                (By.CSS_SELECTOR, 'button[type="button"]')
            ])
            
            button = None
            for by, selector in selectors:
                if selector:
                    try:
                        button = self.wait.until(EC.element_to_be_clickable((by, selector)))
                        break
                    except:
                        continue
            
            if button:
                # Scroll to button if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)
                
                # Click the button
                button.click()
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            return True
        except Exception as e:
            return False
    
    def get_page_title(self):
        """Get current page title"""
        try:
            return self.driver.title
        except:
            return "Unknown"
    
    def get_current_url(self):
        """Get current page URL"""
        try:
            return self.driver.current_url
        except:
            return "Unknown"
    
    def get_page_name(self):
        """
        Extract page name from step_name (removes "Step X: " prefix)
        
        Returns:
            str: Page name (e.g., "Passport Photo Upload" from "Step 7: Passport Photo Upload")
        """
        if not self.step_name:
            return "Unknown Page"
        # Remove "Step X: " prefix if present
        import re
        page_name = re.sub(r'^Step \d+:\s*', '', self.step_name)
        return page_name.strip()
    
    def get_page_name_code(self):
        """
        Get page name in code format (uppercase, spaces replaced with underscores)
        
        Returns:
            str: Page name code (e.g., "PASSPORT_PHOTO_UPLOAD")
        """
        page_name = self.get_page_name()
        # Convert to uppercase and replace spaces with underscores
        code = page_name.upper().replace(' ', '_')
        return code
    
    def log_step_info(self):
        """Log current step information"""
        pass
    
    def find_and_input_text(self, input_selector, text, description="input field"):
        """
        Find and input text into a field
        
        Args:
            input_selector (dict): Dictionary containing selector strategies
            text (str): Text to input
            description (str): Description of the input field for logging
            
        Returns:
            bool: True if input was successful, False otherwise
        """
        try:
            # Try different selector strategies
            selectors = []
            
            if input_selector.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, input_selector.get('css_selector')))
            
            if input_selector.get('xpath'):
                selectors.append((By.XPATH, input_selector.get('xpath')))
            
            if input_selector.get('data_testid'):
                selectors.append((By.CSS_SELECTOR, f'[data-testid="{input_selector.get("data_testid")}"]'))
            
            if input_selector.get('id'):
                selectors.append((By.ID, input_selector.get('id')))
            
            input_field = None
            for by, selector in selectors:
                if selector:
                    try:
                        input_field = self.wait.until(EC.presence_of_element_located((by, selector)))
                        break
                    except:
                        continue
            
            if input_field:
                # Clear existing text and input new text
                input_field.clear()
                time.sleep(0.5)  # Brief pause after clearing
                input_field.send_keys(text)
                time.sleep(0.5)  # Brief pause after input
                
                # Verify the input was actually entered
                try:
                    actual_value = input_field.get_attribute("value")
                    if actual_value == text:
                        return True
                    else:
                        # Try one more time with a different approach
                        input_field.clear()
                        time.sleep(0.5)
                        input_field.click()  # Focus the field
                        time.sleep(0.5)
                        input_field.send_keys(text)
                        time.sleep(0.5)
                        actual_value = input_field.get_attribute("value")
                        if actual_value == text:
                            return True
                        else:
                            return False
                except Exception as e:
                    return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def find_and_select_option(self, select_selector, option_value, description="select field"):
        """
        Find and select an option from a dropdown
        
        Args:
            select_selector (dict): Dictionary containing selector strategies
            option_value (str): Value of the option to select
            description (str): Description of the select field for logging
            
        Returns:
            bool: True if selection was successful, False otherwise
        """
        try:
            # Try different selector strategies
            selectors = []
            
            if select_selector.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, select_selector.get('css_selector')))
            
            if select_selector.get('xpath'):
                selectors.append((By.XPATH, select_selector.get('xpath')))
            
            if select_selector.get('data_testid'):
                selectors.append((By.CSS_SELECTOR, f'[data-testid="{select_selector.get("data_testid")}"]'))
            
            if select_selector.get('id'):
                selectors.append((By.ID, select_selector.get('id')))
            
            select_field = None
            for by, selector in selectors:
                if selector:
                    try:
                        select_field = self.wait.until(EC.presence_of_element_located((by, selector)))
                        break
                    except:
                        continue
            
            if select_field:
                from selenium.webdriver.support.ui import Select
                select = Select(select_field)
                select.select_by_value(option_value)
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def find_and_click_radio(self, radio_selector, description="radio button"):
        """
        Find and click a radio button
        
        Args:
            radio_selector (dict): Dictionary containing selector strategies
            description (str): Description of the radio button for logging
            
        Returns:
            bool: True if click was successful, False otherwise
        """
        try:
            # Try different selector strategies
            selectors = []
            
            if radio_selector.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, radio_selector.get('css_selector')))
            
            if radio_selector.get('xpath'):
                selectors.append((By.XPATH, radio_selector.get('xpath')))
            
            if radio_selector.get('data_testid'):
                selectors.append((By.CSS_SELECTOR, f'[data-testid="{radio_selector.get("data_testid")}"]'))
            
            if radio_selector.get('id'):
                selectors.append((By.ID, radio_selector.get('id')))
            
            radio_button = None
            for by, selector in selectors:
                if selector:
                    try:
                        radio_button = self.wait.until(EC.element_to_be_clickable((by, selector)))
                        break
                    except:
                        continue
            
            if radio_button:
                # Scroll to radio button if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
                time.sleep(1)
                
                # Click the radio button
                radio_button.click()
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def find_and_click_checkbox(self, checkbox_selector, description="checkbox"):
        """
        Find and click a checkbox
        
        Args:
            checkbox_selector (dict): Dictionary containing selector strategies
            description (str): Description of the checkbox for logging
            
        Returns:
            bool: True if click was successful, False otherwise
        """
        try:
            # Try different selector strategies
            selectors = []
            
            if checkbox_selector.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, checkbox_selector.get('css_selector')))
            
            if checkbox_selector.get('xpath'):
                selectors.append((By.XPATH, checkbox_selector.get('xpath')))
            
            if checkbox_selector.get('data_testid'):
                selectors.append((By.CSS_SELECTOR, f'[data-testid="{checkbox_selector.get("data_testid")}"]'))
            
            if checkbox_selector.get('id'):
                selectors.append((By.ID, checkbox_selector.get('id')))
            
            checkbox = None
            for by, selector in selectors:
                if selector:
                    try:
                        checkbox = self.wait.until(EC.element_to_be_clickable((by, selector)))
                        break
                    except:
                        continue
            
            if checkbox:
                # Scroll to checkbox if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(1)
                
                # Click the checkbox
                checkbox.click()
                return True
            else:
                return False
                
        except Exception as e:
            return False
    
    def find_and_select_combo_box(self, combo_selector, country_name, description="combo box"):
        """
        Find and select from a combo box (like country selection)
        
        Args:
            combo_selector (dict): Dictionary containing selector strategies
            country_name (str): Name of the country to select
            description (str): Description of the combo box for logging
            
        Returns:
            bool: True if selection was successful, False otherwise
        """
        try:
            # Try different selector strategies
            selectors = []
            
            if combo_selector.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, combo_selector.get('css_selector')))
            
            if combo_selector.get('xpath'):
                selectors.append((By.XPATH, combo_selector.get('xpath')))
            
            if combo_selector.get('data_testid'):
                selectors.append((By.CSS_SELECTOR, f'[data-testid="{combo_selector.get("data_testid")}"]'))
            
            if combo_selector.get('id'):
                selectors.append((By.ID, combo_selector.get('id')))
            
            combo_input = None
            for by, selector in selectors:
                if selector:
                    try:
                        combo_input = self.wait.until(EC.presence_of_element_located((by, selector)))
                        break
                    except:
                        continue
            
            if combo_input:
                # Clear and type country name
                combo_input.clear()
                combo_input.send_keys(country_name)
                time.sleep(0.5)  # Wait for dropdown to appear
                
                # Find and click the first option in the dropdown
                try:
                    option_selector = f'[data-testid="combo-box-option-{country_name}"]'
                    option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, option_selector)))
                    option.click()
                    return True
                except:
                    # Fallback: try to click first option in the list
                    try:
                        first_option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid*="combo-box-option"]')))
                        first_option.click()
                        return True
                    except:
                        return False
            else:
                return False
                
        except Exception as e:
            return False
    
    def find_and_select_state_combo_box(self, combo_selector, state_code, state_name, description="state combo box"):
        """
        Find and select from a state combo box (uses state code in data-testid)
        
        Args:
            combo_selector (dict): Dictionary containing selector strategies  
            state_code (str): 2-letter state code (e.g., "KS" for Kansas)
            state_name (str): Full state name (e.g., "Kansas")
            description (str): Description of the combo box for logging
            
        Returns:
            bool: True if selection was successful, False otherwise
        """
        try:
            # Try different selector strategies to find the input field
            selectors = []
            
            if combo_selector.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, combo_selector.get('css_selector')))
            
            if combo_selector.get('xpath'):
                selectors.append((By.XPATH, combo_selector.get('xpath')))
            
            if combo_selector.get('data_testid'):
                selectors.append((By.CSS_SELECTOR, f'[data-testid="{combo_selector.get("data_testid")}"]'))
            
            if combo_selector.get('id'):
                selectors.append((By.ID, combo_selector.get('id')))
            
            combo_input = None
            for by, selector in selectors:
                if selector:
                    try:
                        combo_input = self.wait.until(EC.presence_of_element_located((by, selector)))
                        break
                    except:
                        continue
            
            if combo_input:
                # Clear and type state name
                combo_input.clear()
                time.sleep(0.3)
                combo_input.send_keys(state_name)
                time.sleep(0.5)  # Wait for dropdown to appear and filter
                
                # Try to find and click the option using state code in data-testid
                try:
                    # First try: use state code in data-testid (e.g., combo-box-option-KS)
                    option_selector = f'[data-testid="combo-box-option-{state_code}"]'
                    option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, option_selector)))
                    option.click()
                    return True
                except:
                    # Second try: Find option by data-value attribute
                    try:
                        option_selector = f'li[data-value="{state_code}"]'
                        option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, option_selector)))
                        option.click()
                        return True
                    except:
                        # Third try: Press Enter to select the first filtered option
                        try:
                            from selenium.webdriver.common.keys import Keys
                            combo_input.send_keys(Keys.ENTER)
                            return True
                        except:
                            # Fourth try: Find any visible option in the list
                            try:
                                visible_option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.usa-combo-box__list-option:not([hidden])')))
                                visible_option.click()
                                return True
                            except:
                                return False
            else:
                return False
                
        except Exception as e:
            return False

    def check_for_page_errors(self, step_name=None):
        """
        Check for error messages on the page after an action
        
        Args:
            step_name (str, optional): Name of the step for error code. If None, uses page name code.
            
        Returns:
            dict or None: Error dict if error found, None if no errors
        """
        # Use page name code if step_name not provided
        if step_name is None:
            step_name = self.get_page_name_code()
        
        try:
            # Wait a moment for any errors to appear
            time.sleep(1)
            
            # Look for any usa-alert element
            try:
                alert_element = self.driver.find_element(By.CSS_SELECTOR, "div.usa-alert")
                if alert_element and alert_element.is_displayed():
                    # Check if it has usa-alert--success class
                    alert_classes = alert_element.get_attribute("class")
                    
                    if "usa-alert--success" in alert_classes:
                        # This is a success alert, not an error
                        return None  # This is success, not error
                    else:
                        # This is an error or warning alert
                        error_text = alert_element.text.strip()
                        if error_text:
                            return {
                                'status': False,
                                'code': f'{step_name}_ERROR',
                                'message': error_text
                            }
            except Exception as e:
                pass
            
            # Look for inline error messages with errorMessage testid
            try:
                error_spans = self.driver.find_elements(By.CSS_SELECTOR, 'span[data-testid="errorMessage"]')
                error_messages = []
                for error_span in error_spans:
                    if error_span.is_displayed():
                        text = error_span.text.strip()
                        if text:
                            error_messages.append(text)
                
                if error_messages:
                    error_message = ", ".join(error_messages)
                    return {
                        'status': False,
                        'code': f'{step_name}_VALIDATION_ERROR',
                        'message': error_message
                    }
            except Exception as e:
                pass
            
            # No errors found
            return None
            
        except Exception as e:
            return None
    
    def execute(self):
        """
        Execute the step - to be implemented by subclasses
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        raise NotImplementedError("Subclasses must implement execute method")
