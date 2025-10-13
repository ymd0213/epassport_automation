"""
Complete Web Automation Script for OPR Website
Automates interactions with https://opr.travel.state.gov/ and other websites
Includes ChromeDriver fixes and comprehensive error handling
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import logging
import os
import platform
import json
import random
from selenium_stealth import stealth

# Configure simple logging
logging.basicConfig(level=logging.WARNING, format='%(message)s')
logger = logging.getLogger(__name__)


class WebAutomation:
    def __init__(self, headless=False, wait_timeout=10):
        """
        Initialize the WebAutomation class
        
        Args:
            headless (bool): Run browser in headless mode
            wait_timeout (int): Default timeout for element waits
        """
        self.driver = None
        self.wait_timeout = wait_timeout
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
    
    def find_chromedriver(self):
        """Find ChromeDriver in common locations"""
        possible_paths = [
            "chromedriver.exe",
            "chromedriver",
            "./chromedriver.exe",
            "./chromedriver",
            "C:/chromedriver.exe",
            "C:/chromedriver"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None
    
    def setup_driver(self):
        """Setup Chrome WebDriver with multiple fallback options"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            # Chrome options for anti-detection and stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-logging")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--silent")
            chrome_options.add_argument("--disable-infobars")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--start-maximized")
            
            # Anti-detection: Remove automation flags
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("detach", True)
            
            # Set realistic user agent
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Additional preferences to avoid detection
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Try multiple approaches to setup ChromeDriver
            success = False
            
            # Method 1: Try using system PATH ChromeDriver
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                success = True
            except Exception as e1:
                # Method 2: Try webdriver-manager with specific version
                try:
                    from webdriver_manager.chrome import ChromeDriverManager
                    
                    # Get Chrome version and try to match ChromeDriver
                    chrome_version = self.get_chrome_version()
                    if chrome_version:
                        service = Service(ChromeDriverManager(version=chrome_version).install())
                    else:
                        service = Service(ChromeDriverManager().install())
                    
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    success = True
                    
                except Exception as e2:
                    # Method 3: Try manual ChromeDriver path
                    try:
                        chromedriver_path = self.find_chromedriver()
                        if chromedriver_path:
                            service = Service(chromedriver_path)
                            self.driver = webdriver.Chrome(service=service, options=chrome_options)
                            success = True
                    except Exception as e3:
                        pass
            
            if not success:
                raise Exception("All ChromeDriver setup methods failed")
            
            # Apply stealth mode to avoid detection
            stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
            )
            
            # Additional anti-detection scripts
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                    window.chrome = {runtime: {}};
                """
            })
            
            self.driver.implicitly_wait(self.wait_timeout)
            
            return True
            
        except Exception as e:
            return False
    
    def navigate_to_url(self, url):
        """Navigate to a specific URL"""
        try:
            self.driver.get(url)
            return True
        except Exception as e:
            return False
    
    def find_element(self, locator_type, locator_value, timeout=None):
        """Find an element on the page"""
        try:
            timeout = timeout or self.wait_timeout
            wait = WebDriverWait(self.driver, timeout)
            
            locator_map = {
                'id': By.ID,
                'name': By.NAME,
                'class_name': By.CLASS_NAME,
                'xpath': By.XPATH,
                'css_selector': By.CSS_SELECTOR,
                'tag_name': By.TAG_NAME,
                'link_text': By.LINK_TEXT,
                'partial_link_text': By.PARTIAL_LINK_TEXT
            }
            
            locator = locator_map.get(locator_type.lower())
            if not locator:
                raise ValueError(f"Invalid locator type: {locator_type}")
            
            element = wait.until(EC.presence_of_element_located((locator, locator_value)))
            return element
            
        except Exception as e:
            return None
    
    def click_element(self, locator_type, locator_value, timeout=None):
        """
        Click an element
        
        Args:
            locator_type (str): Type of locator
            locator_value (str): Value of the locator
            timeout (int): Custom timeout for this operation
        """
        try:
            element = self.find_element(locator_type, locator_value, timeout)
            if element:
                element.click()
                logger.info(f"Clicked element: {locator_type}='{locator_value}'")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to click element: {str(e)}")
            return False
    
    def input_text(self, locator_type, locator_value, text, clear_first=True, timeout=None):
        """
        Input text into an element
        
        Args:
            locator_type (str): Type of locator
            locator_value (str): Value of the locator
            text (str): Text to input
            clear_first (bool): Clear the field before inputting text
            timeout (int): Custom timeout for this operation
        """
        try:
            element = self.find_element(locator_type, locator_value, timeout)
            if element:
                if clear_first:
                    element.clear()
                element.send_keys(text)
                logger.info(f"Input text '{text}' into element: {locator_type}='{locator_value}'")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to input text: {str(e)}")
            return False
    
    def wait_for_element_visible(self, locator_type, locator_value, timeout=None):
        """
        Wait for an element to be visible
        
        Args:
            locator_type (str): Type of locator
            locator_value (str): Value of the locator
            timeout (int): Custom timeout for this operation
        """
        try:
            timeout = timeout or self.wait_timeout
            wait = WebDriverWait(self.driver, timeout)
            
            locator_map = {
                'id': By.ID,
                'name': By.NAME,
                'class_name': By.CLASS_NAME,
                'xpath': By.XPATH,
                'css_selector': By.CSS_SELECTOR
            }
            
            locator = locator_map.get(locator_type.lower())
            if not locator:
                raise ValueError(f"Invalid locator type: {locator_type}")
            
            element = wait.until(EC.visibility_of_element_located((locator, locator_value)))
            logger.info(f"Element is visible: {locator_type}='{locator_value}'")
            return element
            
        except Exception as e:
            logger.error(f"Element not visible: {locator_type}='{locator_value}' - {str(e)}")
            return None
    
    def get_page_title(self):
        """Get the current page title"""
        try:
            title = self.driver.title
            logger.info(f"Page title: {title}")
            return title
        except Exception as e:
            logger.error(f"Failed to get page title: {str(e)}")
            return None
    
    
    def close_driver(self):
        """Close the WebDriver"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("WebDriver closed successfully")
        except Exception as e:
            logger.error(f"Error closing WebDriver: {str(e)}")


    def access_opr_website(self):
        """Navigate to the OPR website"""
        try:
            logger.info("Accessing OPR website...")
            success = self.navigate_to_url("https://opr.travel.state.gov/")
            if success:
                # Wait for page to load completely
                time.sleep(3)
                logger.info("Successfully accessed OPR website")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to access OPR website: {str(e)}")
            return False
    
    def wait_for_page_load(self):
        """Wait 90 seconds for page to fully load"""
        try:
            # Wait 60 seconds
            logger.info("Waiting 60 seconds for page to fully load...")
            time.sleep(60)
            
            logger.info("60-second wait completed")
            
            return True
            
        except Exception as e:
            logger.error(f"Error waiting for page load: {str(e)}")
            return False
    
    def find_and_click_get_started_retry(self):
        """Try to find and click the 'Get Started' button 3 times with 30-second intervals"""
        try:
            # Look for the specific "Get Started" button
            get_started_selectors = [
                ("xpath", "//button[@type='button' and @class='usa-button padding-y-2' and @data-testid='button' and @aria-label='Start passport renewal application']"),
                ("xpath", "//button[contains(@class, 'usa-button') and contains(@class, 'padding-y-2') and @data-testid='button']"),
                ("xpath", "//button[@data-testid='button' and contains(text(), 'Get Started')]"),
                ("xpath", "//button[contains(@aria-label, 'Start passport renewal')]"),
                ("xpath", "//button[contains(text(), 'Get Started')]"),
                ("xpath", "//button[@class='usa-button padding-y-2']"),
                ("xpath", "//button[@data-testid='button']")
            ]
            
            # Try 3 times with 30-second intervals
            for attempt in range(1, 4):
                logger.info(f"Attempt {attempt}/3: Looking for 'Get Started' button...")
                
                for locator_type, locator_value in get_started_selectors:
                    try:
                        logger.info(f"Trying to find button with: {locator_value}")
                        if self.click_element(locator_type, locator_value, timeout=5):
                            logger.info(f"Successfully clicked 'Get Started' button using: {locator_value}")
                            time.sleep(5)
                            return True
                    except Exception as e:
                        logger.warning(f"Failed to click with selector {locator_value}: {str(e)}")
                        continue
                
                # If not found in this attempt and not the last attempt, wait 30 seconds
                if attempt < 3:
                    logger.info(f"Button not found in attempt {attempt}. Waiting 30 seconds before next attempt...")
                    time.sleep(30)
            
            logger.warning("Could not find or click the 'Get Started' button after 3 attempts")
            return False
            
        except Exception as e:
            logger.error(f"Error in find_and_click_get_started_retry: {str(e)}")
            return False
    
    def find_and_click_continue_button(self):
        """Find and click the 'Continue' button in what you need page"""
        try:
            logger.info("Looking for 'Continue' button in what you need page...")
            
            # Look for the specific "Continue" button
            continue_selectors = [
                ("xpath", "//button[@type='button' and @class='usa-button padding-y-2' and @data-testid='button' and contains(text(), 'Continue')]"),
                ("xpath", "//button[contains(@class, 'usa-button') and contains(@class, 'padding-y-2') and @data-testid='button' and contains(text(), 'Continue')]"),
                ("xpath", "//button[@data-testid='button' and contains(text(), 'Continue')]"),
                ("xpath", "//button[contains(text(), 'Continue')]"),
                ("xpath", "//button[@class='usa-button padding-y-2']")
            ]
            
            for locator_type, locator_value in continue_selectors:
                try:
                    logger.info(f"Trying to find Continue button with: {locator_value}")
                    if self.click_element(locator_type, locator_value, timeout=5):
                        logger.info(f"Successfully clicked 'Continue' button in what you need page using: {locator_value}")
                        time.sleep(5)
                        return True
                except Exception as e:
                    logger.warning(f"Failed to click Continue button with selector {locator_value}: {str(e)}")
                    continue
            
            logger.warning("Could not find or click the 'Continue' button in what you need page")
            return False
            
        except Exception as e:
            logger.error(f"Error in find_and_click_continue_button: {str(e)}")
            return False
    
    def find_and_click_continue_eligibility(self):
        """Find and click the 'Continue' button in eligibility requirements page"""
        try:
            logger.info("Looking for 'Continue' button in eligibility requirements page...")
            
            # Look for the specific "Continue" button on eligibility page
            continue_selectors = [
                ("xpath", "//button[@type='button' and @class='usa-button padding-y-2' and @data-testid='button' and contains(text(), 'Continue')]"),
                ("xpath", "//button[contains(@class, 'usa-button') and contains(@class, 'padding-y-2') and @data-testid='button' and contains(text(), 'Continue')]"),
                ("xpath", "//button[@data-testid='button' and contains(text(), 'Continue')]"),
                ("xpath", "//button[contains(text(), 'Continue')]"),
                ("xpath", "//button[@class='usa-button padding-y-2']")
            ]
            
            for locator_type, locator_value in continue_selectors:
                try:
                    logger.info(f"Trying to find Continue button in eligibility page with: {locator_value}")
                    if self.click_element(locator_type, locator_value, timeout=5):
                        logger.info(f"Successfully clicked 'Continue' button in eligibility requirements page using: {locator_value}")
                        time.sleep(5)
                        return True
                except Exception as e:
                    logger.warning(f"Failed to click Continue button in eligibility page with selector {locator_value}: {str(e)}")
                    continue
            
            logger.warning("Could not find or click the 'Continue' button in eligibility requirements page")
            return False
            
        except Exception as e:
            logger.error(f"Error in find_and_click_continue_eligibility: {str(e)}")
            return False
    
    
    
    
    def fill_form_field(self, field_name, value, passport_data=None):
        """
        Fill a specific form field using multiple locator strategies
        
        Args:
            field_name (str): Name of the field to fill
            value (str): Value to input (if None, will try to get from passport_data)
            passport_data (dict): Passport data dictionary (optional)
        """
        try:
            # If no value provided, try to get from passport_data
            if value is None and passport_data:
                value = passport_data.get(field_name, '')
            
            if not value:
                logger.warning(f"No value provided for field: {field_name}")
                return False
            
            # Common field name variations
            field_variations = [
                field_name,
                field_name.replace('_', ''),
                field_name.replace('_', '-'),
                field_name.replace('_', ' '),
                field_name.lower(),
                field_name.upper()
            ]
            
            # Try different locator strategies
            for variation in field_variations:
                # Try by name attribute
                if self.input_text("name", variation, str(value)):
                    logger.info(f"Filled {field_name} using name='{variation}' with value='{value}'")
                    time.sleep(5)
                    return True
                
                # Try by id attribute
                if self.input_text("id", variation, str(value)):
                    logger.info(f"Filled {field_name} using id='{variation}' with value='{value}'")
                    time.sleep(5)
                    return True
                
                # Try by placeholder
                if self.input_text("xpath", f"//input[@placeholder='{variation}']", str(value)):
                    logger.info(f"Filled {field_name} using placeholder='{variation}' with value='{value}'")
                    time.sleep(5)
                    return True
            
            logger.warning(f"Could not find field: {field_name}")
            return False
            
        except Exception as e:
            logger.error(f"Error filling field {field_name}: {str(e)}")
            return False
    


def load_passport_data():
    """Load passport data from JSON file"""
    try:
        with open('passport_data.json', 'r') as file:
            data = json.load(file)
            logger.info("Passport data loaded successfully from JSON file")
            return data
    except Exception as e:
        logger.error(f"Error loading passport data: {str(e)}")
        return None

# ============================================================================
# STEP 1: INITIAL SETUP AND WEBSITE ACCESS
# ============================================================================

def step1_initial_setup():
    """Step 1: Setup WebDriver, wait 60 seconds, then access OPR website"""
    automation = WebAutomation(headless=False, wait_timeout=15)
    
    print("=== STEP 1: INITIAL SETUP ===")
    print("Setting up WebDriver...")
    if not automation.setup_driver():
        print("Failed to setup WebDriver")
        return None
    
    print("Waiting 60 seconds after browser opens...")
    time.sleep(60)
    print("60-second wait completed")
    
    print("Accessing OPR website...")
    if not automation.access_opr_website():
        print("Failed to access OPR website")
        return None
    
    title = automation.get_page_title()
    print(f"Page title: {title}")
    
    return automation

# ============================================================================
# STEP 2: WAIT FOR PAGE LOAD
# ============================================================================

def step2_wait_for_page_load(automation):
    """Step 2: Wait 60 seconds for page to fully load"""
    print("\n=== STEP 2: WAITING FOR PAGE LOAD ===")
    print("Waiting 60 seconds for page to load...")
    
    if not automation.wait_for_page_load():
        print("Failed to wait for page load")
        return False
    
    return True

# ============================================================================
# STEP 3: GET STARTED BUTTON
# ============================================================================

def step3_click_get_started(automation):
    """Step 3: Find and click 'Get Started' button (3 attempts)"""
    print("\n=== STEP 3: GET STARTED BUTTON ===")
    print("Looking for 'Get Started' button (3 attempts with 30-second intervals)...")
    
    if automation.find_and_click_get_started_retry():
        print("Successfully clicked 'Get Started' button!")
        return True
    else:
        print("Could not find or click the 'Get Started' button after 3 attempts")
        return False

# ============================================================================
# STEP 4: WHAT YOU NEED PAGE
# ============================================================================

def step4_what_you_need_page(automation):
    """Step 4: Click Continue button on 'What You Need' page"""
    print("\n=== STEP 4: WHAT YOU NEED PAGE ===")
    print("Looking for 'Continue' button in what you need page")
    
    if automation.find_and_click_continue_button():
        print("Successfully clicked 'Continue' button!")
        return True
    else:
        print("Could not find or click the 'Continue' button")
        return False

# ============================================================================
# STEP 5: ELIGIBILITY REQUIREMENTS PAGE
# ============================================================================

def step5_eligibility_requirements_page(automation):
    """Step 5: Click Continue button on 'Eligibility Requirements' page"""
    print("\n=== STEP 5: ELIGIBILITY REQUIREMENTS PAGE ===")
    print("Looking for 'Continue' button in eligibility requirements page")
    
    if automation.find_and_click_continue_eligibility():
        print("Successfully clicked 'Continue' button in eligibility page!")
        return True
    else:
        print("Could not find or click the 'Continue' button in eligibility page")
        return False

# ============================================================================
# STEP 6: FORM FILLING READY
# ============================================================================

def step6_form_filling_ready(automation, passport_data):
    """Step 6: Ready for multi-page form filling"""
    print("\n=== STEP 6: FORM FILLING READY ===")
    print("Passport data loaded and ready for multi-page form filling!")
    print("\nAvailable data fields:")
    print(f"- Name: {passport_data.get('first_name')} {passport_data.get('last_name')}")
    print(f"- Email: {passport_data.get('email')}")
    print(f"- Phone: {passport_data.get('phone_number')}")
    print(f"- Address: {passport_data.get('mailing_address_1')}")
    print(f"- Birth: {passport_data.get('month_of_birth')}/{passport_data.get('day_of_birth')}/{passport_data.get('year_of_birth')}")
    print(f"- SSN: {passport_data.get('ssn_1')}-{passport_data.get('ssn_2')}-{passport_data.get('ssn_3')}")
    
    print("\nTo fill forms on each page, use:")
    print("automation.fill_form_field('field_name', None, passport_data)")
    print("\nExample fields: first_name, last_name, email, phone_number, etc.")

# ============================================================================
# MAIN AUTOMATION FUNCTION
# ============================================================================

def run_opr_automation():
    """Complete OPR automation - organized by clear steps"""
    
    # Load passport data
    passport_data = load_passport_data()
    if not passport_data:
        print("Failed to load passport data from JSON file")
        return
    
    try:
        # Step 1: Initial setup
        automation = step1_initial_setup()
        if not automation:
            return
        
        # Step 2: Wait for page load
        if not step2_wait_for_page_load(automation):
            return
        
        # Step 3: Click Get Started button
        step3_click_get_started(automation)
        
        # Step 4: What You Need page
        step4_what_you_need_page(automation)
        
        # Step 5: Eligibility Requirements page
        step5_eligibility_requirements_page(automation)
        
        # Step 6: Ready for form filling
        step6_form_filling_ready(automation, passport_data)
        
        print("\n=== AUTOMATION COMPLETED ===")
        print("Browser will remain open for you to continue manually...")
        
    except Exception as e:
        logger.error(f"Error in OPR automation: {str(e)}")
        print("Browser will remain open for debugging...")


if __name__ == "__main__":
    print("OPR Web Automation Script")
    print("=" * 40)
    print("Starting automation...")
    print()
    
    run_opr_automation()
