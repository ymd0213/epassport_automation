"""
Step 4: Upcoming Travel Page Automation
Handles travel plans selection and form filling based on travel_plans value
"""

import time
import logging
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
    
    def execute(self):
        """
        Execute Step 4: Handle upcoming travel plans based on travel_plans value
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            travel_plans = str(self.travel_data.get('travel_plans', '0'))
            logger.info(f"Travel plans value: {travel_plans}")
            
            if travel_plans == "1":
                # User has travel plans - click Yes radio button
                logger.info("User has travel plans - selecting Yes")
                if not self.find_and_click_radio(self.yes_radio, "Yes radio button"):
                    logger.error("Failed to click Yes radio button")
                    return False
                
                time.sleep(2)  # Wait for form fields to appear
                
                # Fill departure date
                logger.info("Filling departure date...")
                if not self.find_and_input_text(self.departure_day, str(self.travel_data.get('trip_abroad_day', '')), "departure day"):
                    logger.error("Failed to input departure day")
                    return False
                time.sleep(2)  # 2 second delay after input
                
                # Convert month number to 0-based index (January = 0, December = 11)
                departure_month = self.travel_data.get('trip_abroad_month', '')
                if departure_month:
                    month_index = str(int(departure_month) - 1)
                    if not self.find_and_select_option(self.departure_month, month_index, "departure month"):
                        logger.error("Failed to select departure month")
                        return False
                time.sleep(2)  # 2 second delay after select
                
                if not self.find_and_input_text(self.departure_year, str(self.travel_data.get('trip_abroad_year', '')), "departure year"):
                    logger.error("Failed to input departure year")
                    return False
                time.sleep(2)  # 2 second delay after input
                
                # Fill return date
                logger.info("Filling return date...")
                if not self.find_and_input_text(self.return_day, str(self.travel_data.get('trip_return_day', '')), "return day"):
                    logger.error("Failed to input return day")
                    return False
                time.sleep(2)  # 2 second delay after input
                
                # Convert month number to 0-based index (January = 0, December = 11)
                return_month = self.travel_data.get('trip_return_month', '')
                if return_month:
                    month_index = str(int(return_month) - 1)
                    if not self.find_and_select_option(self.return_month, month_index, "return month"):
                        logger.error("Failed to select return month")
                        return False
                time.sleep(2)  # 2 second delay after select
                
                if not self.find_and_input_text(self.return_year, str(self.travel_data.get('trip_return_year', '')), "return year"):
                    logger.error("Failed to input return year")
                    return False
                time.sleep(2)  # 2 second delay after input
                
                # Select country
                logger.info("Selecting travel destination...")
                country = self.travel_data.get('trip_abroad_countries', '')
                if country:
                    if not self.find_and_select_combo_box(self.country_combo, country, "travel destination combo box"):
                        logger.error("Failed to select travel destination")
                        return False
                    time.sleep(2)  # 2 second delay after combo box selection
                else:
                    logger.warning("No travel destination specified")
            
            else:
                # User has no travel plans - click No radio button
                logger.info("User has no travel plans - selecting No")
                if not self.find_and_click_radio(self.no_radio, "No radio button"):
                    logger.error("Failed to click No radio button")
                    return False
            
            time.sleep(2)  # Wait for form to update
            
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
                        return {
                            'status': False,
                            'code': 'TRAVEL_PLANS_ERROR',
                            'message': error_message
                        }
                except:
                    pass  # No travel plans error found
                
                logger.error("Continue button not found and travel plans error detected")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_NOT_FOUND',
                    'message': 'Continue button not found and travel plans error detected'
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
                        return {
                            'status': False,
                            'code': 'TRAVEL_PLANS_ERROR',
                            'message': error_message
                        }
                except:
                    pass  # No date error found
                
                logger.error("Continue button is disabled but no date error detected")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_DISABLED',
                    'message': 'Continue button is disabled but no date error detected'
                }
            
            # Click Continue button
            logger.info("Clicking Continue button...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                return {
                    'status': False,
                    'code': 'CONTINUE_BUTTON_CLICK_FAILED',
                    'message': 'Failed to click Continue button'
                }
            
            logger.info("✅ Step 4 completed successfully - Upcoming travel form submitted")
            
            # Wait 5 seconds as requested
            logger.info("Waiting 5 seconds...")
            time.sleep(5)
            
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 4 completed successfully - Upcoming travel form submitted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 4 failed with error: {str(e)}")
            return {
                'status': False,
                'code': 'STEP4_EXCEPTION',
                'message': f'Step 4 failed with error: {str(e)}'
            }
