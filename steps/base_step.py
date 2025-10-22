"""
Base step class for passport automation steps
"""

import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


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
            logger.info(f"Looking for {description}...")
            
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
                        logger.info(f"Found {description} using {by}: {selector}")
                        break
                    except:
                        continue
            
            if button:
                # Scroll to button if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)
                
                # Click the button
                button.click()
                logger.info(f"✅ Successfully clicked {description}")
                return True
            else:
                logger.error(f"❌ Could not find {description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error clicking {description}: {str(e)}")
            return False
    
    def wait_for_page_load(self, timeout=10):
        """Wait for page to load completely"""
        try:
            self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
            logger.info("Page loaded completely")
            return True
        except Exception as e:
            logger.warning(f"Page load timeout: {str(e)}")
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
    
    def log_step_info(self):
        """Log current step information"""
        logger.info(f"=== {self.step_name} ===")
        logger.info(f"Page Title: {self.get_page_title()}")
        logger.info(f"Current URL: {self.get_current_url()}")
    
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
            logger.info(f"Looking for {description}...")
            
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
                        logger.info(f"Found {description} using {by}: {selector}")
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
                        logger.info(f"✅ Successfully input '{text}' into {description}")
                        return True
                    else:
                        logger.warning(f"Input verification failed: expected '{text}', got '{actual_value}'")
                        # Try one more time with a different approach
                        input_field.clear()
                        time.sleep(0.5)
                        input_field.click()  # Focus the field
                        time.sleep(0.5)
                        input_field.send_keys(text)
                        time.sleep(0.5)
                        actual_value = input_field.get_attribute("value")
                        if actual_value == text:
                            logger.info(f"✅ Successfully input '{text}' into {description} on retry")
                            return True
                        else:
                            logger.error(f"❌ Failed to input '{text}' into {description} after retry")
                            return False
                except Exception as e:
                    logger.warning(f"Could not verify input for {description}: {str(e)}")
                    logger.info(f"✅ Input '{text}' sent to {description} (verification skipped)")
                    return True
            else:
                logger.error(f"❌ Could not find {description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error inputting text into {description}: {str(e)}")
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
            logger.info(f"Looking for {description}...")
            
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
                        logger.info(f"Found {description} using {by}: {selector}")
                        break
                    except:
                        continue
            
            if select_field:
                from selenium.webdriver.support.ui import Select
                select = Select(select_field)
                select.select_by_value(option_value)
                logger.info(f"✅ Successfully selected option '{option_value}' in {description}")
                return True
            else:
                logger.error(f"❌ Could not find {description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error selecting option in {description}: {str(e)}")
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
            logger.info(f"Looking for {description}...")
            
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
                        logger.info(f"Found {description} using {by}: {selector}")
                        break
                    except:
                        continue
            
            if radio_button:
                # Scroll to radio button if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", radio_button)
                time.sleep(1)
                
                # Click the radio button
                radio_button.click()
                logger.info(f"✅ Successfully clicked {description}")
                return True
            else:
                logger.error(f"❌ Could not find {description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error clicking {description}: {str(e)}")
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
            logger.info(f"Looking for {description}...")
            
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
                        logger.info(f"Found {description} using {by}: {selector}")
                        break
                    except:
                        continue
            
            if checkbox:
                # Scroll to checkbox if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(1)
                
                # Click the checkbox
                checkbox.click()
                logger.info(f"✅ Successfully clicked {description}")
                return True
            else:
                logger.error(f"❌ Could not find {description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error clicking {description}: {str(e)}")
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
            logger.info(f"Looking for {description}...")
            
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
                        logger.info(f"Found {description} using {by}: {selector}")
                        break
                    except:
                        continue
            
            if combo_input:
                # Clear and type country name
                combo_input.clear()
                combo_input.send_keys(country_name)
                time.sleep(2)  # Wait for dropdown to appear
                
                # Find and click the first option in the dropdown
                try:
                    option_selector = f'[data-testid="combo-box-option-{country_name}"]'
                    option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, option_selector)))
                    option.click()
                    logger.info(f"✅ Successfully selected '{country_name}' from {description}")
                    return True
                except:
                    # Fallback: try to click first option in the list
                    try:
                        first_option = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid*="combo-box-option"]')))
                        first_option.click()
                        logger.info(f"✅ Successfully selected first option from {description}")
                        return True
                    except:
                        logger.error(f"❌ Could not find option for '{country_name}' in {description}")
                        return False
            else:
                logger.error(f"❌ Could not find {description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error selecting from {description}: {str(e)}")
            return False

    def execute(self):
        """
        Execute the step - to be implemented by subclasses
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        raise NotImplementedError("Subclasses must implement execute method")
