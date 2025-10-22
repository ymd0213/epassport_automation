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
                return {
                    'status': False,
                    'code': 'CHECKBOX_CLICK_FAILED',
                    'message': 'Failed to click terms and conditions checkbox'
                }
            
            # 2 second delay after checkbox click
            logger.info("Waiting 2 seconds after checkbox click...")
            time.sleep(2)
            
            # Click Continue button
            logger.info("Clicking Continue button...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_FAILED',
                    'message': 'Failed to click Continue button'
                }
            
            logger.info("✅ Step 5 completed successfully - Terms and conditions accepted")
            
            # Wait 5 seconds as requested
            logger.info("Waiting 5 seconds...")
            time.sleep(5)
            
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 5 completed successfully - Terms and conditions accepted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 5 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP5_EXCEPTION',
                'message': f'Step 5 failed with error: {str(e)}'
            }

