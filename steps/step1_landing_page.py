"""
Step 1: Landing Page Automation
Finds and clicks the "Get Started" button on the landing page
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step1LandingPage(BaseStep):
    """Step 1: Landing page automation"""
    
    def __init__(self, driver):
        super().__init__(driver, "Step 1: Landing Page")
        
        # Button selector for "Get Started" button
        self.get_started_button = {
            'css_selector': 'button[data-testid="button"][aria-label="Start passport renewal application"]',
            'xpath': '//button[@data-testid="button" and @aria-label="Start passport renewal application"]',
            'data_testid': 'button',
            'class_name': 'usa-button',
            'id': None
        }
    
    def execute(self):
        """
        Execute Step 1: Click the "Get Started" button
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Find and click the "Get Started" button
            success = self.find_and_click_button(
                self.get_started_button, 
                "Get Started button"
            )
            
            if success:
                logger.info("✅ Step 1 completed successfully - Get Started button clicked")
                
                # Wait 5 seconds as requested
                logger.info("Waiting 5 seconds...")
                time.sleep(5)
                
                return {
                    'status': True,
                    'code': 'SUCCESS',
                    'message': 'Step 1 completed successfully - Get Started button clicked'
                }
            else:
                logger.error("❌ Step 1 failed - Could not find or click Get Started button")
                return {
                    'status': False,
                    'code': 'GET_STARTED_BUTTON_FAILED',
                    'message': 'Could not find or click Get Started button'
                }
                
        except Exception as e:
            logger.error(f"❌ Step 1 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP1_EXCEPTION',
                'message': f'Step 1 failed with error: {str(e)}'
            }
