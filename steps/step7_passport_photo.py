"""
Step 7: Passport Photo Upload Page Automation
Handles passport photo upload and form submission
"""

import time
import logging
import os
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step7PassportPhoto(BaseStep):
    """Step 7: Passport photo upload page automation"""
    
    def __init__(self, driver):
        super().__init__(driver, "Step 7: Passport Photo Upload")
        
        # Initial Continue button selector - more specific to avoid other buttons
        self.initial_continue_button = {
            'css_selector': 'button[type="button"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="button" and @data-testid="button" and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
        
        # File upload input selector
        self.file_upload_input = {
            'css_selector': 'input[id="photo-upload"]',
            'xpath': '//input[@id="photo-upload"]',
            'id': 'photo-upload'
        }
        
        # Continue button after upload selector
        self.continue_after_upload = {
            'css_selector': 'button[type="submit"][data-testid="button"]',
            'xpath': '//button[@type="submit" and @data-testid="button"]',
            'data_testid': 'button'
        }
        
        # Final Continue button selector (enabled) - more specific
        self.final_continue_button = {
            'css_selector': 'button[type="submit"][data-testid="button"].usa-button.padding-y-2:not([disabled])',
            'xpath': '//button[@type="submit" and @data-testid="button" and contains(@class, "padding-y-2") and not(@disabled)]',
            'data_testid': 'button'
        }
    
    def find_and_upload_file(self, file_path, description="file upload"):
        """
        Find and upload a file
        
        Args:
            file_path (str): Path to the file to upload
            description (str): Description of the upload field for logging
            
        Returns:
            bool: True if upload was successful, False otherwise
        """
        try:
            logger.info(f"Looking for {description}...")
            
            # Try different selector strategies
            selectors = []
            
            if self.file_upload_input.get('css_selector'):
                selectors.append(('css selector', self.file_upload_input.get('css_selector')))
            
            if self.file_upload_input.get('xpath'):
                selectors.append(('xpath', self.file_upload_input.get('xpath')))
            
            if self.file_upload_input.get('id'):
                selectors.append(('id', self.file_upload_input.get('id')))
            
            file_input = None
            for by, selector in selectors:
                if selector:
                    try:
                        file_input = self.wait.until(lambda driver: driver.find_element(by, selector))
                        logger.info(f"Found {description} using {by}: {selector}")
                        break
                    except:
                        continue
            
            if file_input:
                # Check if file exists
                if not os.path.exists(file_path):
                    logger.error(f"❌ File not found: {file_path}")
                    return False
                
                # Get absolute path
                absolute_path = os.path.abspath(file_path)
                logger.info(f"Uploading file: {absolute_path}")
                
                # Send file path to input
                file_input.send_keys(absolute_path)
                logger.info(f"✅ Successfully uploaded file to {description}")
                return True
            else:
                logger.error(f"❌ Could not find {description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error uploading file to {description}: {str(e)}")
            return False
    
    def execute(self):
        """
        Execute Step 7: Handle passport photo upload
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Click initial Continue button
            logger.info("Clicking initial Continue button...")
            if not self.find_and_click_button(self.initial_continue_button, "initial Continue button"):
                logger.error("Failed to click initial Continue button")
                return {
                    'status': False,
                    'code': 'STEP7_INITIAL_BUTTON_FAILED',
                    'message': 'Failed to click initial Continue button'
                }
            
            # Wait 5 seconds and check for errors
            time.sleep(5)
            error_result = self.check_for_page_errors("STEP7")
            if error_result:
                return error_result
            
            # Upload passport photo
            logger.info("Uploading passport photo...")
            photo_path = "accept-man.jpg"
            if not self.find_and_upload_file(photo_path, "passport photo upload"):
                logger.error("Failed to upload passport photo")
                return {
                    'status': False,
                    'code': 'STEP7_UPLOAD_FAILED',
                    'message': 'Failed to upload passport photo'
                }
            
            # Wait for upload to process
            time.sleep(3)
            
            # Click Continue button after upload
            logger.info("Clicking Continue button after upload...")
            if not self.find_and_click_button(self.continue_after_upload, "Continue button after upload"):
                logger.error("Failed to click Continue button after upload")
                return {
                    'status': False,
                    'code': 'STEP7_UPLOAD_BUTTON_FAILED',
                    'message': 'Failed to click Continue button after upload'
                }
            
            # Wait 5 seconds and check for errors
            time.sleep(5)
            error_result = self.check_for_page_errors("STEP7")
            if error_result:
                return error_result
            
            # Look for final Continue button 3 times
            for attempt in range(3):
                logger.info(f"Looking for final Continue button (attempt {attempt + 1}/3)...")
                
                try:
                    # Look for enabled Continue button with specific class
                    continue_btn = self.driver.find_element("css selector", 'button[type="submit"][data-testid="button"].usa-button.padding-y-2:not([disabled])')
                    if continue_btn:
                        logger.info("Found final Continue button, clicking it...")
                        continue_btn.click()
                        
                        # Wait 5 seconds and check for errors
                        time.sleep(5)
                        error_result = self.check_for_page_errors("STEP7")
                        if error_result:
                            return error_result
                        
                        logger.info("✅ Step 7 completed successfully - Final Continue button clicked")
                        return {
                            'status': True,
                            'code': 'SUCCESS',
                            'message': 'Step 7 completed successfully - Final Continue button clicked'
                        }
                except Exception as e:
                    logger.debug(f"Final Continue button not found on attempt {attempt + 1}: {e}")
                
                if attempt < 2:  # Don't sleep after the last attempt
                    time.sleep(2)
            
            # If we get here, no final Continue button was found - check for photo error
            logger.info("Final Continue button not found, checking for photo error...")
            
            try:
                # Look for the photo error message
                photo_error_heading = self.driver.find_element("css selector", "h2.usa-alert__heading")
                if photo_error_heading and "Sorry, we can't accept your photo" in photo_error_heading.text:
                    error_message = photo_error_heading.text
                    logger.error(f"❌ Photo error found: {error_message}")
                    return {
                        'status': False,
                        'code': 'PHOTO_ERROR',
                        'message': error_message
                    }
            except:
                logger.info("No photo error message found")
            
            # If we get here, no final Continue button was found and no photo error
            logger.error("❌ Your passport photo is not correct - Final Continue button not found")
            return {
                'status': False,
                'code': 'CONTINUE_BUTTON_NOT_FOUND',
                'message': 'Final Continue button not found after photo upload'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 7 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP7_EXCEPTION',
                'message': f'Step 7 failed with error: {str(e)}'
            }
