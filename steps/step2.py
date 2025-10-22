"""
Step 2: What You Need Page Automation
Finds and clicks the "Continue" button on the "What You Need" page
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step2WhatYouNeed(BaseStep):
    """Step 2: What You Need page automation"""
    
    def __init__(self, driver):
        super().__init__(driver, "Step 2: What You Need")
        
        # Button selector for "Continue" button
        self.continue_button = {
            'css_selector': 'button[data-testid="button"][type="button"]:not([aria-expanded])',
            'xpath': '//button[@data-testid="button" and @type="button" and not(@aria-expanded)]',
            'data_testid': 'button'
        }
    
    def execute(self):
        """
        Execute Step 2: Click the "Continue" button on What You Need page
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Find and click the "Continue" button
            success = self.find_and_click_button(
                self.continue_button, 
                "Continue button"
            )
            
            if success:
                logger.info("✅ Step 2 completed successfully - Continue button clicked")
                
                # Wait 5 seconds as requested
                logger.info("Waiting 5 seconds...")
                time.sleep(5)
                
                return True
            else:
                logger.error("❌ Step 2 failed - Could not find or click Continue button")
                return False
                
        except Exception as e:
            logger.error(f"❌ Step 2 failed with error: {str(e)}")
            return False
