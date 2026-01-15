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
                
                # Wait 1 seconds as requested
                # logger.info("waiting 1 seconds...")
                time.sleep(1)
                
                return {
                    'status': True,
                    'code': 'SUCCESS',
                    'message': 'Step 1 completed successfully - Get Started button clicked'
                }
            else:
                logger.error("❌ Step 1 failed - Could not find or click Get Started button")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_GET_STARTED_BUTTON_FAILED',
                    'message': 'We couldn\'t start your application. Please try again.'
                }
                
        except Exception as e:
            logger.error(f"❌ Step 1 failed with error: {str(e)}")
            page_code = self.get_page_name_code()
            return {
                'status': False,
                'code': f'{page_code}_EXCEPTION',
                'message': 'We encountered an issue starting your application. Please try again.'
            }
