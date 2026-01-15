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

    def parse_card_exp(self, card_exp):
        """
        Parse card expiration date from various formats (MM/YY, MMYY, etc.)
        
        Args:
            card_exp (str): Card expiration in format like "12/25", "1225", etc.
            
        Returns:
            tuple: (month, year) or (None, None) if parsing fails
        """
        if not card_exp:
            return None, None
        
        card_exp = str(card_exp).strip()
        
        # Handle MM/YY format
        if '/' in card_exp:
            parts = card_exp.split('/')
            if len(parts) == 2:
                month = parts[0].strip()
                year = parts[1].strip()
                return month, year
        
        # Handle MMYY format (4 digits)
        if len(card_exp) == 4 and card_exp.isdigit():
            month = card_exp[:2]
            year = card_exp[2:]
            return month, year
        
        return None, None
    
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
            
            # Get billing info from payment data
            billing_info = self.payment_data.get('billing_info', {})
            card_holder = self.payment_data.get('card_holder')
            card_num = self.payment_data.get('card_num')
            card_exp = self.payment_data.get('card_exp')
            card_cvv = self.payment_data.get('card_cvv')
            card_zip = self.payment_data.get('card_zip')
            
            # If billing_info is a string (JSON), parse it
            if isinstance(billing_info, str):
                import json
                try:
                    billing_info = json.loads(billing_info)
                except:
                    logger.error("Failed to parse billing_info JSON string")
                    billing_info = {}
            
            # Validate that we have the required billing information
            if not billing_info:
                logger.error("No billing_info found in payment data")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_BILLING_INFO_MISSING',
                    'message': 'Payment information is missing. Please provide your billing details.'
                }
            
            # Use billing_info from API
            payment_info = billing_info
            
            # Validate required fields
            required_fields = ['cardholder_name', 'cc_number', 'cc_exp_month', 'cc_exp_year', 'cc_cvv', 'payment_option']
            missing_fields = [field for field in required_fields if not payment_info.get(field)]
            
            if missing_fields:
                individual_card_missing = []
                field_to_card_var = {
                    'cardholder_name': card_holder,
                    'cc_number': card_num,
                    # 'cc_exp_month': card_exp,  # Note: card_exp might need parsing
                    # 'cc_exp_year': card_exp,   # Note: card_exp might need parsing
                    'cc_cvv': card_cvv,
                    # 'payment_option': None  # No direct mapping for 
                }

                for field in missing_fields:
                    if field == 'cardholder_name' and not card_holder:
                        individual_card_missing.append('card_holder')
                    elif field == 'cc_number' and not card_num:
                        individual_card_missing.append('card_num')                    
                    elif field == 'cc_cvv' and not card_cvv:
                        individual_card_missing.append('card_cvv')

                if individual_card_missing:        
                    print(f"Missing required billing fields: {', '.join(individual_card_missing)}")
                    page_code = self.get_page_name_code()
                    return {
                        'status': False,
                        'code': f'{page_code}_BILLING_INFO_INCOMPLETE',
                        'message': 'Please provide all required payment information.'
                    }
            
            # Split cardholder name into first and last name
            cardholder_name = payment_info.get('cardholder_name', '') or card_holder or ''
            name_parts = cardholder_name.split(' ', 1)  # Split on first space only
            first_name = name_parts[0] if name_parts else ''
            last_name = name_parts[1] if len(name_parts) > 1 else ''
            
            logger.info(f"Cardholder name: {cardholder_name}")
            logger.info(f"First name: {first_name}, Last name: {last_name}")
            
            # Fill in first name
            logger.info("Filling in account holder first name...")
            if not self.find_and_input_text(self.first_name, first_name, "first name"):
                logger.error("Failed to input first name")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_FIRST_NAME_INPUT_FAILED',
                    'message': 'We couldn\'t process your payment information. Please try again.'
                }
            
            # Fill in last name
            logger.info("Filling in account holder last name...")
            if not self.find_and_input_text(self.surname, last_name, "last name"):
                logger.error("Failed to input last name")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_LAST_NAME_INPUT_FAILED',
                    'message': 'We couldn\'t process your payment information. Please try again.'
                }
            
            # Select card type using payment_option as index (not value)
            # Note: First option (index 0) is "Select" placeholder, so we add 1 to skip it
            payment_option = payment_info.get('payment_option', '0')
            payment_option_index = int(payment_option) + 1  # Add 1 to skip "Select" option
            logger.info(f"Selecting card type with index: {payment_option_index} (payment_option: {payment_option})")
            
            # Select by index (not by value) since payment_option represents position in dropdown
            if not self.select_card_type_by_index(payment_option_index):
                logger.error("Failed to select card type")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_CARD_TYPE_SELECT_FAILED',
                    'message': 'We couldn\'t process your payment information. Please try again.'
                }
            time.sleep(0.5)  # 2 second delay after select
            
            # Fill in card number (use custom method to handle auto-formatting)
            cc_number = str(payment_info.get('cc_number', '') or card_num or '')
            logger.info("Filling in card number...")
            if not self.input_card_number(cc_number, "card number"):
                logger.error("Failed to input card number")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_CARD_NUMBER_INPUT_FAILED',
                    'message': 'We couldn\'t process your payment information. Please try again.'
                }
            
            # Fill in security code
            cc_cvv = str(payment_info.get('cc_cvv', '') or card_cvv or '')
            logger.info("Filling in security code...")
            if not self.find_and_input_text(self.security_code, cc_cvv, "security code"):
                logger.error("Failed to input security code")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_SECURITY_CODE_INPUT_FAILED',
                    'message': 'We couldn\'t process your payment information. Please try again.'
                }
            
            # Select expiration month (data is 1-12, but option values are 0-11)
            cc_exp_month = payment_info.get('cc_exp_month', '')
            if not cc_exp_month and card_exp:
                parsed_month, _ = self.parse_card_exp(card_exp)
                if parsed_month:
                    cc_exp_month = parsed_month

            if cc_exp_month:
                month_value = str(int(cc_exp_month) - 1)  # Convert 1-12 to 0-11
                logger.info(f"Selecting expiration month: {cc_exp_month} (option value: {month_value})")
                if not self.find_and_select_option(self.expiration_month, month_value, "expiration month"):
                    logger.error("Failed to select expiration month")
                    page_code = self.get_page_name_code()
                    return {
                        'status': False,
                        'code': f'{page_code}_EXP_MONTH_SELECT_FAILED',
                        'message': 'We couldn\'t process your payment information. Please try again.'
                    }
            
            # Fill in expiration year
            cc_exp_year = str(payment_info.get('cc_exp_year', ''))
            logger.info("Filling in expiration year...")
            if not cc_exp_year and card_exp:
                _, parsed_year = self.parse_card_exp(card_exp)
                if parsed_year:
                    cc_exp_year = parsed_year

            if not self.find_and_input_text(self.expiration_year, cc_exp_year, "expiration year"):
                logger.error("Failed to input expiration year")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_EXP_YEAR_INPUT_FAILED',
                    'message': 'We couldn\'t process your payment information. Please try again.'
                }
            
            # Click Submit Order button
            logger.info("Clicking Submit Order button...")
            if not self.find_and_click_button(self.submit_button, "Submit Order button"):
                logger.error("Failed to click Submit Order button")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_SUBMIT_BUTTON_CLICK_FAILED',
                    'message': 'We couldn\'t submit your payment. Please try again.'
                }
            
            # Wait 2 seconds after clicking button
            logger.info("waiting 2 seconds after clicking Submit Order...")
            time.sleep(2)
            
            # Check for errors after clicking submit
            logger.info("Checking for errors after clicking Submit Order...")
            error_result = self.check_for_page_errors()
            if error_result:
                return error_result
            
            logger.info("✅ Step 15 completed successfully - Payment form submitted")
            
            # Wait for confirmation page to load
            time.sleep(20)
            
            # Scrape the application number from the confirmation page
            renewal_application_id = None
            try:
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.support import expected_conditions as EC
                
                logger.info("Scraping renewal application number...")
                
                # Find the span with class "pii-mask" containing the application number
                wait = WebDriverWait(self.driver, 30)
                app_number_element = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "span.pii-mask"))
                )
                renewal_application_id = app_number_element.text.strip()
                logger.info(f"✅ Renewal Application Number: {renewal_application_id}")
                    
            except Exception as e:
                logger.error(f"❌ Could not scrape renewal application number: {str(e)}")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_RENEWAL_APP_NUMBER',
                    'message': 'Could not scrape renewal application number.'
                }
            
            if not renewal_application_id:
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_RENEWAL_APP_NUMBER_MISSING',
                    'message': 'Renewal application number is missing.'
                }
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 15 completed successfully - Payment form submitted',
                'renewal_application_id': renewal_application_id
            }
            
        except Exception as e:
            logger.error(f"❌ Step 15 failed with error: {str(e)}")
            page_code = self.get_page_name_code()
            return {
                'status': False,
                'code': f'{page_code}_EXCEPTION',
                'message': 'We encountered an issue processing your payment. Please try again.'
            }

