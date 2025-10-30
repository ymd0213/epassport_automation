"""
Step 15: Payment Page Automation
Handles payment information form filling and submission
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step15Payment(BaseStep):
    """Step 15: Payment page automation"""
    
    def __init__(self, driver, payment_data):
        super().__init__(driver, "Step 15: Payment")
        self.payment_data = payment_data
        
        # First name input
        self.first_name = {
            'css_selector': 'input[data-testid="textInput"]#firstName',
            'xpath': '//input[@data-testid="textInput" and @id="firstName"]',
            'data_testid': 'textInput',
            'id': 'firstName'
        }
        
        # Last name input
        self.surname = {
            'css_selector': 'input[data-testid="textInput"]#surname',
            'xpath': '//input[@data-testid="textInput" and @id="surname"]',
            'data_testid': 'textInput',
            'id': 'surname'
        }
        
        # Card type selector
        self.card_type = {
            'css_selector': 'select[data-testid="Select"]#cardType',
            'xpath': '//select[@data-testid="Select" and @id="cardType"]',
            'data_testid': 'Select',
            'id': 'cardType'
        }
        
        # Card number input
        self.account_number = {
            'css_selector': 'input[data-testid="textInput"]#accountNumber',
            'xpath': '//input[@data-testid="textInput" and @id="accountNumber"]',
            'data_testid': 'textInput',
            'id': 'accountNumber'
        }
        
        # Security code input
        self.security_code = {
            'css_selector': 'input[data-testid="textInput"]#securityCode',
            'xpath': '//input[@data-testid="textInput" and @id="securityCode"]',
            'data_testid': 'textInput',
            'id': 'securityCode'
        }
        
        # Expiration month selector
        self.expiration_month = {
            'css_selector': 'select[data-testid="Select"]#expirationDateMonth',
            'xpath': '//select[@data-testid="Select" and @id="expirationDateMonth"]',
            'data_testid': 'Select',
            'id': 'expirationDateMonth'
        }
        
        # Expiration year input
        self.expiration_year = {
            'css_selector': 'input[data-testid="textInput"]#expirationDateYear',
            'xpath': '//input[@data-testid="textInput" and @id="expirationDateYear"]',
            'data_testid': 'textInput',
            'id': 'expirationDateYear'
        }
        
        # Submit button
        self.submit_button = {
            'css_selector': 'button[type="submit"][data-testid="button"].usa-button.padding-y-2',
            'xpath': '//button[@type="submit" and @data-testid="button" and contains(@class, "usa-button") and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
    
    def input_card_number(self, text, description="card number"):
        """
        Input credit card number - handles auto-formatting by the field
        
        Args:
            text (str): Card number to input
            description (str): Description for logging
            
        Returns:
            bool: True if input was successful, False otherwise
        """
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            
            logger.info(f"Looking for {description}...")
            
            # Try different selector strategies
            selectors = []
            
            if self.account_number.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, self.account_number.get('css_selector')))
            
            if self.account_number.get('xpath'):
                selectors.append((By.XPATH, self.account_number.get('xpath')))
            
            if self.account_number.get('id'):
                selectors.append((By.ID, self.account_number.get('id')))
            
            input_field = None
            for by, selector in selectors:
                if selector:
                    try:
                        input_field = self.wait.until(EC.presence_of_element_located((by, selector)))
                        logger.info(f"Found {description} using {by}: {selector}")
                        break
                    except:
                        continue
            
            if input_field:
                # Clear existing text and input new text
                input_field.clear()
                time.sleep(0.5)
                input_field.send_keys(text)
                time.sleep(0.5)
                
                # Verify the input - strip spaces for comparison since field auto-formats
                try:
                    actual_value = input_field.get_attribute("value")
                    # Remove spaces from both values for comparison
                    actual_value_stripped = actual_value.replace(' ', '').replace('-', '')
                    text_stripped = text.replace(' ', '').replace('-', '')
                    
                    if actual_value_stripped == text_stripped:
                        logger.info(f"✅ Successfully input card number (formatted as '{actual_value}')")
                        return True
                    else:
                        logger.warning(f"Card number verification failed: expected '{text}', got '{actual_value}'")
                        # Try one more time
                        input_field.clear()
                        time.sleep(0.5)
                        input_field.click()
                        time.sleep(0.5)
                        input_field.send_keys(text)
                        time.sleep(0.5)
                        actual_value = input_field.get_attribute("value")
                        actual_value_stripped = actual_value.replace(' ', '').replace('-', '')
                        
                        if actual_value_stripped == text_stripped:
                            logger.info(f"✅ Successfully input card number on retry (formatted as '{actual_value}')")
                            return True
                        else:
                            logger.error(f"❌ Failed to input card number after retry")
                            return False
                except Exception as e:
                    logger.warning(f"Could not verify card number input: {str(e)}")
                    logger.info(f"✅ Card number sent (verification skipped)")
                    return True
            else:
                logger.error(f"❌ Could not find {description} field")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error inputting card number: {str(e)}")
            return False
    
    def select_card_type_by_index(self, index):
        """
        Select card type by index position (not by value attribute)
        
        Args:
            index (int): Index of the option to select (0-based)
            
        Returns:
            bool: True if selection was successful, False otherwise
        """
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.support.ui import Select
            
            logger.info(f"Looking for card type select field...")
            
            # Try different selector strategies
            selectors = []
            
            if self.card_type.get('css_selector'):
                selectors.append((By.CSS_SELECTOR, self.card_type.get('css_selector')))
            
            if self.card_type.get('xpath'):
                selectors.append((By.XPATH, self.card_type.get('xpath')))
            
            if self.card_type.get('id'):
                selectors.append((By.ID, self.card_type.get('id')))
            
            select_field = None
            for by, selector in selectors:
                if selector:
                    try:
                        select_field = self.wait.until(EC.presence_of_element_located((by, selector)))
                        logger.info(f"Found card type select using {by}: {selector}")
                        break
                    except:
                        continue
            
            if select_field:
                select = Select(select_field)
                select.select_by_index(index)
                logger.info(f"✅ Successfully selected card type at index {index}")
                return True
            else:
                logger.error(f"❌ Could not find card type select field")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error selecting card type by index: {str(e)}")
            return False
    
    def execute(self):
        """
        Execute Step 15: Handle payment information form
        
        Returns:
            dict: Result containing status, code, and message
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Mock payment data (since payment info is not in API data)
            mock_payment_data = {
                "payment_option": "3",
                "cardholder_name": "Hunter Johnson",
                "cc_number": "376743655814011",
                "cc_exp_month": "8",
                "cc_exp_year": "30",
                "cc_cvv": "1345"
            }
            
            # Use mock data for payment (API doesn't provide payment info)
            # If payment data exists in self.payment_data, it will override mock data
            payment_info = {**mock_payment_data, **{k: v for k, v in self.payment_data.items() if k in mock_payment_data}}
            
            # Split cardholder name into first and last name
            cardholder_name = payment_info.get('cardholder_name', '')
            name_parts = cardholder_name.split(' ', 1)  # Split on first space only
            first_name = name_parts[0] if name_parts else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            logger.info(f"Cardholder name: {cardholder_name}")
            logger.info(f"First name: {first_name}, Last name: {last_name}")
            
            # Fill in first name
            logger.info("Filling in account holder first name...")
            if not self.find_and_input_text(self.first_name, first_name, "first name"):
                logger.error("Failed to input first name")
                return {
                    'status': False,
                    'code': 'FIRST_NAME_INPUT_FAILED',
                    'message': 'Failed to input first name'
                }
            time.sleep(2)  # 2 second delay after input
            
            # Fill in last name
            logger.info("Filling in account holder last name...")
            if not self.find_and_input_text(self.surname, last_name, "last name"):
                logger.error("Failed to input last name")
                return {
                    'status': False,
                    'code': 'LAST_NAME_INPUT_FAILED',
                    'message': 'Failed to input last name'
                }
            time.sleep(2)  # 2 second delay after input
            
            # Select card type using payment_option as index (not value)
            payment_option = payment_info.get('payment_option', '0')
            payment_option_index = int(payment_option)  # Convert to integer index
            logger.info(f"Selecting card type with index: {payment_option_index}")
            
            # Select by index (not by value) since payment_option represents position in dropdown
            if not self.select_card_type_by_index(payment_option_index):
                logger.error("Failed to select card type")
                return {
                    'status': False,
                    'code': 'CARD_TYPE_SELECT_FAILED',
                    'message': 'Failed to select card type'
                }
            time.sleep(2)  # 2 second delay after select
            
            # Fill in card number (use custom method to handle auto-formatting)
            cc_number = str(payment_info.get('cc_number', ''))
            logger.info("Filling in card number...")
            if not self.input_card_number(cc_number, "card number"):
                logger.error("Failed to input card number")
                return {
                    'status': False,
                    'code': 'CARD_NUMBER_INPUT_FAILED',
                    'message': 'Failed to input card number'
                }
            time.sleep(2)  # 2 second delay after input
            
            # Fill in security code
            cc_cvv = str(payment_info.get('cc_cvv', ''))
            logger.info("Filling in security code...")
            if not self.find_and_input_text(self.security_code, cc_cvv, "security code"):
                logger.error("Failed to input security code")
                return {
                    'status': False,
                    'code': 'SECURITY_CODE_INPUT_FAILED',
                    'message': 'Failed to input security code'
                }
            time.sleep(2)  # 2 second delay after input
            
            # Select expiration month - convert from real month number to 0-based index
            cc_exp_month = payment_info.get('cc_exp_month', '')
            if cc_exp_month:
                month_index = str(int(cc_exp_month) - 1)  # Convert to 0-based index
                logger.info(f"Selecting expiration month: {cc_exp_month} (index: {month_index})")
                if not self.find_and_select_option(self.expiration_month, month_index, "expiration month"):
                    logger.error("Failed to select expiration month")
                    return {
                        'status': False,
                        'code': 'EXP_MONTH_SELECT_FAILED',
                        'message': 'Failed to select expiration month'
                    }
            time.sleep(2)  # 2 second delay after select
            
            # Fill in expiration year
            cc_exp_year = str(payment_info.get('cc_exp_year', ''))
            logger.info("Filling in expiration year...")
            if not self.find_and_input_text(self.expiration_year, cc_exp_year, "expiration year"):
                logger.error("Failed to input expiration year")
                return {
                    'status': False,
                    'code': 'EXP_YEAR_INPUT_FAILED',
                    'message': 'Failed to input expiration year'
                }
            time.sleep(2)  # 2 second delay after input
            
            # Click Submit Order button
            logger.info("Clicking Submit Order button...")
            if not self.find_and_click_button(self.submit_button, "Submit Order button"):
                logger.error("Failed to click Submit Order button")
                return {
                    'status': False,
                    'code': 'SUBMIT_BUTTON_CLICK_FAILED',
                    'message': 'Failed to click Submit Order button'
                }
            
            # Wait 5 seconds after clicking button
            logger.info("Waiting 5 seconds after clicking Submit Order...")
            time.sleep(5)
            
            # Check for errors after clicking submit
            logger.info("Checking for errors after clicking Submit Order...")
            error_result = self.check_for_page_errors("STEP15")
            if error_result:
                return error_result
            
            logger.info("✅ Step 15 completed successfully - Payment form submitted")
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 15 completed successfully - Payment form submitted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 15 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP15_EXCEPTION',
                'message': f'Step 15 failed with error: {str(e)}'
            }

