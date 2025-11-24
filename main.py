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
import argparse
import multiprocessing
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

# Configure logging (only errors)
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
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
        options.add_argument("--window-size=640,480")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-logging")
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-notifications")
        
        return options
    
    def setup_driver(self):
        """
        Setup undetected Chrome WebDriver with auto-downloaded ChromeDriver
        """
        try:
            # Get Chrome version for better compatibility
            chrome_version = self.get_chrome_version()
            if chrome_version:
                try:
                    major_version = int(chrome_version.split('.')[0])
                except:
                    major_version = None
            else:
                major_version = None
            
            # Try different versions systematically
            versions_to_try = []
            
            # Start with detected version if available
            if major_version:
                versions_to_try.append(major_version)
            
            # Add common versions
            versions_to_try.extend([None, 141, 140, 131, 130, 129])
            
            # Remove duplicates while preserving order
            seen = set()
            versions_to_try = [x for x in versions_to_try if not (x in seen or seen.add(x))]
            
            # Try each version
            for idx, version in enumerate(versions_to_try, 1):
                try:
                    options = self.create_chrome_options()
                    self.driver = uc.Chrome(options=options, version_main=version)
                    return True
                    
                except Exception as e:
                    continue
            
            # If we get here, all versions failed
            logger.error("All ChromeDriver versions failed to initialize")
            return False
            
        except Exception as e:
            logger.error(f"Failed to setup undetected ChromeDriver: {str(e)}")
            return False
    
    def navigate_to_url(self, url):
        """Navigate to a specific URL"""
        try:
            self.driver.get(url)
            
            # Wait for page to load
            time.sleep(3)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to navigate to {url}: {str(e)}")
            return False
    
    def get_page_info(self):
        """Get current page information"""
        try:
            title = self.driver.title
            current_url = self.driver.current_url
            
            return {
                'title': title,
                'url': current_url
            }
            
        except Exception as e:
            logger.error(f"Failed to get page info: {str(e)}")
            return None
    
    def handle_cloudflare_captcha(self, timeout=30):
        """
        Handle Cloudflare v2 captcha by clicking the checkbox if present
        
        Args:
            timeout (int): Maximum time to wait for captcha to appear and complete (default: 30 seconds)
            
        Returns:
            bool: True if captcha was found and clicked, False if no captcha found
        """
        try:
            from selenium.webdriver.common.by import By
            
            # Wait a moment for page to fully load
            time.sleep(2)
            
            # Retry logic for finding and clicking captcha
            max_attempts = 6  # Try up to 6 times
            check_interval = 2  # Wait 2 seconds between attempts
            
            for attempt in range(max_attempts):
                if attempt > 0:
                    logger.info(f"Captcha click attempt {attempt + 1}/{max_attempts}")
                    time.sleep(check_interval)
                
                try:
                    # Try to find main-wrapper element
                    main_wrappers = self.driver.find_elements(By.CSS_SELECTOR, "div.main-wrapper[role='main']")
                    if not main_wrappers:
                        main_wrappers = self.driver.find_elements(By.CSS_SELECTOR, "div.main-wrapper")
                    
                    if not main_wrappers:
                        continue
                    
                    # Find visible wrapper
                    main_wrapper = None
                    for wrapper in main_wrappers:
                        try:
                            if wrapper.is_displayed():
                                main_wrapper = wrapper
                                break
                        except:
                            continue
                    
                    if not main_wrapper:
                        continue
                    
                    # Try to click the captcha
                    try:
                        # Scroll into view
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", main_wrapper)
                        time.sleep(1)
                        
                        # Try JavaScript click
                        self.driver.execute_script("arguments[0].click();", main_wrapper)
                        logger.info("Successfully clicked Cloudflare captcha")
                        
                        # Wait for captcha to process
                        time.sleep(5)
                        
                        # Verify if captcha is gone (successful click)
                        verify_wrappers = self.driver.find_elements(By.CSS_SELECTOR, "div.main-wrapper")
                        captcha_still_present = False
                        for wrapper in verify_wrappers:
                            try:
                                if wrapper.is_displayed():
                                    captcha_still_present = True
                                    break
                            except:
                                continue
                        
                        if not captcha_still_present:
                            logger.info("Captcha successfully resolved")
                            return True
                        else:
                            logger.info("Captcha still present, retrying...")
                            continue
                            
                    except Exception as click_error:
                        logger.warning(f"Click attempt failed: {str(click_error)}")
                        continue
                        
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                    continue
            
            # If we've exhausted all attempts
            logger.info("No Cloudflare captcha found or unable to click it")
            return False
                
        except Exception as e:
            logger.error(f"Error handling captcha: {str(e)}")
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return False
    
    def close_driver(self):
        """Close the WebDriver"""
        try:
            if self.driver:
                self.driver.quit()
        except Exception as e:
            logger.error(f"Error closing WebDriver: {str(e)}")
        finally:
            self.driver = None
    


def fetch_single_passport_application(props=None):
    """
    Fetch a single passport application from backend API
    
    Args:
        props (dict): Optional dictionary containing:
            - application_processing_method (str): "normal" or "failed"
            - error_code (str): Required if method is "failed", e.g., "STEP6_ERROR"
    
    Returns:
        dict: Application data with 'id' and 'data' keys, or None if no application available
    """
    try:
        # Load environment variables
        load_dotenv()
        
        # Default to "normal" if props not provided
        if props is None:
            props = {}
        
        method = props.get('application_processing_method', 'normal')
        
        if method == 'failed':
            # Use error endpoint for failed applications
            api_endpoint = os.getenv('API_ENDPOINT_ERROR')
            
            if not api_endpoint:
                logger.error("API_ENDPOINT_ERROR not found in .env file")
                return None
            
            error_code = props.get('error_code')
            if not error_code:
                logger.error("error_code is required when application_processing_method is 'failed'")
                return None
            
            
            # Make POST request to the API with error_code parameter
            response = requests.post(api_endpoint, json={'error_code': error_code}, timeout=10)
            response.raise_for_status()
        else:
            # Use normal endpoint for normal applications
            api_endpoint = os.getenv('API_ENDPOINT')
            
            if not api_endpoint:
                logger.error("API_ENDPOINT not found in .env file")
                return None
            
            
            # Make GET request to the API with timeout
            response = requests.get(api_endpoint, timeout=10)  # 10 second timeout
            response.raise_for_status()
        
        # Parse JSON response
        try:
            api_data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse API response as JSON: {str(e)}")
            return None
        
        # Check if API returned an error status (no applications available)
        if isinstance(api_data, dict) and api_data.get('status') == 'error':
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
            return None
        
        # Check if 'data' is a list
        if not isinstance(api_data['data'], list):
            logger.error(f"Invalid API response format: 'data' is not a list. Type: {type(api_data['data'])}")
            logger.error(f"Data value: {str(api_data['data'])[:500]}")
            
            # If data is an object with an 'id', try to process it as a single application
            if isinstance(api_data['data'], dict) and 'id' in api_data['data']:
                api_data['data'] = [api_data['data']]
            else:
                return None
        
        # Check if there's any data
        if len(api_data['data']) == 0:
            return None
        
        # Get the first application
        application = api_data['data'][0]
        
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
                
                # Return the application with parsed data and top-level fields preserved
                return {
                    'id': application_id,
                    'data': parsed_data,
                    'billing_info': application.get('billing_info'),
                    'photo_url': application.get('photo_url'),
                    'ai_photo_url': application.get('ai_photo_url')
                }
            else:
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


def update_application_status(application_id, renewal_status, renewal_error=None, renewal_application_id=None):
    """
    Update application status via backend API
    
    Args:
        application_id: The application ID
        renewal_status: "11" for processing started, "2" for error in steps 1-14, "3" for error in step 15, "5" for success
        renewal_error: Dict with code and message (optional, for failures)
        renewal_application_id: The renewal application number from the government website (optional, for success)
        
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
        
        # Add renewal_application_id if provided (for success cases)
        if renewal_application_id:
            request_body["renewal_application_id"] = str(renewal_application_id)
        
        # Make POST request to update status
        response = requests.post(update_endpoint, json=request_body, timeout=10)
        response.raise_for_status()
        
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
    
    # Merge top-level fields (billing_info, photo_url, ai_photo_url, application_id) into data for easier access in steps
    # This ensures all steps receive complete data in a single object
    if 'billing_info' in passport_data:
        data['billing_info'] = passport_data['billing_info']
    
    if 'photo_url' in passport_data:
        data['photo_url'] = passport_data['photo_url']
    
    if 'ai_photo_url' in passport_data:
        data['ai_photo_url'] = passport_data['ai_photo_url']
    
    # Add application_id to data for database updates
    data['application_id'] = application_id
    
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
    renewal_application_id = None
    
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
            
            # Capture renewal_application_id from Step 15 if present
            if step_num == 15 and isinstance(step_result, dict) and 'renewal_application_id' in step_result:
                renewal_application_id = step_result['renewal_application_id']
            
            if not success:
                print(f"❌ Step {step_num} failed: {message}")
                failed_step = step_num
                failed_error = {
                    "code": code,
                    "message": message
                }
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
            
            # Update backend with success status and renewal application ID
            if renewal_application_id:
                print(f"Renewal Application ID: {renewal_application_id}")
                update_application_status(application_id, "5", renewal_application_id=renewal_application_id)
            else:
                update_application_status(application_id, "5")
            
            return {
                'success': True,
                'results': results,
                'renewal_application_id': renewal_application_id
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


def process_application_in_process(passport_data, app_number, props):
    """
    Process a single application in a separate process
    
    Args:
        passport_data: Dictionary containing passport application data
        app_number: Application number for display purposes
        props: Properties for the application (method, error_code)
    """
    process_id = multiprocessing.current_process().name
    print(f"\n🚀 [{process_id}] Process started for application #{app_number}")
    
    # Create automation instance for this process
    automation = UndetectedWebAutomation(headless=False)
    
    try:
        # Target URL
        target_url = "https://opr.travel.state.gov/"
        
        # Setup driver
        print(f"🚀 [{process_id}] Setting up browser...")
        if not automation.setup_driver():
            print(f"❌ [{process_id}] Failed to setup browser")
            return
        
        print(f"✅ [{process_id}] Browser setup successful!")
        time.sleep(1)
        
        # Navigate to the URL
        print(f"🚀 [{process_id}] Navigating to {target_url}...")
        if not automation.navigate_to_url(target_url):
            print(f"❌ [{process_id}] Failed to navigate to {target_url}")
            return
            
        print(f"✅ [{process_id}] Successfully navigated to {target_url}")
        
        # Get page information
        page_info = automation.get_page_info()
        if page_info:
            print(f"📄 [{process_id}] Page Title: {page_info['title']}")
        
        time.sleep(5)
        
        # Handle Cloudflare captcha if present
        print(f"\n🔍 [{process_id}] Checking for Cloudflare captcha...")
        captcha_found = automation.handle_cloudflare_captcha()
        if captcha_found:
            print(f"✅ [{process_id}] Cloudflare captcha was found and clicked")
        else:
            print(f"ℹ️  [{process_id}] No Cloudflare captcha found - proceeding normally")
        
        # Wait 10 seconds after initial navigation
        print(f"\n⏳ [{process_id}] Waiting 10 seconds after initial navigation...")
        time.sleep(10)
        
        # Process the application
        print(f"\n🚀 [{process_id}] Starting application processing...")
        app_results = process_single_application(
            automation.driver, 
            passport_data, 
            app_number - 1,  # 0-based index
            app_number  # Display as total
        )
        
        # Print result
        if app_results.get('success', False):
            print(f"\n✅ [{process_id}] Application #{app_number} completed successfully!")
        else:
            print(f"\n❌ [{process_id}] Application #{app_number} failed")
        
    except Exception as e:
        logger.error(f"[{process_id}] Error in process: {str(e)}")
        print(f"❌ [{process_id}] Error in process: {str(e)}")
    
    finally:
        # Close the browser and cleanup
        print(f"\n🧹 [{process_id}] Closing browser and cleaning up...")
        automation.close_driver()
        print(f"✅ [{process_id}] Process completed and browser closed")


def main():
    """Main function to poll API and create processes for each application"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Undetected ChromeDriver Web Automation with Multiprocessing')
    parser.add_argument(
        '--method',
        type=str,
        choices=['normal', 'failed'],
        default='normal',
        help='Application processing method: normal (default) or failed'
    )
    parser.add_argument(
        '--error-code',
        type=str,
        default=None,
        help='Error code for failed applications (required when method is "failed"), e.g., STEP6_ERROR'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.method == 'failed' and not args.error_code:
        parser.error('--error-code is required when --method is "failed"')
    
    # Prepare props for fetch_single_passport_application
    props = {
        'application_processing_method': args.method
    }
    if args.error_code:
        props['error_code'] = args.error_code
    
    print("Undetected ChromeDriver Web Automation - Multiprocessing Mode")
    print("=" * 70)
    print(f"Processing Method: {args.method}")
    if args.error_code:
        print(f"Error Code: {args.error_code}")
    print("=" * 70)
    print("The system will poll the API every 20 seconds for new applications.")
    print("Each application will be processed in a separate process.")
    print("Maximum concurrent processes: 5")
    print("Press Ctrl+C to stop the automation.\n")
    
    # Track statistics
    total_processed = 0
    active_processes = []
    MAX_PROCESSES = 5  # Maximum number of concurrent processes
    
    try:
        # Main polling loop
        while True:
            try:
                # Clean up finished processes first
                active_processes = [p for p in active_processes if p.is_alive()]
                active_count = len(active_processes)
                
                print("\n" + ">"*70)
                print(f"📡 Checking process status...")
                print(f"📊 Active processes: {active_count}/{MAX_PROCESSES}")
                print(">"*70)
                
                # Check if we've reached the maximum process limit
                if active_count >= MAX_PROCESSES:
                    print(f"⏸️  Maximum processes ({MAX_PROCESSES}) reached. Waiting for a process to complete...")
                    print("⏳ Waiting 20 seconds before next check...")
                    time.sleep(20)
                    continue
                
                # We have available slots - fetch new application
                print(f"✅ Process slot available ({active_count}/{MAX_PROCESSES}). Fetching new application...")
                passport_data = fetch_single_passport_application(props)
                
                if not passport_data:
                    print("⏸️  No application data available from API")
                    print("⏳ Waiting 20 seconds before next check...")
                    time.sleep(20)
                    continue
                
                # Application found - update status immediately to prevent duplicate processing
                application_id = passport_data.get('id', 'Unknown')
                print(f"\n📝 Application {application_id} fetched - Updating status to 11 (Processing Started)...")
                update_success = update_application_status(application_id, "11")
                if update_success:
                    print(f"✅ Application status updated to 11")
                else:
                    print(f"⚠️  Failed to update application status - skipping this application")
                    print("⏳ Waiting 20 seconds before next check...")
                    time.sleep(20)
                    continue
                
                # Create a new process
                total_processed += 1
                process_name = f"App-{total_processed}"
                
                print(f"\n✨ Creating process '{process_name}' for application {application_id}...")
                
                # Create and start the process
                process = multiprocessing.Process(
                    target=process_application_in_process,
                    args=(passport_data, total_processed, props),
                    name=process_name,
                    daemon=True  # Daemon process will exit when main program exits
                )
                process.start()
                active_processes.append(process)
                
                print(f"✅ Process '{process_name}' started for application #{total_processed}")
                print(f"📊 Active processes: {len(active_processes)}/{MAX_PROCESSES}")
                
                # Wait 20 seconds before polling again
                print("⏳ Waiting 20 seconds before next API poll...")
                time.sleep(20)
                
            except KeyboardInterrupt:
                print("\n\n" + "="*70)
                print("⚠️  Keyboard interrupt detected. Stopping automation...")
                print("="*70)
                break
                
            except Exception as e:
                logger.error(f"Error in main polling loop: {str(e)}")
                print(f"❌ Error in main polling loop: {str(e)}")
                print("⏳ Waiting 20 seconds before retry...")
                time.sleep(20)
    
    except Exception as e:
        logger.error(f"Critical error in automation: {str(e)}")
        print(f"❌ Critical error occurred: {str(e)}")
    
    finally:
        # Wait for all active processes to complete
        if active_processes:
            print("\n" + "="*70)
            print(f"⏳ Waiting for {len(active_processes)} active process(es) to complete...")
            print("="*70)
            for process in active_processes:
                if process.is_alive():
                    print(f"⏳ Waiting for process '{process.name}' to complete...")
                    process.join(timeout=300)  # Wait up to 5 minutes per process
        
        # Print final summary
        print("\n" + "="*70)
        print("🏁 FINAL SESSION SUMMARY")
        print("="*70)
        print(f"Total Applications Processed: {total_processed}")
        print("="*70)
        print("\n✅ Automation stopped. All processes have been completed or terminated.")


if __name__ == "__main__":
    # Required for Windows multiprocessing support
    multiprocessing.freeze_support()
    # Set spawn method for better cross-platform compatibility
    # 'spawn' creates a fresh Python interpreter process
    multiprocessing.set_start_method('spawn', force=True)
    main()
