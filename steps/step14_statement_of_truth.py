"""
Step 14: Statement of Truth Page Automation
Handles statement of truth page by clicking checkbox wrapper and Continue button
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step14StatementOfTruth(BaseStep):
    """Step 14: Statement of truth page automation"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 14: Statement of Truth")
        self.passport_data = passport_data
        
        # Checkbox wrapper (click the wrapper, not the checkbox itself)
        self.checkbox_wrapper = {
            'css_selector': 'div[data-testid="checkbox"].usa-checkbox.margin-top-1',
            'xpath': '//div[@data-testid="checkbox" and contains(@class, "usa-checkbox") and contains(@class, "margin-top-1")]',
            'data_testid': 'checkbox'
        }
        
        # Continue button
        self.continue_button = {
            'css_selector': 'button[type="button"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="button" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
    
    def find_and_click_checkbox_wrapper(self):
        """
        Find and click the checkbox wrapper (not the checkbox itself)
        
        Returns:
            bool: True if wrapper was found and clicked, False otherwise
        """
        try:
            logger.info("Looking for checkbox wrapper...")
            
            # Try different selector strategies
            selectors = []
            
            if self.checkbox_wrapper.get('css_selector'):
                selectors.append(('css selector', self.checkbox_wrapper.get('css_selector')))
            
            if self.checkbox_wrapper.get('xpath'):
                selectors.append(('xpath', self.checkbox_wrapper.get('xpath')))
            
            if self.checkbox_wrapper.get('data_testid'):
                selectors.append(('css selector', f'[data-testid="{self.checkbox_wrapper.get("data_testid")}"]'))
            
            # Add fallback selectors
            selectors.extend([
                ('css selector', 'div[data-testid="checkbox"]'),
                ('xpath', '//div[@data-testid="checkbox"]'),
                ('css selector', '.usa-checkbox'),
                ('xpath', '//div[contains(@class, "usa-checkbox")]')
            ])
            
            wrapper = None
            for by, selector in selectors:
                if selector:
                    try:
                        from selenium.webdriver.common.by import By
                        from selenium.webdriver.support import expected_conditions as EC
                        
                        wrapper = self.wait.until(EC.element_to_be_clickable((by, selector)))
                        logger.info(f"Found checkbox wrapper using {by}: {selector}")
                        break
                    except:
                        continue
            
            if wrapper:
                # Scroll to wrapper if needed
                self.driver.execute_script("arguments[0].scrollIntoView(true);", wrapper)
                time.sleep(1)
                
                # Click the wrapper
                wrapper.click()
                logger.info("✅ Successfully clicked checkbox wrapper")
                return True
            else:
                logger.error("❌ Could not find checkbox wrapper")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error clicking checkbox wrapper: {str(e)}")
            return False
    
    def execute(self):
        """
        Execute Step 14: Handle statement of truth page
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Click checkbox wrapper
            logger.info("Clicking checkbox wrapper on statement of truth page...")
            if not self.find_and_click_checkbox_wrapper():
                logger.error("Failed to click checkbox wrapper")
                return {
                    'status': False,
                    'code': 'CHECKBOX_WRAPPER_FAILED',
                    'message': 'Failed to click checkbox wrapper'
                }
            
            time.sleep(2)  # Brief pause after clicking checkbox
            
            # Click Continue button
            logger.info("Clicking Continue button on statement of truth page...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_FAILED',
                    'message': 'Failed to click Continue button'
                }
            
            # Small delay to allow next page to load
            time.sleep(5)
            
            logger.info("✅ Step 14 completed successfully - Statement of truth page submitted")
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 14 completed successfully - Statement of truth page submitted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 14 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP14_EXCEPTION',
                'message': f'Step 14 failed with error: {str(e)}'
            }

