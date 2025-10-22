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
from steps.step1 import Step1LandingPage
from steps.step2 import Step2WhatYouNeed
from steps.step3 import Step3EligibilityRequirements
from steps.step4 import Step4WhyAreWeAskingForThis
from steps.step5 import Step5TermsAndConditions
from steps.step6 import Step6WhatAreYouRenewing
from steps.step7 import Step7PassportPhoto
from steps.step8 import Step8PersonalInformation
from steps.step9 import Step9EmergencyContact
from steps.step10 import Step10PassportOptions
from steps.step11 import Step11MailingAddress
from steps.step12 import Step12PassportDelivery
from steps.step13 import Step13ReviewOrder
from steps.step14 import Step14StatementOfTruth

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
    """Load passport data from JSON file"""
    try:
        with open('passport_data.json', 'r') as file:
            data = json.load(file)
            logger.info(f"Loaded {len(data)} passport applications from JSON file")
            return data
    except Exception as e:
        logger.error(f"Failed to load passport data: {str(e)}")
        return []

def main():
    """Main function to run the undetected automation"""
    print("Undetected ChromeDriver Web Automation")
    print("=" * 50)
    
    # Load passport data
    passport_data = load_passport_data()
    if not passport_data:
        print("No passport data found. Exiting...")
        return
    
    print(f"Processing {len(passport_data)} passport application(s)")
    
    # Create automation instance
    automation = UndetectedWebAutomation(headless=False)
    
    try:
        # Setup driver
        if not automation.setup_driver():
            print("Failed to setup undetected ChromeDriver")
            return
        
        print("ChromeDriver setup successful!")
        print("Waiting 5 seconds before navigation...")
        time.sleep(5)
        
        # Navigate to the OPR website
        target_url = "https://opr.travel.state.gov/"
        if automation.navigate_to_url(target_url):
            print(f"Successfully navigated to {target_url}")
            
            # Get page information
            page_info = automation.get_page_info()
            if page_info:
                print(f"Page Title: {page_info['title']}")
                print(f"Current URL: {page_info['url']}")
            
            # Wait 30 seconds after navigation as requested
            print("\nWaiting 30 seconds after navigation...")
            time.sleep(30)
            
            # Start step-by-step automation
            print("Starting step-by-step automation...")
            
            # Execute Step 1: Landing Page
            print("\n" + "="*50)
            print("EXECUTING STEP 1: LANDING PAGE")
            print("="*50)
            step1 = Step1LandingPage(automation.driver)
            step1_success = step1.execute()
            if not step1_success:
                print("❌ Step 1 failed. Continuing with remaining steps...")
            
            # Execute Step 2: What You Need
            print("\n" + "="*50)
            print("EXECUTING STEP 2: WHAT YOU NEED")
            print("="*50)
            step2 = Step2WhatYouNeed(automation.driver)
            step2_success = step2.execute()
            if not step2_success:
                print("❌ Step 2 failed. Continuing with remaining steps...")
            
            # Execute Step 3: Eligibility Requirements
            print("\n" + "="*50)
            print("EXECUTING STEP 3: ELIGIBILITY REQUIREMENTS")
            print("="*50)
            step3 = Step3EligibilityRequirements(automation.driver)
            step3_success = step3.execute()
            if not step3_success:
                print("❌ Step 3 failed. Continuing with remaining steps...")
            
            # Execute Step 4: Why Are We Asking For This (Travel Plans)
            print("\n" + "="*50)
            print("EXECUTING STEP 4: WHY ARE WE ASKING FOR THIS")
            print("="*50)
            # Use the first passport application data for travel plans
            travel_data = passport_data[1] if passport_data else {}
            step4 = Step4WhyAreWeAskingForThis(automation.driver, travel_data)
            step4_success = step4.execute()
            if not step4_success:
                print("❌ Step 4 failed. Automation completed with errors.")
            
            # Execute Step 5: Terms and Conditions
            print("\n" + "="*50)
            print("EXECUTING STEP 5: TERMS AND CONDITIONS")
            print("="*50)
            step5 = Step5TermsAndConditions(automation.driver)
            step5_success = step5.execute()
            if not step5_success:
                print("❌ Step 5 failed. Continuing with remaining steps...")
            
            # Execute Step 6: What Are You Renewing
            print("\n" + "="*50)
            print("EXECUTING STEP 6: WHAT ARE YOU RENEWING")
            print("="*50)
            # Use the first passport application data for renewal form
            renewal_data = passport_data[0] if passport_data else {}
            step6 = Step6WhatAreYouRenewing(automation.driver, renewal_data)
            step6_success = step6.execute()
            if not step6_success:
                print("❌ Step 6 failed. Continuing with remaining steps...")
            
            # Execute Step 7: Passport Photo Upload
            print("\n" + "="*50)
            print("EXECUTING STEP 7: PASSPORT PHOTO UPLOAD")
            print("="*50)
            step7 = Step7PassportPhoto(automation.driver)
            step7_success = step7.execute()
            if not step7_success:
                print("❌ Step 7 failed. Continuing with remaining steps...")
            
            # Execute Step 8: Personal Information
            print("\n" + "="*50)
            print("EXECUTING STEP 8: PERSONAL INFORMATION")
            print("="*50)
            # Use the first passport application data for personal information
            personal_data = passport_data[0] if passport_data else {}
            step8 = Step8PersonalInformation(automation.driver, personal_data)
            step8_success = step8.execute()
            if not step8_success:
                print("❌ Step 8 failed. Continuing with remaining steps...")
            
            # Execute Step 9: Emergency Contact
            print("\n" + "="*50)
            print("EXECUTING STEP 9: EMERGENCY CONTACT")
            print("="*50)
            # Use the first passport application data for emergency contact
            emergency_data = passport_data[0] if passport_data else {}
            step9 = Step9EmergencyContact(automation.driver, emergency_data)
            step9_success = step9.execute()
            if not step9_success:
                print("❌ Step 9 failed. Continuing with remaining steps...")
            
            # Execute Step 10: Passport Options
            print("\n" + "="*50)
            print("EXECUTING STEP 10: PASSPORT OPTIONS")
            print("="*50)
            # Use the first passport application data for passport options
            options_data = passport_data[0] if passport_data else {}
            step10 = Step10PassportOptions(automation.driver, options_data)
            step10_success = step10.execute()
            if not step10_success:
                print("❌ Step 10 failed. Automation completed with errors.")
            
            # Execute Step 11: Mailing Address
            print("\n" + "="*50)
            print("EXECUTING STEP 11: MAILING ADDRESS")
            print("="*50)
            step11 = Step11MailingAddress(automation.driver, personal_data)
            step11_success = step11.execute()
            if not step11_success:
                print("❌ Step 11 failed. Continuing with remaining steps...")
            
            # Execute Step 12: Passport Delivery
            print("\n" + "="*50)
            print("EXECUTING STEP 12: PASSPORT DELIVERY")
            print("="*50)
            step12 = Step12PassportDelivery(automation.driver, personal_data)
            step12_success = step12.execute()
            if not step12_success:
                print("❌ Step 12 failed. Continuing with remaining steps...")
            
            # Execute Step 13: Review Order
            print("\n" + "="*50)
            print("EXECUTING STEP 13: REVIEW ORDER")
            print("="*50)
            step13 = Step13ReviewOrder(automation.driver, personal_data)
            step13_success = step13.execute()
            if not step13_success:
                print("❌ Step 13 failed. Continuing with remaining steps...")
            
            # Execute Step 14: Statement of Truth
            print("\n" + "="*50)
            print("EXECUTING STEP 14: STATEMENT OF TRUTH")
            print("="*50)
            step14 = Step14StatementOfTruth(automation.driver, personal_data)
            step14_success = step14.execute()
            if not step14_success:
                print("❌ Step 14 failed. Automation completed with errors.")
            
            # Summary of results
            print("\n" + "="*50)
            print("AUTOMATION SUMMARY")
            print("="*50)
            print(f"Step 1 (Landing Page): {'✅ SUCCESS' if step1_success else '❌ FAILED'}")
            print(f"Step 2 (What You Need): {'✅ SUCCESS' if step2_success else '❌ FAILED'}")
            print(f"Step 3 (Eligibility Requirements): {'✅ SUCCESS' if step3_success else '❌ FAILED'}")
            print(f"Step 4 (Travel Plans): {'✅ SUCCESS' if step4_success else '❌ FAILED'}")
            print(f"Step 5 (Terms and Conditions): {'✅ SUCCESS' if step5_success else '❌ FAILED'}")
            print(f"Step 6 (What Are You Renewing): {'✅ SUCCESS' if step6_success else '❌ FAILED'}")
            print(f"Step 7 (Passport Photo Upload): {'✅ SUCCESS' if step7_success else '❌ FAILED'}")
            print(f"Step 8 (Personal Information): {'✅ SUCCESS' if step8_success else '❌ FAILED'}")
            print(f"Step 9 (Emergency Contact): {'✅ SUCCESS' if step9_success else '❌ FAILED'}")
            print(f"Step 10 (Passport Options): {'✅ SUCCESS' if step10_success else '❌ FAILED'}")
            print(f"Step 11 (Mailing Address): {'✅ SUCCESS' if step11_success else '❌ FAILED'}")
            print(f"Step 12 (Passport Delivery): {'✅ SUCCESS' if step12_success else '❌ FAILED'}")
            print(f"Step 13 (Review Order): {'✅ SUCCESS' if step13_success else '❌ FAILED'}")
            print(f"Step 14 (Statement of Truth): {'✅ SUCCESS' if step14_success else '❌ FAILED'}")
            
            if all([step1_success, step2_success, step3_success, step4_success, step5_success, step6_success, step7_success, step8_success, step9_success, step10_success, step11_success, step12_success, step13_success, step14_success]):
                print("\n🎉 ALL STEPS COMPLETED SUCCESSFULLY!")
            else:
                print(f"\n⚠️  AUTOMATION COMPLETED WITH {sum([step1_success, step2_success, step3_success, step4_success, step5_success, step6_success, step7_success, step8_success, step9_success, step10_success, step11_success, step12_success, step13_success, step14_success])}/14 STEPS SUCCESSFUL")
            print("="*50)
            
        else:
            print(f"Failed to navigate to {target_url}")
    
    except Exception as e:
        logger.error(f"Error in main automation: {str(e)}")
        print(f"An error occurred: {str(e)}")
    
    finally:
        # Don't close the driver - keep browser open as requested
        print("Automation completed! Browser will remain open.")


if __name__ == "__main__":
    main()
