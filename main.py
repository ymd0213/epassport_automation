"""
Undetected ChromeDriver Web Automation Script
Uses undetected_chromedriver to navigate to https://opr.travel.state.gov/
"""

import undetected_chromedriver as uc
import time
import logging
import platform
import subprocess
import os
import json
import requests
from dotenv import load_dotenv
from steps.step1_landing_page import Step1LandingPage
from steps.step2_what_you_need import Step2WhatYouNeed
from steps.step3_eligibility_requirements import Step3EligibilityRequirements
from steps.step4_upcoming_travel import Step4UpcomingTravel
from steps.step5_terms_and_conditions import Step5TermsAndConditions
from steps.step6_what_are_you_renewing import Step6WhatAreYouRenewing
from steps.step7_passport_photo import Step7PassportPhoto
from steps.step8_personal_information import Step8PersonalInformation
from steps.step9_emergency_contact import Step9EmergencyContact
from steps.step10_passport_options import Step10PassportOptions
from steps.step11_mailing_address import Step11MailingAddress
from steps.step12_passport_delivery import Step12PassportDelivery
from steps.step13_review_order import Step13ReviewOrder
from steps.step14_statement_of_truth import Step14StatementOfTruth
from steps.step15_payment import Step15Payment

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class UndetectedWebAutomation:
    def __init__(self, headless=False):
        """
        Initialize the UndetectedWebAutomation class
        
        Args:
            headless (bool): Run browser in headless mode
        """
        self.driver = None
        self.headless = headless
        
    def get_chrome_version(self):
        """Get Chrome browser version"""
        try:
            if platform.system() == "Windows":
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                return version
        except:
            pass
        return None
        
    def create_chrome_options(self):
        """Create fresh Chrome options for each attempt"""
        options = uc.ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        # Additional options for better performance
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        
        return options
        
    def setup_driver(self):
        """Setup undetected Chrome WebDriver with auto-downloaded ChromeDriver"""
        try:
            logger.info("Setting up undetected ChromeDriver...")
            
            # Use auto-download for best version compatibility
            logger.info("Using auto-downloaded ChromeDriver for optimal version compatibility...")
            
            # Get Chrome version for better compatibility
            chrome_version = self.get_chrome_version()
            if chrome_version:
                logger.info(f"Detected Chrome version: {chrome_version}")
                # Extract major version number
                try:
                    major_version = int(chrome_version.split('.')[0])
                except:
                    major_version = None
            else:
                major_version = None
                logger.warning("Could not detect Chrome version")
            
            # Try different approaches to handle version compatibility
            # Method 1: Try auto-download first (best compatibility)
            try:
                logger.info("Method 1: Attempting auto-download ChromeDriver...")
                options = self.create_chrome_options()
                self.driver = uc.Chrome(options=options, version_main=None)
                logger.info("✅ Undetected ChromeDriver setup successful with auto-download")
                return True
                
            except Exception as e1:
                logger.warning(f"Auto-download failed: {str(e1)}")
                
                # Method 2: Try auto-download with detected Chrome version
                if major_version:
                    try:
                        logger.info(f"Method 2: Attempting auto-download with Chrome version {major_version}...")
                        options = self.create_chrome_options()
                        self.driver = uc.Chrome(options=options, version_main=major_version)
                        logger.info(f"✅ Undetected ChromeDriver setup successful with auto-download and version {major_version}")
                        return True
                        
                    except Exception as e2:
                        logger.warning(f"Auto-download with version {major_version} failed: {str(e2)}")
                
                # Method 3: Try auto-download with version 140
                try:
                    logger.info("Method 3: Attempting auto-download with version 140...")
                    options = self.create_chrome_options()
                    self.driver = uc.Chrome(options=options, version_main=140)
                    logger.info("✅ Undetected ChromeDriver setup successful with auto-download and version 140")
                    return True
                    
                except Exception as e3:
                    logger.warning(f"Auto-download with version 140 failed: {str(e3)}")
                    
                    # Method 4: Try auto-download with version 141 as fallback
                    try:
                        logger.info("Method 4: Attempting auto-download with version 141...")
                        options = self.create_chrome_options()
                        self.driver = uc.Chrome(options=options, version_main=141)
                        logger.info("✅ Undetected ChromeDriver setup successful with auto-download and version 141")
                        return True
                        
                    except Exception as e4:
                        logger.error(f"All auto-download methods failed. Last error: {str(e4)}")
                        return False
            
        except Exception as e:
            logger.error(f"Failed to setup undetected ChromeDriver: {str(e)}")
            return False
    
    def navigate_to_url(self, url):
        """Navigate to a specific URL"""
        try:
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Get page title
            title = self.driver.title
            logger.info(f"Page loaded successfully. Title: {title}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            return False
    
    def get_page_info(self):
        """Get current page information"""
        try:
            title = self.driver.title
            current_url = self.driver.current_url
            
            logger.info(f"Current page title: {title}")
            logger.info(f"Current URL: {current_url}")
            
            return {
                'title': title,
                'url': current_url
            }
            
        except Exception as e:
            logger.error(f"Failed to get page info: {str(e)}")
            return None
    
    def wait_for_element(self, locator, timeout=10):
        """Wait for an element to be present"""
        try:
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located(locator))
            return element
            
        except Exception as e:
            logger.error(f"Element not found: {str(e)}")
            return None
    
    def close_driver(self):
        """Close the WebDriver"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
        except Exception as e:
            logger.error(f"Error closing WebDriver: {str(e)}")
        finally:
            self.driver = None


def load_passport_data():
    """Load passport data from backend API"""
    try:
        # Load environment variables
        load_dotenv()
        api_endpoint = os.getenv('API_ENDPOINT')
        
        if not api_endpoint:
            logger.error("API_ENDPOINT not found in .env file")
            return []
        
        logger.info(f"Fetching passport data from API: {api_endpoint}")
        
        # Make GET request to the API with timeout
        response = requests.get(api_endpoint, timeout=10)  # 10 second timeout
        response.raise_for_status()
        
        # Parse JSON response
        api_data = response.json()
        
        if 'data' not in api_data or not isinstance(api_data['data'], list):
            logger.error("Invalid API response format: 'data' key not found or is not a list")
            return []
        
        # Get first 5 results
        first_five = api_data['data'][:5]
        logger.info(f"Retrieved {len(api_data['data'])} applications from API, using first {len(first_five)}")
        
        # Parse the 'data' field from each application (it's a JSON string)
        passport_data = []
        for idx, application in enumerate(first_five):
            try:
                if 'data' in application and application['data']:
                    # Parse the JSON string in the 'data' field
                    parsed_data = json.loads(application['data'])
                    # Append both id and parsed data
                    passport_data.append({
                        'id': application.get('id'),
                        'data': parsed_data
                    })
                    logger.info(f"Application {idx + 1} (ID: {application.get('id')}): Parsed data for {parsed_data.get('first_name', 'Unknown')} {parsed_data.get('last_name', 'Unknown')}")
                else:
                    logger.warning(f"Application {idx + 1}: No 'data' field found")
            except json.JSONDecodeError as e:
                logger.error(f"Application {idx + 1}: Failed to parse data field: {str(e)}")
            except Exception as e:
                logger.error(f"Application {idx + 1}: Error processing application: {str(e)}")
        
        logger.info(f"Successfully loaded {len(passport_data)} passport applications from API")
        return passport_data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from API: {str(e)}")
        return []
    except Exception as e:
        logger.error(f"Failed to load passport data: {str(e)}")
        return []

def extract_step_result(step_result):
    """
    Extract status, code, and message from step result
    
    Args:
        step_result: Can be bool or dict with status, code, message
        
    Returns:
        tuple: (success: bool, code: str, message: str)
    """
    if isinstance(step_result, dict):
        success = step_result.get('status', False)
        code = step_result.get('code', 'UNKNOWN_ERROR')
        message = step_result.get('message', 'Step failed')
        return success, code, message
    elif isinstance(step_result, bool):
        if step_result:
            return True, 'SUCCESS', 'Step completed successfully'
        else:
            return False, 'STEP_FAILED', 'Step failed'
    else:
        return False, 'INVALID_RESULT', 'Invalid step result type'


def update_application_status(application_id, renewal_status, renewal_error=None):
    """
    Update application status via backend API
    
    Args:
        application_id: The application ID
        renewal_status: "1" for failed, "2" for success
        renewal_error: Dict with code and message (optional, for failures)
        
    Returns:
        bool: True if update was successful, False otherwise
    """
    try:
        load_dotenv()
        update_endpoint = os.getenv('API_ENDPOINT')
        
        if not update_endpoint:
            logger.error("API_ENDPOINT not found in .env file")
            return False
        
        # Prepare request body
        request_body = {
            "id": str(application_id),
            "renewal_status": renewal_status
        }
        
        # Add renewal_error if provided (for failed cases)
        if renewal_error:
            request_body["renewal_error"] = json.dumps(renewal_error)
        
        logger.info(f"Updating application status for ID {application_id}: {request_body}")
        
        # Make POST request to update status
        response = requests.post(update_endpoint, json=request_body, timeout=10)
        response.raise_for_status()
        
        logger.info(f"✅ Successfully updated status for application {application_id}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Failed to update status via API: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"❌ Error updating application status: {str(e)}")
        return False


def process_single_application(driver, passport_data, app_index, total_apps):
    """
    Process a single passport application through all steps
    
    Args:
        driver: Selenium WebDriver instance
        passport_data: Dictionary containing passport application data (with 'id' and 'data' keys)
        app_index: Current application index (0-based)
        total_apps: Total number of applications to process
        
    Returns:
        dict: Dictionary containing success status and results for the application
    """
    data = passport_data.get('data', {})
    application_id = passport_data.get('id', 'Unknown')
    applicant_name = f"{data.get('first_name', 'Unknown')} {data.get('last_name', 'Unknown')}"
    
    print("\n" + "#"*70)
    print(f"# PROCESSING APPLICATION {app_index + 1}/{total_apps}")
    print(f"# Application ID: {application_id}")
    print(f"# Applicant: {applicant_name}")
    print("#"*70)
    
    results = {}
    failed_step = None
    failed_error = None
    
    try:
        # Define all steps with their configurations
        steps = [
            {"num": 1, "name": "Landing Page", "class": Step1LandingPage, "params": [driver]},
            {"num": 2, "name": "What You Need", "class": Step2WhatYouNeed, "params": [driver]},
            {"num": 3, "name": "Eligibility Requirements", "class": Step3EligibilityRequirements, "params": [driver]},
            {"num": 4, "name": "Upcoming Travel", "class": Step4UpcomingTravel, "params": [driver, data]},
            {"num": 5, "name": "Terms and Conditions", "class": Step5TermsAndConditions, "params": [driver]},
            {"num": 6, "name": "What Are You Renewing", "class": Step6WhatAreYouRenewing, "params": [driver, data]},
            {"num": 7, "name": "Passport Photo Upload", "class": Step7PassportPhoto, "params": [driver]},
            {"num": 8, "name": "Personal Information", "class": Step8PersonalInformation, "params": [driver, data]},
            {"num": 9, "name": "Emergency Contact", "class": Step9EmergencyContact, "params": [driver, data]},
            {"num": 10, "name": "Passport Options", "class": Step10PassportOptions, "params": [driver, data]},
            {"num": 11, "name": "Mailing Address", "class": Step11MailingAddress, "params": [driver, data]},
            {"num": 12, "name": "Passport Delivery", "class": Step12PassportDelivery, "params": [driver, data]},
            {"num": 13, "name": "Review Order", "class": Step13ReviewOrder, "params": [driver, data]},
            {"num": 14, "name": "Statement of Truth", "class": Step14StatementOfTruth, "params": [driver, data]},
            {"num": 15, "name": "Payment", "class": Step15Payment, "params": [driver, data]},
        ]
        
        # Execute each step
        for step_config in steps:
            step_num = step_config["num"]
            step_name = step_config["name"]
            step_key = f"step{step_num}"
            
            print("\n" + "="*50)
            print(f"EXECUTING STEP {step_num}: {step_name.upper()}")
            print("="*50)
            
            # Execute step
            step_instance = step_config["class"](*step_config["params"])
            step_result = step_instance.execute()
            
            # Extract result details
            success, code, message = extract_step_result(step_result)
            results[step_key] = success
            
            if not success:
                print(f"❌ Step {step_num} failed: {message}")
                failed_step = step_num
                failed_error = {
                    "code": code,
                    "message": message
                }
                logger.error(f"Application {application_id} failed at Step {step_num}: {code} - {message}")
                break  # Stop processing further steps
            else:
                print(f"✅ Step {step_num} completed successfully")
        
        # Print summary for this application
        print("\n" + "="*50)
        print(f"SUMMARY FOR APPLICATION {app_index + 1}: {applicant_name}")
        print("="*50)
        
        # Display executed steps
        for step_config in steps:
            step_num = step_config["num"]
            step_name = step_config["name"]
            step_key = f"step{step_num}"
            
            if step_key in results:
                status = '✅ SUCCESS' if results[step_key] else '❌ FAILED'
                print(f"Step {step_num} ({step_name}): {status}")
            else:
                print(f"Step {step_num} ({step_name}): ⏭️  SKIPPED")
        
        # Determine overall status and update backend
        if failed_step:
            print(f"\n❌ APPLICATION {app_index + 1} FAILED AT STEP {failed_step}")
            print(f"Error: {failed_error['code']} - {failed_error['message']}")
            print("="*50)
            
            # Update backend with failure status
            update_application_status(application_id, "1", failed_error)
            
            return {
                'success': False,
                'failed_step': failed_step,
                'error': failed_error,
                'results': results
            }
        else:
            print(f"\n🎉 APPLICATION {app_index + 1} COMPLETED SUCCESSFULLY!")
            print("="*50)
            
            # Update backend with success status
            update_application_status(application_id, "2")
            
            return {
                'success': True,
                'results': results
            }
        
    except Exception as e:
        logger.error(f"Error processing application {app_index + 1}: {str(e)}")
        print(f"❌ Error processing application {app_index + 1}: {str(e)}")
        
        # Update backend with exception error
        exception_error = {
            "code": "APPLICATION_EXCEPTION",
            "message": f"Error processing application: {str(e)}"
        }
        update_application_status(application_id, "1", exception_error)
        
        return {
            'success': False,
            'error': exception_error,
            'results': results
        }


def main():
    """Main function to run the undetected automation"""
    print("Undetected ChromeDriver Web Automation")
    print("=" * 50)
    
    # Load passport data from API
    passport_data_list = load_passport_data()
    if not passport_data_list:
        print("No passport data found. Exiting...")
        return
    
    print(f"Loaded {len(passport_data_list)} passport application(s) from API")
    
    # Create automation instance
    automation = UndetectedWebAutomation(headless=False)
    
    # Track overall results
    all_applications_results = []
    
    try:
        # Setup driver once for all applications
        if not automation.setup_driver():
            print("Failed to setup undetected ChromeDriver")
            return
        
        print("ChromeDriver setup successful!")
        print("Waiting 5 seconds before navigation...")
        time.sleep(5)
        
        # Navigate to the OPR website
        target_url = "https://opr.travel.state.gov/"
        if not automation.navigate_to_url(target_url):
            print(f"Failed to navigate to {target_url}")
            return
            
        print(f"Successfully navigated to {target_url}")
        
        # Get page information
        page_info = automation.get_page_info()
        if page_info:
            print(f"Page Title: {page_info['title']}")
            print(f"Current URL: {page_info['url']}")
        
        # Wait 30 seconds after initial navigation
        print("\nWaiting 30 seconds after navigation...")
        time.sleep(30)
        
        # Process each passport application
        total_apps = len(passport_data_list)
        for index, passport_data in enumerate(passport_data_list):
            app_results = process_single_application(
                automation.driver, 
                passport_data, 
                index, 
                total_apps
            )
            data = passport_data.get('data', {})
            all_applications_results.append({
                'index': index + 1,
                'name': f"{data.get('first_name', 'Unknown')} {data.get('last_name', 'Unknown')}",
                'success': app_results.get('success', False),
                'failed_step': app_results.get('failed_step'),
                'error': app_results.get('error'),
                'results': app_results.get('results', {})
            })
            
            # If not the last application, navigate back to start for next one
            if index < total_apps - 1:
                print("\n" + ">"*50)
                print(f"Preparing for next application ({index + 2}/{total_apps})...")
                print(">"*50)
                time.sleep(5)
                # Navigate back to the starting page for the next application
                automation.navigate_to_url(target_url)
                time.sleep(10)
        
        # Print final overall summary
        print("\n" + "="*70)
        print("=" * 70)
        print("FINAL SUMMARY - ALL APPLICATIONS")
        print("=" * 70)
        print("="*70 + "\n")
        
        total_successful_apps = 0
        total_failed_apps = 0
        for app_result in all_applications_results:
            if app_result['success']:
                status = "✅ COMPLETE"
                total_successful_apps += 1
            else:
                failed_step = app_result.get('failed_step', 'Unknown')
                error_code = app_result.get('error', {}).get('code', 'Unknown')
                status = f"❌ FAILED at Step {failed_step} ({error_code})"
                total_failed_apps += 1
            
            print(f"Application {app_result['index']}: {app_result['name']} - {status}")
        
        print("\n" + "="*70)
        print(f"Total Applications Processed: {len(all_applications_results)}")
        print(f"Successful: {total_successful_apps}")
        print(f"Failed: {total_failed_apps}")
        print("="*70)
    
    except Exception as e:
        logger.error(f"Error in main automation: {str(e)}")
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Don't close the driver - keep browser open as requested
        print("\nAutomation completed! Browser will remain open.")


if __name__ == "__main__":
    main()
