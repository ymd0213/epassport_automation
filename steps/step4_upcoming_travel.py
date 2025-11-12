"""
Step 4: Upcoming Travel Page Automation
Handles travel plans selection and form filling based on travel_plans value
"""

import time
import logging
import re
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step4UpcomingTravel(BaseStep):
    """Step 4: Upcoming Travel page automation"""
    
    def __init__(self, driver, travel_data):
        super().__init__(driver, "Step 4: Upcoming Travel")
        self.travel_data = travel_data
        
        # Radio button selectors - targeting wrapper div instead of input
        self.yes_radio = {
            'css_selector': 'div[data-testid="radio"]:has(input[id="areYouTravelingSoon-yes-radio"])',
            'xpath': '//div[@data-testid="radio" and .//input[@id="areYouTravelingSoon-yes-radio"]]',
            'data_testid': 'radio'
        }
        
        self.no_radio = {
            'css_selector': 'div[data-testid="radio"]:has(input[id="areYouTravelingSoon-no-radio"])',
            'xpath': '//div[@data-testid="radio" and .//input[@id="areYouTravelingSoon-no-radio"]]',
            'data_testid': 'radio'
        }
        
        # Departure date selectors
        self.departure_day = {
            'css_selector': 'input[data-testid="memorable-date-estimatedDepartureDate-day"]',
            'xpath': '//input[@data-testid="memorable-date-estimatedDepartureDate-day"]',
            'data_testid': 'memorable-date-estimatedDepartureDate-day',
            'id': 'estimatedDepartureDate-day'
        }
        
        self.departure_month = {
            'css_selector': 'select[data-testid="memorable-date-estimatedDepartureDate-month"]',
            'xpath': '//select[@data-testid="memorable-date-estimatedDepartureDate-month"]',
            'data_testid': 'memorable-date-estimatedDepartureDate-month',
            'id': 'estimatedDepartureDate-month'
        }
        
        self.departure_year = {
            'css_selector': 'input[data-testid="memorable-date-estimatedDepartureDate-year"]',
            'xpath': '//input[@data-testid="memorable-date-estimatedDepartureDate-year"]',
            'data_testid': 'memorable-date-estimatedDepartureDate-year',
            'id': 'estimatedDepartureDate-year'
        }
        
        # Return date selectors
        self.return_day = {
            'css_selector': 'input[data-testid="memorable-date-estimatedReturnDate-day"]',
            'xpath': '//input[@data-testid="memorable-date-estimatedReturnDate-day"]',
            'data_testid': 'memorable-date-estimatedReturnDate-day',
            'id': 'estimatedReturnDate-day'
        }
        
        self.return_month = {
            'css_selector': 'select[data-testid="memorable-date-estimatedReturnDate-month"]',
            'xpath': '//select[@data-testid="memorable-date-estimatedReturnDate-month"]',
            'data_testid': 'memorable-date-estimatedReturnDate-month',
            'id': 'estimatedReturnDate-month'
        }
        
        self.return_year = {
            'css_selector': 'input[data-testid="memorable-date-estimatedReturnDate-year"]',
            'xpath': '//input[@data-testid="memorable-date-estimatedReturnDate-year"]',
            'data_testid': 'memorable-date-estimatedReturnDate-year',
            'id': 'estimatedReturnDate-year'
        }
        
        # Country selector
        self.country_combo = {
            'css_selector': 'input[data-testid="combo-box-input"]',
            'xpath': '//input[@data-testid="combo-box-input"]',
            'data_testid': 'combo-box-input',
            'id': 'travel-destinations'
        }
        
        # Continue button
        self.continue_button = {
            'css_selector': 'button[data-testid="button"][type="submit"]',
            'xpath': '//button[@data-testid="button" and @type="submit"]',
            'data_testid': 'button'
        }
    
    def parse_countries(self, countries_string):
        """
        Parse countries string that can be in formats:
        - "united kingdom and france"
        - "united kingdom,france"
        - "united kingdom, france"
        
        Args:
            countries_string (str): String containing one or more countries
            
        Returns:
            list: List of individual country names (stripped and lowercased)
        """
        if not countries_string:
            return []
        
        # First, try splitting by " and " (case insensitive)
        countries = re.split(r'\s+and\s+', countries_string.strip(), flags=re.IGNORECASE)
        
        # If we still have just one item, try splitting by comma
        if len(countries) == 1:
            countries = [c.strip() for c in countries_string.split(',')]
        
        # Clean up each country name (strip whitespace and keep original case for matching)
        countries = [c.strip() for c in countries if c.strip()]
        
        return countries
    
    def execute(self):
        """
        Execute Step 4: Always select No for upcoming travel plans (ignoring travel_plans data)
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Always click No radio button (ignoring travel_plans value)
            logger.info("Always selecting No for travel plans (ignoring travel_plans data)")
            if not self.find_and_click_radio(self.no_radio, "No radio button"):
                logger.error("Failed to click No radio button")
                return False
            
            time.sleep(0.5)  # Wait for form to update
            
            # Validate Continue button before clicking
            logger.info("Validating Continue button...")
            continue_button_element = self.find_element(self.continue_button, "Continue button")
            
            if not continue_button_element:
                # Continue button not found - check for travel plans error
                logger.warning("Continue button not found - checking for travel plans error")
                try:
                    travel_plans_error = self.driver.find_element("css selector", 'p.usa-alert__text div')
                    if travel_plans_error:
                        error_message = travel_plans_error.text.strip()
                        logger.error(f"Travel plans error detected: {error_message}")
                        page_code = self.get_page_name_code()
                        return {
                            'status': False,
                            'code': f'{page_code}_TRAVEL_PLANS_ERROR',
                            'message': error_message
                        }
                except:
                    pass  # No travel plans error found
                
                logger.error("Continue button not found and travel plans error detected")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_CONTINUE_BUTTON_NOT_FOUND',
                    'message': 'We couldn\'t proceed with your travel information. Please check your details and try again.'
                }
            
            # Check if continue button is disabled
            if not continue_button_element.is_enabled():
                # Continue button is disabled - check for date error
                logger.warning("Continue button is disabled - checking for date error")
                try:
                    date_error = self.driver.find_element("css selector", 'span[data-testid="errorMessage"]')
                    if date_error:
                        error_message = date_error.text.strip()
                        logger.error(f"Date error detected: {error_message}")
                        page_code = self.get_page_name_code()
                        return {
                            'status': False,
                            'code': f'{page_code}_TRAVEL_PLANS_ERROR',
                            'message': error_message
                        }
                except:
                    pass  # No date error found
                
                logger.error("Continue button is disabled but no date error detected")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_CONTINUE_BUTTON_DISABLED',
                    'message': 'Please check your travel information and try again.'
                }
            
            # Click Continue button
            logger.info("Clicking Continue button...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_CONTINUE_BUTTON_CLICK_FAILED',
                    'message': 'We couldn\'t proceed with your request. Please try again.'
                }
            
            # Wait 2 seconds after clicking button
            logger.info("waiting 2 seconds after clicking Continue...")
            time.sleep(2)
            
            # Check for errors after clicking continue
            logger.info("Checking for errors after clicking Continue...")
            error_result = self.check_for_page_errors()
            if error_result:
                return error_result
            
            logger.info("✅ Step 4 completed successfully - Upcoming travel form submitted")
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 4 completed successfully - Upcoming travel form submitted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 4 failed with error: {str(e)}")
            page_code = self.get_page_name_code()
            return {
                'status': False,
                'code': f'{page_code}_EXCEPTION',
                'message': 'We encountered an issue processing your travel information. Please try again.'
            }
