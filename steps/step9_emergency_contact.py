"""
Step 9: Emergency Contact Page Automation
Handles emergency contact page by clicking Continue button
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step9EmergencyContact(BaseStep):
    """Step 9: Emergency contact page automation"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 9: Emergency Contact")
        self.passport_data = passport_data
        
        # Continue button
        self.continue_button = {
            'css_selector': 'button[type="submit"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="submit" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
    
    def execute(self):
        """
        Execute Step 9: Handle emergency contact page
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Click Continue button
            logger.info("Clicking Continue button on emergency contact page...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_FAILED',
                    'message': 'Failed to click Continue button'
                }
            
            # Small delay to allow next page to load
            time.sleep(5)
            
            logger.info("✅ Step 9 completed successfully - Emergency contact page submitted")
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 9 completed successfully - Emergency contact page submitted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 9 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP9_EXCEPTION',
                'message': f'Step 9 failed with error: {str(e)}'
            }
