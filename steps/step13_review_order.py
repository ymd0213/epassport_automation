"""
Step 13: Review Your Order Page Automation
Handles review order page by clicking Continue button with specific selector
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step13ReviewOrder(BaseStep):
    """Step 13: Review order page automation"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 13: Review Order")
        self.passport_data = passport_data
        
        # Continue button - using more specific selector to avoid multiple buttons
        self.continue_button = {
            'css_selector': 'button[type="button"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="button" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
    
    def find_specific_continue_button(self):
        """
        Find the specific Continue button on review order page
        Since there are multiple buttons, we need to be more specific
        
        Returns:
            bool: True if button was found and clicked, False otherwise
        """
        try:
            logger.info("Looking for specific Continue button on review order page...")
            
            # Try to find the button that's most likely the main Continue button
            # Look for button with specific text content
            selectors = [
                # Try by text content first
                ('xpath', '//button[@type="button" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2") and contains(text(), "Continue")]'),
                # Try by position (usually the last or main button)
                ('xpath', '//button[@type="button" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2")][last()]'),
                # Try by CSS selector
                ('css selector', 'button[type="button"][data-testid="button"].usa-button.padding-y-2'),
                # Fallback to any button with Continue text
                ('xpath', '//button[contains(text(), "Continue")]')
            ]
            
            for by, selector in selectors:
                try:
                    from selenium.webdriver.common.by import By
                    from selenium.webdriver.support import expected_conditions as EC
                    
                    button = self.wait.until(EC.element_to_be_clickable((by, selector)))
                    logger.info(f"Found Continue button using {by}: {selector}")
                    
                    # Scroll to button if needed
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                    time.sleep(1)
                    
                    # Click the button
                    button.click()
                    logger.info("✅ Successfully clicked Continue button on review order page")
                    return True
                    
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {str(e)}")
                    continue
            
            logger.error("❌ Could not find Continue button on review order page")
            return False
            
        except Exception as e:
            logger.error(f"❌ Error finding Continue button: {str(e)}")
            return False
    
    def execute(self):
        """
        Execute Step 13: Handle review order page
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Click Continue button using specific method
            logger.info("Clicking Continue button on review order page...")
            if not self.find_specific_continue_button():
                logger.error("Failed to click Continue button")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_FAILED',
                    'message': 'Failed to click Continue button'
                }
            
            # Wait 5 seconds after clicking button
            time.sleep(5)
            
            # Check for errors after clicking continue
            logger.info("Checking for errors after clicking Continue...")
            error_result = self.check_for_page_errors("STEP13")
            if error_result:
                return error_result
            
            logger.info("✅ Step 13 completed successfully - Review order page submitted")
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 13 completed successfully - Review order page submitted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 13 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP13_EXCEPTION',
                'message': f'Step 13 failed with error: {str(e)}'
            }

