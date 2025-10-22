"""
Step 10: Passport Options Page Automation
Handles passport options page by clicking Continue button
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step10PassportOptions(BaseStep):
    """Step 10: Passport options page automation"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 10: Passport Options")
        self.passport_data = passport_data
        
        # Continue button
        self.continue_button = {
            'css_selector': 'button[type="submit"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="submit" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
    
    def execute(self):
        """
        Execute Step 10: Handle passport options page
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Click Continue button
            logger.info("Clicking Continue button on passport options page...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                return False
            
            # Small delay to allow next page to load
            time.sleep(5)
            
            logger.info("✅ Step 10 completed successfully - Passport options page submitted")
            return True
            
        except Exception as e:
            logger.error(f"❌ Step 10 failed with error: {str(e)}")
            return False
