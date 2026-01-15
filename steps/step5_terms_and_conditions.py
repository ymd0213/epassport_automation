"""
Step 5: Terms and Conditions Page Automation
Handles terms and conditions acceptance and form submission
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step5TermsAndConditions(BaseStep):
    """Step 5: Terms and conditions page automation"""
    
    def __init__(self, driver):
        super().__init__(driver, "Step 5: Terms and Conditions")
        
        # Terms and conditions checkbox selector - targeting wrapper div
        self.terms_checkbox = {
            'css_selector': 'div[data-testid="checkbox"]:has(input[id="agree"])',
            'xpath': '//div[@data-testid="checkbox" and .//input[@id="agree"]]',
            'data_testid': 'checkbox'
        }
        
        # Continue button selector
        self.continue_button = {
            'css_selector': 'button[data-testid="button"][type="button"]',
            'xpath': '//button[@data-testid="button" and @type="button"]',
            'data_testid': 'button'
        }
    
    def execute(self):
        """
        Execute Step 5: Handle terms and conditions acceptance
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Click terms and conditions checkbox
            logger.info("Clicking terms and conditions checkbox...")
            if not self.find_and_click_checkbox(self.terms_checkbox, "terms and conditions checkbox"):
                logger.error("Failed to click terms and conditions checkbox")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_CHECKBOX_CLICK_FAILED',
                    'message': 'We couldn\'t accept the terms and conditions. Please try again.'
                }
            
            # 2 second delay after checkbox click
            logger.info("Waiting 2 seconds after checkbox click...")
            
            # Click Continue button
            logger.info("Clicking Continue button...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_CONTINUE_BUTTON_FAILED',
                    'message': 'We couldn\'t proceed with your request. Please try again.'
                }
            
            # Wait 2 seconds after clicking button
            logger.info("waiting 2 seconds after clicking Continue...")
            time.sleep(2)
            
            # Check for errors after clicking continue
            logger.info("Checking for errors after clicking Continue...")
            error_result = self.check_for_page_errors()
            if error_result:
                return error_result
            
            logger.info("✅ Step 5 completed successfully - Terms and conditions accepted")
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 5 completed successfully - Terms and conditions accepted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 5 failed with error: {str(e)}")
            page_code = self.get_page_name_code()
            return {
                'status': False,
                'code': f'{page_code}_EXCEPTION',
                'message': 'We encountered an issue processing your request. Please try again.'
            }

