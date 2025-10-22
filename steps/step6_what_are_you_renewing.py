"""
Step 6: What Are You Renewing Page Automation
Handles passport renewal form with book/card selection and personal information
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step6WhatAreYouRenewing(BaseStep):
    """Step 6: What are you renewing page automation"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 6: What Are You Renewing")
        self.passport_data = passport_data
        
        # Radio button wrapper div selectors for renew book
        self.renew_book_yes = {
            'css_selector': 'div[data-testid="radio"]:has(input[id="renewBook-yes-radio"])',
            'xpath': '//div[@data-testid="radio" and .//input[@id="renewBook-yes-radio"]]',
            'data_testid': 'radio'
        }
        
        self.renew_book_no = {
            'css_selector': 'div[data-testid="radio"]:has(input[id="renewBook-no-radio"])',
            'xpath': '//div[@data-testid="radio" and .//input[@id="renewBook-no-radio"]]',
            'data_testid': 'radio'
        }
        
        # Radio button wrapper div selectors for renew card
        self.renew_card_yes = {
            'css_selector': 'div[data-testid="radio"]:has(input[id="renewCard-yes-radio"])',
            'xpath': '//div[@data-testid="radio" and .//input[@id="renewCard-yes-radio"]]',
            'data_testid': 'radio'
        }
        
        self.renew_card_no = {
            'css_selector': 'div[data-testid="radio"]:has(input[id="renewCard-no-radio"])',
            'xpath': '//div[@data-testid="radio" and .//input[@id="renewCard-no-radio"]]',
            'data_testid': 'radio'
        }
        
        # Passport book form fields
        self.passport_book_id = {
            'css_selector': 'input[id="passportBookId"]',
            'xpath': '//input[@id="passportBookId"]',
            'id': 'passportBookId'
        }
        
        self.passport_book_issue_day = {
            'css_selector': 'input[id="passportBookIssueDate-day"]',
            'xpath': '//input[@id="passportBookIssueDate-day"]',
            'id': 'passportBookIssueDate-day'
        }
        
        self.passport_book_issue_month = {
            'css_selector': 'select[id="passportBookIssueDate-month"]',
            'xpath': '//select[@id="passportBookIssueDate-month"]',
            'id': 'passportBookIssueDate-month'
        }
        
        self.passport_book_issue_year = {
            'css_selector': 'input[id="passportBookIssueDate-year"]',
            'xpath': '//input[@id="passportBookIssueDate-year"]',
            'id': 'passportBookIssueDate-year'
        }
        
        # Passport card form fields
        self.passport_card_id = {
            'css_selector': 'input[id="passportCardId"]',
            'xpath': '//input[@id="passportCardId"]',
            'id': 'passportCardId'
        }
        
        self.passport_card_issue_day = {
            'css_selector': 'input[id="passportCardIssueDate-day"]',
            'xpath': '//input[@id="passportCardIssueDate-day"]',
            'id': 'passportCardIssueDate-day'
        }
        
        self.passport_card_issue_month = {
            'css_selector': 'select[id="passportCardIssueDate-month"]',
            'xpath': '//select[@id="passportCardIssueDate-month"]',
            'id': 'passportCardIssueDate-month'
        }
        
        self.passport_card_issue_year = {
            'css_selector': 'input[id="passportCardIssueDate-year"]',
            'xpath': '//input[@id="passportCardIssueDate-year"]',
            'id': 'passportCardIssueDate-year'
        }
        
        # Personal information fields
        self.surname = {
            'css_selector': 'input[id="surname"]',
            'xpath': '//input[@id="surname"]',
            'id': 'surname'
        }
        
        self.date_of_birth_year = {
            'css_selector': 'input[id="dateOfBirth-year"]',
            'xpath': '//input[@id="dateOfBirth-year"]',
            'id': 'dateOfBirth-year'
        }
        
        self.date_of_birth_month = {
            'css_selector': 'select[id="dateOfBirth-month"]',
            'xpath': '//select[@id="dateOfBirth-month"]',
            'id': 'dateOfBirth-month'
        }
        
        self.date_of_birth_day = {
            'css_selector': 'input[id="dateOfBirth-day"]',
            'xpath': '//input[@id="dateOfBirth-day"]',
            'id': 'dateOfBirth-day'
        }
        
        # Continue button
        self.continue_button = {
            'css_selector': 'button[type="submit"][data-testid="button"]',
            'xpath': '//button[@type="submit" and @data-testid="button"]',
            'data_testid': 'button'
        }
        
        # Error detection selectors
        self.error_alert = {
            'css_selector': 'div.usa-alert__body',
            'xpath': '//div[@class="usa-alert__body"]',
            'class_name': 'usa-alert__body'
        }
        
        self.continue_button_after_error = {
            'css_selector': 'button[type="button"][data-testid="button"]',
            'xpath': '//button[@type="button" and @data-testid="button"]',
            'data_testid': 'button'
        }
    
    def execute(self):
        """
        Execute Step 6: Handle what are you renewing form
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Handle recent book number logic
            recent_book_number = self.passport_data.get('recent_book_number', '')
            if recent_book_number and recent_book_number.strip():
                logger.info("Recent book number found, clicking Yes for renew book")
                if not self.find_and_click_checkbox(self.renew_book_yes, "renew book Yes radio"):
                    logger.error("Failed to click renew book Yes radio")
                    return False
                time.sleep(2)  # 1 second delay after input
                
                # Fill passport book form fields
                logger.info("Filling passport book information...")
                
                # Passport book number
                if not self.find_and_input_text(self.passport_book_id, recent_book_number, "passport book ID"):
                    logger.error("Failed to input passport book ID")
                    return False
                time.sleep(2)
                
                # Passport book issue date
                recent_book_issued_day = str(self.passport_data.get('recent_book_issued_day', ''))
                if recent_book_issued_day:
                    if not self.find_and_input_text(self.passport_book_issue_day, recent_book_issued_day, "passport book issue day"):
                        logger.error("Failed to input passport book issue day")
                        return False
                    time.sleep(2)
                
                recent_book_issued_month = str(self.passport_data.get('recent_book_issued_month', ''))
                if recent_book_issued_month:
                    # Convert month number to 0-based index (January = 0, December = 11)
                    month_index = str(int(recent_book_issued_month) - 1)
                    if not self.find_and_select_option(self.passport_book_issue_month, month_index, "passport book issue month"):
                        logger.error("Failed to select passport book issue month")
                        return False
                    time.sleep(2)
                
                recent_book_issued_year = str(self.passport_data.get('recent_book_issued_year', ''))
                if recent_book_issued_year:
                    if not self.find_and_input_text(self.passport_book_issue_year, recent_book_issued_year, "passport book issue year"):
                        logger.error("Failed to input passport book issue year")
                        return False
                    time.sleep(2)
            else:
                logger.info("No recent book number found, clicking No for renew book")
                if not self.find_and_click_checkbox(self.renew_book_no, "renew book No radio"):
                    logger.error("Failed to click renew book No radio")
                    return False
                time.sleep(2)
            
            # Handle recent card number logic
            recent_card_number = self.passport_data.get('recent_card_number', '')
            if recent_card_number and recent_card_number.strip():
                logger.info("Recent card number found, clicking Yes for renew card")
                if not self.find_and_click_checkbox(self.renew_card_yes, "renew card Yes radio"):
                    logger.error("Failed to click renew card Yes radio")
                    return False
                time.sleep(2)
                
                # Fill passport card form fields
                logger.info("Filling passport card information...")
                
                # Passport card number
                if not self.find_and_input_text(self.passport_card_id, recent_card_number, "passport card ID"):
                    logger.error("Failed to input passport card ID")
                    return False
                time.sleep(2)
                
                # Passport card issue date (using same date fields as book for now)
                recent_card_issued_day = str(self.passport_data.get('recent_book_issued_day', ''))
                if recent_card_issued_day:
                    if not self.find_and_input_text(self.passport_card_issue_day, recent_card_issued_day, "passport card issue day"):
                        logger.error("Failed to input passport card issue day")
                        return False
                    time.sleep(2)
                
                recent_card_issued_month = str(self.passport_data.get('recent_book_issued_month', ''))
                if recent_card_issued_month:
                    # Convert month number to 0-based index (January = 0, December = 11)
                    month_index = str(int(recent_card_issued_month) - 1)
                    if not self.find_and_select_option(self.passport_card_issue_month, month_index, "passport card issue month"):
                        logger.error("Failed to select passport card issue month")
                        return False
                    time.sleep(2)
                
                recent_card_issued_year = str(self.passport_data.get('recent_book_issued_year', ''))
                if recent_card_issued_year:
                    if not self.find_and_input_text(self.passport_card_issue_year, recent_card_issued_year, "passport card issue year"):
                        logger.error("Failed to input passport card issue year")
                        return False
                    time.sleep(2)
            else:
                logger.info("No recent card number found, clicking No for renew card")
                if not self.find_and_click_checkbox(self.renew_card_no, "renew card No radio"):
                    logger.error("Failed to click renew card No radio")
                    return False
                time.sleep(2)
            
            # Fill personal information
            logger.info("Filling personal information...")
            
            # Last name
            last_name = self.passport_data.get('last_name', '')
            if last_name:
                if not self.find_and_input_text(self.surname, last_name, "surname"):
                    logger.error("Failed to input surname")
                    return False
                time.sleep(2)
            
            # Date of birth
            year_of_birth = str(self.passport_data.get('year_of_birth', ''))
            if year_of_birth:
                if not self.find_and_input_text(self.date_of_birth_year, year_of_birth, "date of birth year"):
                    logger.error("Failed to input date of birth year")
                    return False
                time.sleep(2)
            
            month_of_birth = str(self.passport_data.get('month_of_birth', ''))
            if month_of_birth:
                # Convert month number to 0-based index (January = 0, December = 11)
                month_index = str(int(month_of_birth) - 1)
                if not self.find_and_select_option(self.date_of_birth_month, month_index, "date of birth month"):
                    logger.error("Failed to select date of birth month")
                    return False
                time.sleep(2)
            
            day_of_birth = str(self.passport_data.get('day_of_birth', ''))
            if day_of_birth:
                if not self.find_and_input_text(self.date_of_birth_day, day_of_birth, "date of birth day"):
                    logger.error("Failed to input date of birth day")
                    return False
                time.sleep(2)
            
            # Validate Continue button before clicking
            logger.info("Validating Continue button...")
            continue_button_element = self.find_element(self.continue_button, "Continue button")
            
            if not continue_button_element:
                logger.error("Continue button not found")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_NOT_FOUND',
                    'message': 'Continue button not found on the page'
                }
            
            # Check if continue button is disabled
            if not continue_button_element.is_enabled():
                logger.error("Continue button is disabled")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_DISABLED',
                    'message': 'Continue button is disabled - form validation failed'
                }
            
            # Click Continue button
            logger.info("Clicking Continue button...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                return False
            
            # Wait 5 seconds after clicking continue
            logger.info("Waiting 5 seconds after clicking Continue...")
            time.sleep(5)
            
            # Wait 20 seconds and check for Continue button first
            logger.info("Waiting 20 seconds to check for Continue button...")
            time.sleep(20)
            
            # Look for Continue button 3 times first
            for attempt in range(3):
                logger.info(f"Looking for Continue button (attempt {attempt + 1}/3)...")
                
                try:
                    continue_btn = self.driver.find_element("css selector", 'button[type="button"][data-testid="button"]')
                    if continue_btn:
                        logger.info("Found Continue button, clicking it...")
                        continue_btn.click()
                        logger.info("✅ Step 6 completed successfully - Continue button clicked")
                        return {
                            'status': True,
                            'code': 'SUCCESS',
                            'message': 'Step 6 completed successfully - Continue button clicked'
                        }
                except:
                    logger.info(f"Continue button not found on attempt {attempt + 1}")
                
                if attempt < 2:  # Don't sleep after the last attempt
                    time.sleep(2)
            
            # If Continue button not found, look for error message
            logger.info("Continue button not found, checking for error messages...")
            
            try:
                # Look for the specific error message
                error_heading = self.driver.find_element("css selector", "h1.usa-alert__heading")
                if error_heading and "Your passport book is eligible for online renewal" in error_heading.text:
                    error_message = error_heading.text
                    logger.error(f"❌ Error found: {error_message}")
                    return {
                        'status': False,
                        'code': 'PASSPORT_ELIGIBILITY_ERROR',
                        'message': error_message
                    }
            except:
                logger.info("No specific error message found")
            
            # Check for other common error patterns
            try:
                # Look for general error alert
                error_alert = self.driver.find_element("css selector", "div.usa-alert__body")
                if error_alert:
                    error_message = error_alert.text.strip()
                    logger.error(f"❌ General error found: {error_message}")
                    return {
                        'status': False,
                        'code': 'GENERAL_ERROR',
                        'message': error_message
                    }
            except:
                logger.info("No general error message found")
            
            # If we get here, no Continue button was found and no specific error message
            logger.error("❌ Your passport data is not correct - Continue button not found")
            return {
                'status': False,
                'code': 'CONTINUE_BUTTON_NOT_FOUND',
                'message': 'Continue button not found after form submission'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 6 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP6_EXCEPTION',
                'message': f'Step 6 failed with error: {str(e)}'
            }
