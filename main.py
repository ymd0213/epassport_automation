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


def fetch_single_passport_application():
    """
    Fetch a single passport application from backend API
    
    Returns:
        dict: Application data with 'id' and 'data' keys, or None if no application available
    """
    try:
        # Load environment variables
        load_dotenv()
        api_endpoint = os.getenv('API_ENDPOINT')
        
        if not api_endpoint:
            logger.error("API_ENDPOINT not found in .env file")
            return None
        
        logger.info(f"Fetching passport application from API: {api_endpoint}")
        
        # Make GET request to the API with timeout
        response = requests.get(api_endpoint, timeout=10)  # 10 second timeout
        response.raise_for_status()
        
        # Log response status and content type
        logger.info(f"API response status: {response.status_code}, Content-Type: {response.headers.get('content-type')}")
        
        # Parse JSON response
        try:
            api_data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response as JSON: {str(e)}")
            logger.error(f"Response text: {response.text[:500]}")  # Log first 500 chars
            return None
        
        # Log the actual response for debugging
        logger.info(f"API response type: {type(api_data)}")
        if isinstance(api_data, dict):
            logger.info(f"API response keys: {list(api_data.keys())}")
        
        # Check if API returned an error status (no applications available)
        if isinstance(api_data, dict) and api_data.get('status') == 'error':
            message = api_data.get('message', 'Unknown error')
            logger.info(f"API returned error status: {message}")
            return None
        
        # Check if response has 'data' key
        if 'data' not in api_data:
            logger.error(f"Invalid API response format: 'data' key not found.")
            if isinstance(api_data, dict):
                logger.error(f"Response keys: {list(api_data.keys())}")
                logger.error(f"Response sample: {str(api_data)[:500]}")
            return None
        
        # Handle if 'data' is None or null
        if api_data['data'] is None:
            logger.info("API returned null data - no passport applications available")
            return None
        
        # Check if 'data' is a list
        if not isinstance(api_data['data'], list):
            logger.error(f"Invalid API response format: 'data' is not a list. Type: {type(api_data['data'])}")
            logger.error(f"Data value: {str(api_data['data'])[:500]}")
            
            # If data is an object with an 'id', try to process it as a single application
            if isinstance(api_data['data'], dict) and 'id' in api_data['data']:
                logger.info("API returned single application object instead of array, wrapping it in array")
                api_data['data'] = [api_data['data']]
            else:
                return None
        
        # Check if there's any data
        if len(api_data['data']) == 0:
            logger.info("No passport applications available in API (empty array)")
            return None
        
        # Get the first application
        application = api_data['data'][0]
        
        # Log what we're processing
        logger.info(f"Processing application with ID: {application.get('id', 'Unknown')}")
        
        try:
            # Extract and parse the nested 'data' field if it's a JSON string
            nested_data = application.get('data')
            if nested_data:
                # If 'data' is a string, parse it as JSON
                if isinstance(nested_data, str):
                    try:
                        parsed_data = json.loads(nested_data)
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse application data field: {str(e)}")
                        return None
                else:
                    # If 'data' is already an object, use it directly
                    parsed_data = nested_data
                
                application_id = application.get('id')
                applicant_name = f"{parsed_data.get('first_name', 'Unknown')} {parsed_data.get('last_name', 'Unknown')}"
                
                logger.info(f"Fetched application ID: {application_id}, Applicant: {applicant_name}")
                
                # Return the application with parsed data and top-level fields preserved
                return {
                    'id': application_id,
                    'data': parsed_data,
                    'billing_info': application.get('billing_info'),
                    'photo_url': application.get('photo_url')
                }
            else:
                logger.warning("Application has no 'data' field")
                return None
        except Exception as e:
            logger.error(f"Failed to process application data: {str(e)}")
            return None
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch data from API: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Failed to load passport data: {str(e)}")
        return None

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
        renewal_status: "2" for error in steps 1-14, "3" for error in step 15, "5" for success
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
    # Extract the nested data object
    data = passport_data.get('data', {})
    application_id = passport_data.get('id', 'Unknown')
    
    # Merge top-level fields (billing_info, photo_url) into data for easier access in steps
    # This ensures all steps receive complete data in a single object
    if 'billing_info' in passport_data:
        data['billing_info'] = passport_data['billing_info']
    
    if 'photo_url' in passport_data:
        data['photo_url'] = passport_data['photo_url']
    
    # Get applicant name for logging
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
            {"num": 7, "name": "Passport Photo Upload", "class": Step7PassportPhoto, "params": [driver, data]},
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
            # Steps 1-14: renewal_status = "2", Step 15: renewal_status = "3"
            if failed_step == 15:
                update_application_status(application_id, "3", failed_error)
            else:
                update_application_status(application_id, "2", failed_error)
            
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
            update_application_status(application_id, "5")
            
            return {
                'success': True,
                'results': results
            }
        
    except Exception as e:
        logger.error(f"Error processing application {app_index + 1}: {str(e)}")
        print(f"❌ Error processing application {app_index + 1}: {str(e)}")
        
        # Update backend with exception error
        # For exceptions, determine which step we were on based on results
        exception_error = {
            "code": "APPLICATION_EXCEPTION",
            "message": f"Error processing application: {str(e)}"
        }
        # Check if we have results to determine the last attempted step
        if results:
            last_step = max([int(k.replace('step', '')) for k in results.keys() if k.startswith('step')])
            if last_step == 15:
                update_application_status(application_id, "3", exception_error)
            else:
                update_application_status(application_id, "2", exception_error)
        else:
            # If no steps completed, default to steps 1-14 error
            update_application_status(application_id, "2", exception_error)
        
        return {
            'success': False,
            'error': exception_error,
            'results': results
        }


def main():
    """Main function to run the undetected automation in continuous loop"""
    print("Undetected ChromeDriver Web Automation - Continuous Mode")
    print("=" * 50)
    
    # Create automation instance once
    automation = UndetectedWebAutomation(headless=False)
    
    # Track statistics
    total_processed = 0
    total_successful = 0
    total_failed = 0
    
    # Target URL
    target_url = "https://opr.travel.state.gov/"
    
    # Setup driver once at the beginning
    try:
        if not automation.setup_driver():
            print("Failed to setup undetected ChromeDriver")
            return
        
        print("ChromeDriver setup successful!")
        print("Waiting 5 seconds before navigation...")
        time.sleep(5)
        
        # Initial navigation to the OPR website
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
        print("\nWaiting 30 seconds after initial navigation...")
        time.sleep(30)
        
        print("\n" + "="*70)
        print("🔄 STARTING CONTINUOUS APPLICATION PROCESSING")
        print("="*70)
        print("The system will continuously check for new applications from the API.")
        print("Press Ctrl+C to stop the automation.\n")
        
        # Infinite loop to process applications
        while True:
            try:
                print("\n" + ">"*70)
                print(f"📡 Fetching next application from API...")
                print(">"*70)
                
                # Fetch single application from API
                passport_data = fetch_single_passport_application()
                
                if not passport_data:
                    print("⏸️  No application data available from API")
                    print("⏳ Waiting 20 seconds before next check...")
                    time.sleep(20)
                    continue
                
                # Process the application
                total_processed += 1
                app_results = process_single_application(
                    automation.driver, 
                    passport_data, 
                    total_processed - 1,  # 0-based index
                    total_processed  # Display current count as total
                )
                
                # Update statistics
                if app_results.get('success', False):
                    total_successful += 1
                else:
                    total_failed += 1
                
                # Print current session statistics
                print("\n" + "="*70)
                print("📊 SESSION STATISTICS")
                print("="*70)
                print(f"Total Processed: {total_processed}")
                print(f"Successful: {total_successful} ✅")
                print(f"Failed: {total_failed} ❌")
                print("="*70)
                
                # Navigate back to start for next application
                print("\n" + ">"*50)
                print("🔄 Preparing for next application...")
                print(">"*50)
                time.sleep(5)
                automation.navigate_to_url(target_url)
                time.sleep(10)
                
            except KeyboardInterrupt:
                print("\n\n" + "="*70)
                print("⚠️  Keyboard interrupt detected. Stopping automation...")
                print("="*70)
                break
                
            except Exception as e:
                logger.error(f"Error in main loop: {str(e)}")
                print(f"❌ Error in main loop: {str(e)}")
                print("⏳ Waiting 20 seconds before retry...")
                time.sleep(20)
                # Try to recover by navigating back to start
                try:
                    automation.navigate_to_url(target_url)
                    time.sleep(10)
                except:
                    pass
    
    except Exception as e:
        logger.error(f"Critical error in automation: {str(e)}")
        print(f"❌ Critical error occurred: {str(e)}")
    
    finally:
        # Print final summary
        print("\n" + "="*70)
        print("🏁 FINAL SESSION SUMMARY")
        print("="*70)
        print(f"Total Applications Processed: {total_processed}")
        print(f"Successful: {total_successful} ✅")
        print(f"Failed: {total_failed} ❌")
        print("="*70)
        print("\n⚠️  Browser will remain open. Close manually if needed.")
        logger.info(f"Automation session ended. Processed: {total_processed}, Success: {total_successful}, Failed: {total_failed}")


if __name__ == "__main__":
    main()
