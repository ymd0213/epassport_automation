"""
Step 12: Passport Delivery Page Automation
Handles passport delivery page by clicking Continue button
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step12PassportDelivery(BaseStep):
    """Step 12: Passport delivery page automation"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 12: Passport Delivery")
        self.passport_data = passport_data
        
        # Continue button
        self.continue_button = {
            'css_selector': 'button[type="submit"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="submit" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
    
    def execute(self):
        """
        Execute Step 12: Handle passport delivery page
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Click Continue button
            logger.info("Clicking Continue button on passport delivery page...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_CONTINUE_BUTTON_FAILED',
                    'message': 'We couldn\'t proceed with your request. Please try again.'
                }
            
            # Wait 2 seconds after clicking button
            time.sleep(2)
            
            # Check for errors after clicking continue
            logger.info("Checking for errors after clicking Continue...")
            error_result = self.check_for_page_errors()
            if error_result:
                return error_result
            
            logger.info("✅ Step 12 completed successfully - Passport delivery page submitted")
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 12 completed successfully - Passport delivery page submitted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 12 failed with error: {str(e)}")
            page_code = self.get_page_name_code()
            return {
                'status': False,
                'code': f'{page_code}_EXCEPTION',
                'message': 'We encountered an issue processing your request. Please try again.'
            }

