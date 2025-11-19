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
import uuid
import base64
import zipfile
import tempfile
from urllib.parse import urlparse
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
        self.proxy_url = None
        self.proxy_host = None
        self.proxy_port = None
        self.proxy_username = None
        self.proxy_password = None
        self.proxy_extension_path = None
        self.proxy_server = None
        self.load_proxy_config()
    
    def load_proxy_config(self):
        """Load and parse proxy configuration from environment variables"""
        try:
            # Load environment variables
            load_dotenv()
            
            # Method 1: Try to get proxy URL from single environment variable
            self.proxy_url = os.getenv('PROXY_URL')
            
            if self.proxy_url:
                # Parse the proxy URL
                parsed = urlparse(self.proxy_url)
                
                self.proxy_host = parsed.hostname
                self.proxy_port = parsed.port
                self.proxy_username = parsed.username
                self.proxy_password = parsed.password
                
                # Determine the scheme (http, https, socks5, etc.)
                scheme = parsed.scheme if parsed.scheme else 'http'
                
            else:
                # Method 2: Try to get proxy configuration from separate variables
                self.proxy_host = os.getenv('PROXY_HOST')
                self.proxy_port = os.getenv('PROXY_PORT')
                self.proxy_username = os.getenv('PROXY_USERNAME')
                self.proxy_password = os.getenv('PROXY_PASSWORD')
                
                if self.proxy_host and self.proxy_port:
                    # Convert port to integer
                    try:
                        self.proxy_port = int(self.proxy_port)
                    except ValueError:
                        logger.error(f"Invalid PROXY_PORT value: {self.proxy_port}")
                        self.proxy_host = None
                        return
                    
                    # Build proxy_url for compatibility
                    scheme = 'http'  # Default to http
                    if self.proxy_username and self.proxy_password:
                        self.proxy_url = f"{scheme}://{self.proxy_username}:{self.proxy_password}@{self.proxy_host}:{self.proxy_port}"
                    else:
                        self.proxy_url = f"{scheme}://{self.proxy_host}:{self.proxy_port}"
                
        except Exception as e:
            logger.error(f"Error loading proxy configuration: {str(e)}")
            self.proxy_url = None
            self.proxy_host = None
    
    def start_local_proxy_server(self):
        """Start local proxy server for authentication"""
        try:
            from proxy_server import ProxyServer
            
            self.proxy_server = ProxyServer(local_host='127.0.0.1', local_port=8888)
            self.proxy_server.start()
            
            # Wait a moment for server to start
            time.sleep(1)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to start local proxy server: {str(e)}")
            return False
    
    def stop_local_proxy_server(self):
        """Stop local proxy server"""
        if self.proxy_server:
            try:
                self.proxy_server.stop()
                self.proxy_server = None
            except Exception as e:
                pass
    
    def create_proxy_extension(self):
        """
        Create a Chrome extension for proxy authentication
        Returns the path to the extension ZIP file
        """
        try:
            if not self.proxy_username or not self.proxy_password:
                return None
            
            # Create a temporary directory for the extension files
            extension_dir = tempfile.mkdtemp(prefix='proxy_ext_')
            
            # Create manifest.json (using manifest v2 for compatibility)
            manifest_json = {
                "version": "1.0.0",
                "manifest_version": 2,
                "name": "Chrome Proxy Auth",
                "permissions": [
                    "webRequest",
                    "webRequestBlocking",
                    "<all_urls>",
                    "proxy",
                    "tabs",
                    "storage"
                ],
                "background": {
                    "scripts": ["background.js"],
                    "persistent": True
                },
                "minimum_chrome_version": "22.0.0"
            }
            
            # Create background.js with proxy authentication
            # Escape special characters in credentials
            username = self.proxy_username.replace('\\', '\\\\').replace('"', '\\"')
            password = self.proxy_password.replace('\\', '\\\\').replace('"', '\\"')
            
            background_js = f"""
// Proxy authentication extension
console.log('='.repeat(50));
console.log('Proxy Auth Extension Starting...');
console.log('Target: {self.proxy_host}:{self.proxy_port}');
console.log('Username: {username}');
console.log('='.repeat(50));

// Authentication credentials
var credentials = {{
    username: "{username}",
    password: "{password}"
}};

// Handle authentication requests
function handleAuthRequest(details) {{
    console.log('🔐 Authentication requested!');
    console.log('   URL:', details.url);
    console.log('   Challenger:', details.challenger);
    console.log('   isProxy:', details.isProxy);
    console.log('   Providing credentials...');
    
    return {{
        authCredentials: credentials
    }};
}}

// Register the authentication handler
chrome.webRequest.onAuthRequired.addListener(
    handleAuthRequest,
    {{urls: ["<all_urls>"]}},
    ['blocking']
);

console.log('✅ Proxy authentication handler registered');
console.log('   Listening for auth requests on all URLs');
console.log('='.repeat(50));
"""
            
            # Write manifest.json
            manifest_path = os.path.join(extension_dir, 'manifest.json')
            with open(manifest_path, 'w', encoding='utf-8') as f:
                json.dump(manifest_json, f, indent=2)
            
            # Write background.js
            background_path = os.path.join(extension_dir, 'background.js')
            with open(background_path, 'w', encoding='utf-8') as f:
                f.write(background_js)
            
            return extension_dir
            
        except Exception as e:
            logger.error(f"Error creating proxy extension: {str(e)}")
            return None
    
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
        
        # Add proxy configuration if available
        if self.proxy_host and self.proxy_port:
            if self.proxy_username and self.proxy_password:
                # Authenticated proxy - use local proxy server (no auth popup)
                options.add_argument("--proxy-server=http://127.0.0.1:8888")
            else:
                # Non-authenticated proxy - direct connection
                proxy_server = f"http://{self.proxy_host}:{self.proxy_port}"
                options.add_argument(f"--proxy-server={proxy_server}")
        
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
        """
        Setup undetected Chrome WebDriver with auto-downloaded ChromeDriver
        """
        try:
            # Start local proxy server if authenticated proxy is configured
            if self.proxy_host and self.proxy_username and self.proxy_password:
                if not self.start_local_proxy_server():
                    logger.error("Failed to start local proxy server")
                    return False
            
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
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            
            # Wait a moment for page to fully load
            time.sleep(2)
            
            # Look for main-wrapper element that contains the Cloudflare captcha
            main_wrapper = None
            max_attempts = 6  # Check every 2 seconds for up to 12 seconds
            check_interval = 2
            
            for attempt in range(max_attempts):
                if attempt > 0:
                    time.sleep(check_interval)
                
                try:
                    # Try to find main-wrapper element
                    main_wrappers = self.driver.find_elements(By.CSS_SELECTOR, "div.main-wrapper[role='main']")
                    if not main_wrappers:
                        # Also try without role='main' attribute
                        main_wrappers = self.driver.find_elements(By.CSS_SELECTOR, "div.main-wrapper")
                    
                    if main_wrappers:
                        for wrapper in main_wrappers:
                            try:
                                if wrapper.is_displayed():
                                    main_wrapper = wrapper
                                    break
                            except Exception as e:
                                continue
                        
                        if main_wrapper:
                            break
                except Exception as e:
                    continue
            
            if not main_wrapper:
                return False
            
            # Click the main-wrapper element
            try:
                # Scroll into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", main_wrapper)
                time.sleep(1)
                
                # Try multiple click methods
                clicked = False
                
                # Method 1: Regular click
                try:
                    main_wrapper.click()
                    clicked = True
                except Exception as click_error:
                    # Method 2: JavaScript click
                    try:
                        self.driver.execute_script("arguments[0].click();", main_wrapper)
                        clicked = True
                    except Exception as js_error:
                        # Method 3: ActionChains click
                        try:
                            from selenium.webdriver.common.action_chains import ActionChains
                            actions = ActionChains(self.driver)
                            actions.move_to_element(main_wrapper).click().perform()
                            clicked = True
                        except Exception as ac_error:
                            # Method 4: Click using coordinates
                            try:
                                from selenium.webdriver.common.action_chains import ActionChains
                                actions = ActionChains(self.driver)
                                actions.move_to_element_with_offset(main_wrapper, 0, 0).click().perform()
                                clicked = True
                            except Exception as coord_error:
                                # Method 5: Try JavaScript click with MouseEvent
                                try:
                                    self.driver.execute_script("""
                                        var element = arguments[0];
                                        var rect = element.getBoundingClientRect();
                                        var x = rect.left + rect.width / 2;
                                        var y = rect.top + rect.height / 2;
                                        var clickEvent = new MouseEvent('click', {
                                            view: window,
                                            bubbles: true,
                                            cancelable: true,
                                            clientX: x,
                                            clientY: y
                                        });
                                        element.dispatchEvent(clickEvent);
                                    """, main_wrapper)
                                    clicked = True
                                except Exception as js_coord_error:
                                    pass
                
                if clicked:
                    # Wait for captcha to complete
                    time.sleep(5)
                    return True
                else:
                    return False
                    
            except Exception as e:
                return False
                
        except Exception as e:
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return False
    
    def clear_browser_cache(self):
        """
        Clear browser cache, cookies, and storage after each application
        
        This includes:
        - Cookies
        - Local storage
        - Session storage
        - Cache storage
        """
        try:
            if not self.driver:
                return False
            
            # Clear cookies
            try:
                self.driver.delete_all_cookies()
            except Exception as e:
                pass
            
            # Clear local storage, session storage, and cache via JavaScript
            try:
                self.driver.execute_script("""
                    try {
                        localStorage.clear();
                    } catch(e) {}
                    
                    try {
                        sessionStorage.clear();
                    } catch(e) {}
                    
                    try {
                        if ('caches' in window) {
                            caches.keys().then(function(names) {
                                for (let name of names) {
                                    caches.delete(name);
                                }
                            });
                        }
                    } catch(e) {}
                    
                    try {
                        if ('indexedDB' in window) {
                            indexedDB.databases().then(databases => {
                                databases.forEach(db => {
                                    indexedDB.deleteDatabase(db.name);
                                });
                            });
                        }
                    } catch(e) {}
                """)
            except Exception as e:
                pass
            
            return True
            
        except Exception as e:
            logger.error(f"Error clearing browser cache: {str(e)}")
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
            
            # Stop local proxy server if running
            self.stop_local_proxy_server()
    


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
        renewal_status: "2" for error in steps 1-14, "3" for error in step 15, "5" for success
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


def main():
    """Main function to run the undetected automation in continuous loop"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Undetected ChromeDriver Web Automation')
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
    
    print("Undetected ChromeDriver Web Automation - Continuous Mode")
    print("=" * 50)
    print(f"Processing Method: {args.method}")
    if args.error_code:
        print(f"Error Code: {args.error_code}")
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
        print("Waiting 1 seconds before navigation...")
        time.sleep(1)
        
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

        time.sleep(5)
        # Handle Cloudflare captcha if present
        print("\nChecking for Cloudflare captcha...")
        captcha_found = automation.handle_cloudflare_captcha()
        if captcha_found:
            print("✅ Cloudflare captcha was found and clicked")
        else:
            print("ℹ️  No Cloudflare captcha found - proceeding normally")
        
        # Wait 15 seconds after initial navigation
        print("\nWaiting 15 seconds after initial navigation...")
        time.sleep(10)
        
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
                passport_data = fetch_single_passport_application(props)
                
                if not passport_data:
                    print("⏸️  No application data available from API")
                    print("⏳ Waiting 20 seconds before next check...")
                    time.sleep(20)
                    
                    # Check for captcha during idle period
                    print("\nChecking for Cloudflare captcha during idle period...")
                    captcha_found = automation.handle_cloudflare_captcha()
                    if captcha_found:
                        print("✅ Cloudflare captcha was found and clicked during idle period")
                    
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
                
                # Close and restart browser for next application (to apply fresh proxy settings)
                print("\n" + ">"*50)
                print("🔄 Restarting browser for next application...")
                print(">"*50)
                
                automation.close_driver()
                time.sleep(2)
                
                # Setup driver again with fresh proxy settings
                if not automation.setup_driver():
                    print("❌ Failed to restart browser")
                    print("⏳ Waiting 30 seconds before retry...")
                    time.sleep(30)
                    continue
                
                print("✅ Browser restarted successfully")
                
                # Navigate to the start URL
                automation.navigate_to_url(target_url)
                time.sleep(5)
                
                # Handle Cloudflare captcha if present
                print("\nChecking for Cloudflare captcha...")
                captcha_found = automation.handle_cloudflare_captcha()
                if captcha_found:
                    print("✅ Cloudflare captcha was found and clicked")
                else:
                    print("ℹ️  No Cloudflare captcha found - proceeding normally")
                
                time.sleep(5)
                
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
                    # Handle Cloudflare captcha if present
                    automation.handle_cloudflare_captcha()
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


if __name__ == "__main__":
    main()
