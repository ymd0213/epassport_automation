"""
Page Detector Module
Dynamically detects which page is currently loaded and maps it to the appropriate step
"""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


class PageDetector:
    """Detects which page is currently loaded based on unique page elements"""
    
    def __init__(self, driver, timeout=10):
        """
        Initialize PageDetector
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Maximum time to wait for page detection
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        
        # Page detection rules - each page has unique identifiers
        # Format: page_key -> list of detection criteria
        self.page_identifiers = {
            'step1_landing': [
                {'type': 'css', 'selector': 'button[aria-label="Start passport renewal application"]'},
                {'type': 'text_in_page', 'text': 'Renew a U.S. Passport Online'}
            ],
            'step2_what_you_need': [
                {'type': 'css', 'selector': 'input[id="renewBook-yes-radio"]'},
                {'type': 'text_in_page', 'text': 'What you need'}
            ],
            'step3_eligibility': [
                {'type': 'css', 'selector': 'input[id="eligible-yes-radio"]'},
                {'type': 'text_in_page', 'text': 'eligibility requirements'}
            ],
            'step4_upcoming_travel': [
                {'type': 'css', 'selector': 'input[id="upcomingTravel-yes-radio"]'},
                {'type': 'text_in_page', 'text': 'upcoming international travel'}
            ],
            'step5_terms': [
                {'type': 'css', 'selector': 'input[id="termsAgreement-checkbox"]'},
                {'type': 'text_in_page', 'text': 'Terms and conditions'}
            ],
            'step6_renewing': [
                {'type': 'css', 'selector': 'input[id="passportBookId"]'},
                {'type': 'css', 'selector': 'input[id="renewBook-yes-radio"]'},
                {'type': 'text_in_page', 'text': 'What are you renewing'}
            ],
            'step7_photo': [
                {'type': 'css', 'selector': 'input[id="passportPhoto"]'},
                {'type': 'text_in_page', 'text': 'Upload your passport photo'}
            ],
            'step8_personal_info': [
                {'type': 'css', 'selector': 'input[id="firstName"]'},
                {'type': 'css', 'selector': 'input[id="middleName"]'},
                {'type': 'css', 'selector': 'select[id="sex"]'},
                {'type': 'text_in_page', 'text': 'Personal information'}
            ],
            'step9_emergency_contact': [
                {'type': 'css', 'selector': 'input[id="emergencyContactName"]'},
                {'type': 'text_in_page', 'text': 'Emergency contact'}
            ],
            'step10_passport_options': [
                {'type': 'css', 'selector': 'input[id="passportBook-yes-radio"]'},
                {'type': 'css', 'selector': 'input[id="passportCard-yes-radio"]'},
                {'type': 'text_in_page', 'text': 'passport options'}
            ],
            'step11_mailing_address': [
                {'type': 'css', 'selector': 'input[id="mailingAddress1"]'},
                {'type': 'css', 'selector': 'input[id="mailingCity"]'},
                {'type': 'text_in_page', 'text': 'Mailing address'}
            ],
            'step12_delivery': [
                {'type': 'css', 'selector': 'input[id="deliverySpeed-routine-radio"]'},
                {'type': 'text_in_page', 'text': 'delivery speed'}
            ],
            'step13_review': [
                {'type': 'text_in_page', 'text': 'Review your order'},
                {'type': 'css', 'selector': 'button[type="submit"]'}
            ],
            'step14_statement': [
                {'type': 'css', 'selector': 'input[id="statementOfTruth-checkbox"]'},
                {'type': 'text_in_page', 'text': 'Statement of truth'}
            ],
            'step15_payment': [
                {'type': 'css', 'selector': 'input[id="cardNumber"]'},
                {'type': 'text_in_page', 'text': 'Payment information'}
            ],
            'confirmation': [
                {'type': 'text_in_page', 'text': 'Application submitted'},
                {'type': 'text_in_page', 'text': 'confirmation'}
            ]
        }
    
    def detect_current_page(self, max_wait_time=30):
        """
        Detect which page is currently loaded
        
        Args:
            max_wait_time: Maximum time to wait for a recognizable page
            
        Returns:
            str: Page key if detected, None if no page matched
        """
        logger.info("🔍 Detecting current page...")
        
        import time
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            # Wait for page to be in ready state
            try:
                self.driver.execute_script("return document.readyState") == "complete"
            except:
                pass
            
            # Try to match each page
            for page_key, identifiers in self.page_identifiers.items():
                if self._check_page_match(page_key, identifiers):
                    logger.info(f"✅ Detected page: {page_key}")
                    return page_key
            
            # Wait a bit before trying again
            time.sleep(1)
        
        logger.warning(f"⚠️  Could not detect page after {max_wait_time} seconds")
        current_url = self.driver.current_url
        logger.warning(f"Current URL: {current_url}")
        return None
    
    def _check_page_match(self, page_key, identifiers):
        """
        Check if current page matches the given identifiers
        
        Args:
            page_key: Key identifying the page
            identifiers: List of identifier dictionaries
            
        Returns:
            bool: True if page matches all identifiers
        """
        try:
            matches = 0
            required_matches = min(2, len(identifiers))  # Need at least 2 matches or all if less than 2
            
            for identifier in identifiers:
                if identifier['type'] == 'css':
                    try:
                        element = self.driver.find_element(By.CSS_SELECTOR, identifier['selector'])
                        if element:
                            matches += 1
                    except:
                        pass
                
                elif identifier['type'] == 'xpath':
                    try:
                        element = self.driver.find_element(By.XPATH, identifier['selector'])
                        if element:
                            matches += 1
                    except:
                        pass
                
                elif identifier['type'] == 'text_in_page':
                    try:
                        page_source = self.driver.page_source.lower()
                        if identifier['text'].lower() in page_source:
                            matches += 1
                    except:
                        pass
                
                # If we have enough matches, return True early
                if matches >= required_matches:
                    return True
            
            return matches >= required_matches
            
        except Exception as e:
            logger.debug(f"Error checking page match for {page_key}: {e}")
            return False
    
    def wait_for_page_change(self, current_page_key, timeout=30):
        """
        Wait for the page to change from the current page
        
        Args:
            current_page_key: The current page key
            timeout: Maximum time to wait for page change
            
        Returns:
            str: New page key if detected, None if timeout
        """
        logger.info(f"⏳ Waiting for page to change from {current_page_key}...")
        
        import time
        start_time = time.time()
        
        # Wait a moment for navigation to start
        time.sleep(1)
        
        while time.time() - start_time < timeout:
            detected_page = self.detect_current_page(max_wait_time=5)
            
            if detected_page and detected_page != current_page_key:
                logger.info(f"✅ Page changed to: {detected_page}")
                return detected_page
            
            # Check if we're still on the same page or detecting
            if detected_page == current_page_key:
                time.sleep(2)
                continue
            
            time.sleep(1)
        
        logger.warning(f"⚠️  Page did not change from {current_page_key} within {timeout} seconds")
        return None
