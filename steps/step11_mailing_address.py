"""
Step 11: Mailing Address Confirmation/Editing Automation
- If permanent_address_same is 1 or "1": click Continue, wait 5s
- Otherwise: click Edit Mailing Address, fill mailing fields, click Add Address, wait 10s, click Continue, then click Continue again
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step11MailingAddress(BaseStep):
    """Step 11: Mailing address handling"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 11: Mailing Address")
        self.passport_data = passport_data
        
        # Buttons
        self.continue_button = {
            'css_selector': 'button[type="submit"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="submit" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
        
        self.edit_mailing_button = {
            'css_selector': 'button[type="button"][data-testid="button"].usa-button.usa-button--outline.width-full.padding-y-2',
            'xpath': '//button[@type="button" and @data-testid="button" and contains(@class, "usa-button--outline") and contains(@class, "width-full") and contains(@class, "padding-y-2") and contains(text(), "Edit Mailing Address")]'
        }
        
        self.add_address_button = {
            'css_selector': 'button[type="submit"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="submit" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2") and contains(text(), "Add Address")]'
        }
        
        # Inputs
        self.mailing_address_1 = {
            'css_selector': 'input#mailingAddress\\.address1',
            'xpath': '//input[@id="mailingAddress.address1"]',
            'id': 'mailingAddress.address1'
        }
        
        self.mailing_city = {
            'css_selector': 'input#mailingAddress\\.city',
            'xpath': '//input[@id="mailingAddress.city"]',
            'id': 'mailingAddress.city'
        }
        
        self.mailing_zip = {
            'css_selector': 'input#mailingAddress\\.zipCode',
            'xpath': '//input[@id="mailingAddress.zipCode"]',
            'id': 'mailingAddress.zipCode'
        }
        
        self.mailing_state = {
            'css_selector': 'select#mailingAddress\\.state',
            'xpath': '//select[@id="mailingAddress.state"]',
            'id': 'mailingAddress.state'
        }
    
    def execute(self):
        try:
            self.log_step_info()
            self.wait_for_page_load()
            
            permanent_address_same = self.passport_data.get('permanent_address_same', '')
            
            if permanent_address_same == 1 or permanent_address_same == "1":
                logger.info("permanent_address_same is 1 -> clicking Continue and waiting 5s")
                if not self.find_and_click_button(self.continue_button, "Continue button"):
                    logger.error("Failed to click Continue button")
                    return False
                time.sleep(5)
            else:
                logger.info("permanent_address_same is not 1 -> editing mailing address")
                # Click Edit Mailing Address
                if not self.find_and_click_button(self.edit_mailing_button, "Edit Mailing Address button"):
                    logger.error("Failed to click Edit Mailing Address button")
                    return False
                time.sleep(1)
                
                # Fill mailing address fields
                addr1 = self.passport_data.get('mailing_address_1', '')
                if addr1:
                    if not self.find_and_input_text(self.mailing_address_1, addr1, "mailing address 1"):
                        logger.error("Failed to input mailing address 1")
                        return False
                    time.sleep(2)
                
                city = self.passport_data.get('mailing_city', '')
                if city:
                    if not self.find_and_input_text(self.mailing_city, city, "mailing city"):
                        logger.error("Failed to input mailing city")
                        return False
                    time.sleep(2)
                
                state = self.passport_data.get('mailing_state', '')
                if state:
                    if not self.find_and_select_option(self.mailing_state, state, "mailing state"):
                        logger.error("Failed to select mailing state")
                        return False
                    time.sleep(2)
                
                zip_code = self.passport_data.get('mailing_zip', '')
                if zip_code:
                    if not self.find_and_input_text(self.mailing_zip, zip_code, "mailing zip"):
                        logger.error("Failed to input mailing zip")
                        return False
                    time.sleep(2)
                
                # Click Add Address
                if not self.find_and_click_button(self.add_address_button, "Add Address button"):
                    logger.error("Failed to click Add Address button")
                    return False
                time.sleep(10)
                
                # Click Continue
                if not self.find_and_click_button(self.continue_button, "Continue button"):
                    logger.error("Failed to click Continue button after Add Address")
                    return False
                time.sleep(5)
                
                # Click Continue again (as specified)
                if not self.find_and_click_button(self.continue_button, "Continue button (final)"):
                    logger.error("Failed to click final Continue button")
                    return False
            
            logger.info("✅ Step 11 completed successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Step 11 failed with error: {str(e)}")
            return False
