"""
Step 3: Eligibility Requirements Page Automation
Finds and clicks the "Continue" button on the "Eligibility Requirements" page
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step3EligibilityRequirements(BaseStep):
    """Step 3: Eligibility Requirements page automation"""
    
    def __init__(self, driver):
        super().__init__(driver, "Step 3: Eligibility Requirements")
        
        # Button selector for "Continue" button
        self.continue_button = {
            'css_selector': 'button[data-testid="button"][type="button"]:not([aria-expanded])',
            'xpath': '//button[@data-testid="button" and @type="button" and not(@aria-expanded)]',
            'data_testid': 'button'
        }
    
    def execute(self):
        """
        Execute Step 3: Click the "Continue" button on Eligibility Requirements page
        
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
                logger.info("✅ Step 3 completed successfully - Continue button clicked")
                
                # Wait 2 seconds as requested
                logger.info("waiting 2 seconds...")
                time.sleep(2)
                
                return {
                    'status': True,
                    'code': 'SUCCESS',
                    'message': 'Step 3 completed successfully - Continue button clicked'
                }
            else:
                logger.error("❌ Step 3 failed - Could not find or click Continue button")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_FAILED',
                    'message': 'Could not find or click Continue button'
                }
                
        except Exception as e:
            logger.error(f"❌ Step 3 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP3_EXCEPTION',
                'message': f'Step 3 failed with error: {str(e)}'
            }
