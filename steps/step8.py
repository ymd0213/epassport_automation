"""
Step 8: Personal Information Page Automation
Handles comprehensive personal information form with conditional logic
"""

import time
import logging
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step8PersonalInformation(BaseStep):
    """Step 8: Personal information page automation"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 8: Personal Information")
        self.passport_data = passport_data
        
        # Country mapping from passport data format to country names and HTML option values
        self.country_mapping = {
            "US": {"name": "United States", "value": "USA"},
            "CA": {"name": "Canada", "value": "CAN"},
            "GB": {"name": "United Kingdom", "value": "GBR"},
            "AU": {"name": "Australia", "value": "AUS"},
            "DE": {"name": "Germany", "value": "DEU"},
            "FR": {"name": "France", "value": "FRA"},
            "IT": {"name": "Italy", "value": "ITA"},
            "ES": {"name": "Spain", "value": "ESP"},
            "JP": {"name": "Japan", "value": "JPN"},
            "CN": {"name": "China", "value": "CHN"},
            "IN": {"name": "India", "value": "IND"},
            "BR": {"name": "Brazil", "value": "BRA"},
            "MX": {"name": "Mexico", "value": "MEX"},
            "RU": {"name": "Russia", "value": "RUS"},
            "KR": {"name": "Korea, Republic of", "value": "KOR"},
            "NL": {"name": "Netherlands", "value": "NLD"},
            "SE": {"name": "Sweden", "value": "SWE"},
            "NO": {"name": "Norway", "value": "NOR"},
            "DK": {"name": "Denmark", "value": "DNK"},
            "FI": {"name": "Finland", "value": "FIN"},
            "CH": {"name": "Switzerland", "value": "CHE"},
            "AT": {"name": "Austria", "value": "AUT"},
            "BE": {"name": "Belgium", "value": "BEL"},
            "IE": {"name": "Ireland", "value": "IRL"},
            "PT": {"name": "Portugal", "value": "PRT"},
            "GR": {"name": "Greece", "value": "GRC"},
            "PL": {"name": "Poland", "value": "POL"},
            "CZ": {"name": "Czech Republic", "value": "CZE"},
            "HU": {"name": "Hungary", "value": "HUN"},
            "SK": {"name": "Slovakia", "value": "SVK"},
            "SI": {"name": "Slovenia", "value": "SVN"},
            "HR": {"name": "Croatia", "value": "HRV"},
            "BG": {"name": "Bulgaria", "value": "BGR"},
            "RO": {"name": "Romania", "value": "ROU"},
            "LT": {"name": "Lithuania", "value": "LTU"},
            "LV": {"name": "Latvia", "value": "LVA"},
            "EE": {"name": "Estonia", "value": "EST"},
            "LU": {"name": "Luxembourg", "value": "LUX"},
            "MT": {"name": "Malta", "value": "MLT"},
            "CY": {"name": "Cyprus", "value": "CYP"},
            "IS": {"name": "Iceland", "value": "ISL"},
            "LI": {"name": "Liechtenstein", "value": "LIE"},
            "MC": {"name": "Monaco", "value": "MCO"},
            "SM": {"name": "San Marino", "value": "SMR"},
            "VA": {"name": "Vatican City", "value": "VAT"},
            "AD": {"name": "Andorra", "value": "AND"},
            "TR": {"name": "Turkey", "value": "TUR"},
            "IL": {"name": "Israel", "value": "ISR"},
            "SA": {"name": "Saudi Arabia", "value": "SAU"},
            "AE": {"name": "United Arab Emirates", "value": "ARE"},
            "EG": {"name": "Egypt", "value": "EGY"},
            "ZA": {"name": "South Africa", "value": "ZAF"},
            "NG": {"name": "Nigeria", "value": "NGA"},
            "KE": {"name": "Kenya", "value": "KEN"},
            "GH": {"name": "Ghana", "value": "GHA"},
            "MA": {"name": "Morocco", "value": "MAR"},
            "TN": {"name": "Tunisia", "value": "TUN"},
            "DZ": {"name": "Algeria", "value": "DZA"},
            "LY": {"name": "Libya", "value": "LBY"},
            "SD": {"name": "Sudan", "value": "SDN"},
            "ET": {"name": "Ethiopia", "value": "ETH"},
            "UG": {"name": "Uganda", "value": "UGA"},
            "TZ": {"name": "Tanzania", "value": "TZA"},
            "MW": {"name": "Malawi", "value": "MWI"},
            "ZM": {"name": "Zambia", "value": "ZMB"},
            "ZW": {"name": "Zimbabwe", "value": "ZWE"},
            "BW": {"name": "Botswana", "value": "BWA"},
            "NA": {"name": "Namibia", "value": "NAM"},
            "SZ": {"name": "Eswatini", "value": "SWZ"},
            "LS": {"name": "Lesotho", "value": "LSO"},
            "MG": {"name": "Madagascar", "value": "MDG"},
            "MU": {"name": "Mauritius", "value": "MUS"},
            "SC": {"name": "Seychelles", "value": "SYC"},
            "KM": {"name": "Comoros", "value": "COM"},
            "DJ": {"name": "Djibouti", "value": "DJI"},
            "SO": {"name": "Somalia", "value": "SOM"},
            "ER": {"name": "Eritrea", "value": "ERI"},
            "SS": {"name": "South Sudan", "value": "SSD"},
            "CF": {"name": "Central African Republic", "value": "CAF"},
            "TD": {"name": "Chad", "value": "TCD"},
            "CM": {"name": "Cameroon", "value": "CMR"},
            "GQ": {"name": "Equatorial Guinea", "value": "GNQ"},
            "GA": {"name": "Gabon", "value": "GAB"},
            "CG": {"name": "Congo-Brazzaville", "value": "COG"},
            "CD": {"name": "Congo-Kinshasa", "value": "COD"},
            "AO": {"name": "Angola", "value": "AGO"},
            "MZ": {"name": "Mozambique", "value": "MOZ"},
            "BI": {"name": "Burundi", "value": "BDI"},
            "RW": {"name": "Rwanda", "value": "RWA"},
            "BF": {"name": "Burkina Faso", "value": "BFA"},
            "ML": {"name": "Mali", "value": "MLI"},
            "NE": {"name": "Niger", "value": "NER"},
            "SN": {"name": "Senegal", "value": "SEN"},
            "GM": {"name": "Gambia, The", "value": "GMB"},
            "GN": {"name": "Guinea", "value": "GIN"},
            "GW": {"name": "Guinea-Bissau", "value": "GNB"},
            "CV": {"name": "Cabo Verde", "value": "CPV"},
            "ST": {"name": "Sao Tome and Principe", "value": "STP"},
            "LR": {"name": "Liberia", "value": "LBR"},
            "SL": {"name": "Sierra Leone", "value": "SLE"},
            "CI": {"name": "Côte d'Ivoire", "value": "CIV"},
            "TG": {"name": "Togo", "value": "TGO"},
            "BJ": {"name": "Benin", "value": "BEN"},
            "MR": {"name": "Mauritania", "value": "MRT"}
        }
        
        # First name input
        self.first_name = {
            'css_selector': 'input[id="givenName"]',
            'xpath': '//input[@id="givenName"]',
            'id': 'givenName'
        }
        
        # Add Other Names button
        self.add_other_names_button = {
            'css_selector': 'button[type="button"][data-testid="button"].usa-button--outline.width-full.margin-top-3',
            'xpath': '//button[@type="button" and @data-testid="button" and contains(@class, "usa-button--outline") and contains(@class, "width-full") and contains(@class, "margin-top-3")]',
            'data_testid': 'button'
        }
        
        # Former name inputs
        self.former_name_a = {
            'css_selector': 'input[id="otherFirstName"]',
            'xpath': '//input[@id="otherFirstName"]',
            'id': 'otherFirstName'
        }
        
        self.former_name_b = {
            'css_selector': 'input[id="otherLastName"]',
            'xpath': '//input[@id="otherLastName"]',
            'id': 'otherLastName'
        }
        
        # Add Name button
        self.add_name_button = {
            'css_selector': 'button[type="submit"][data-testid="button"]',
            'xpath': '//button[@type="submit" and @data-testid="button"]',
            'data_testid': 'button'
        }
        
        # Phone number input
        self.phone_number = {
            'css_selector': 'input[id="phoneNumber"]',
            'xpath': '//input[@id="phoneNumber"]',
            'id': 'phoneNumber'
        }
        
        # Email inputs
        self.email_address = {
            'css_selector': 'input[id="emailAddress"]',
            'xpath': '//input[@id="emailAddress"]',
            'id': 'emailAddress'
        }
        
        self.email_verify = {
            'css_selector': 'input[id="emailVerify"]',
            'xpath': '//input[@id="emailVerify"]',
            'id': 'emailVerify'
        }
        
        # SSN inputs
        self.ssn = {
            'css_selector': 'input[id="ssn"]',
            'xpath': '//input[@id="ssn"]',
            'id': 'ssn'
        }
        
        self.ssn_verify = {
            'css_selector': 'input[id="ssnVerify"]',
            'xpath': '//input[@id="ssnVerify"]',
            'id': 'ssnVerify'
        }
        
        # Add Address button
        self.add_address_button = {
            'css_selector': 'button[type="button"][data-testid="button"].usa-button--outline.width-full:not(.margin-top-3)',
            'xpath': '//button[@type="button" and @data-testid="button" and contains(@class, "usa-button--outline") and contains(@class, "width-full") and not(contains(@class, "margin-top-3"))]',
            'data_testid': 'button'
        }
        
        # Address inputs
        self.address_1 = {
            'css_selector': 'input[id="address.address1"]',
            'xpath': '//input[@id="address.address1"]',
            'id': 'address.address1'
        }
        
        self.address_2 = {
            'css_selector': 'input[id="address.address2"]',
            'xpath': '//input[@id="address.address2"]',
            'id': 'address.address2'
        }
        
        # Country combo box for address
        self.address_country = {
            'css_selector': 'input[id="address.country"]',
            'xpath': '//input[@id="address.country"]',
            'id': 'address.country'
        }
        
        # City and ZIP inputs
        self.address_city = {
            'css_selector': 'input[id="address.city"]',
            'xpath': '//input[@id="address.city"]',
            'id': 'address.city'
        }
        
        self.address_zip = {
            'css_selector': 'input[id="address.zipCode"]',
            'xpath': '//input[@id="address.zipCode"]',
            'id': 'address.zipCode'
        }
        
        # State selection for address
        self.address_state = {
            'css_selector': 'select[id="address.state"]',
            'xpath': '//select[@id="address.state"]',
            'id': 'address.state'
        }
        
        # Add Address submit button
        self.add_address_submit = {
            'css_selector': 'button[type="submit"][data-testid="button"]',
            'xpath': '//button[@type="submit" and @data-testid="button"]',
            'data_testid': 'button'
        }
        
        # Place of birth country combo box
        self.place_of_birth_country = {
            'css_selector': 'input[id="placeOfBirth"]',
            'xpath': '//input[@id="placeOfBirth"]',
            'id': 'placeOfBirth'
        }

        # State of birth combo box
        self.state_of_birth = {
            'css_selector': 'input[id="stateOfBirth"]',
            'xpath': '//input[@id="stateOfBirth"]',
            'id': 'stateOfBirth',
            'data_testid': 'combo-box-input'
        }
        
        # City of birth input
        self.city_of_birth = {
            'css_selector': 'input[id="cityOfBirth"]',
            'xpath': '//input[@id="cityOfBirth"]',
            'id': 'cityOfBirth'
        }
        
        # Personal details selects
        self.gender = {
            'css_selector': 'select[id="gender"]',
            'xpath': '//select[@id="gender"]',
            'id': 'gender'
        }
        
        self.eye_color = {
            'css_selector': 'select[id="eyeColor"]',
            'xpath': '//select[@id="eyeColor"]',
            'id': 'eyeColor'
        }
        
        self.hair_color = {
            'css_selector': 'select[id="hairColor"]',
            'xpath': '//select[@id="hairColor"]',
            'id': 'hairColor'
        }
        
        self.height_feet = {
            'css_selector': 'select[id="heightFeet"]',
            'xpath': '//select[@id="heightFeet"]',
            'id': 'heightFeet'
        }
        
        self.height_inches = {
            'css_selector': 'select[id="heightInches"]',
            'xpath': '//select[@id="heightInches"]',
            'id': 'heightInches'
        }
        
        # Occupation inputs
        self.occupation = {
            'css_selector': 'input[id="occupation"]',
            'xpath': '//input[@id="occupation"]',
            'id': 'occupation'
        }
        
        self.employer_or_school = {
            'css_selector': 'input[id="employerOrSchool"]',
            'xpath': '//input[@id="employerOrSchool"]',
            'id': 'employerOrSchool'
        }
        
        # Continue button
        self.continue_button = {
            'css_selector': 'button[type="submit"][data-testid="button"].padding-y-2',
            'xpath': '//button[@type="submit" and @data-testid="button" and contains(@class, "padding-y-2")]',
            'data_testid': 'button'
        }
    
    def find_and_select_combo_box_option(self, combo_selector, country_code, description="combo box"):
        """
        Find and select from a combo box using country code
        
        Args:
            combo_selector (dict): Dictionary containing selector strategies
            country_code (str): Country code from passport data (e.g., "US", "CA")
            description (str): Description of the combo box for logging
            
        Returns:
            bool: True if selection was successful, False otherwise
        """
        try:
            logger.info(f"Looking for {description}...")
            
            # Get country information from mapping
            country_info = self.country_mapping.get(country_code, {"name": country_code, "value": country_code})
            country_name = country_info["name"]
            country_value = country_info["value"]
            
            logger.info(f"Converting country code '{country_code}' to name '{country_name}' and value '{country_value}' for {description}")
            
            # Try different selector strategies
            selectors = []
            
            if combo_selector.get('css_selector'):
                selectors.append(('css selector', combo_selector.get('css_selector')))
            
            if combo_selector.get('xpath'):
                selectors.append(('xpath', combo_selector.get('xpath')))
            
            if combo_selector.get('id'):
                selectors.append(('id', combo_selector.get('id')))
            
            combo_input = None
            for by, selector in selectors:
                if selector:
                    try:
                        combo_input = self.wait.until(lambda driver: driver.find_element(by, selector))
                        logger.info(f"Found {description} using {by}: {selector}")
                        break
                    except:
                        continue
            
            if combo_input:
                # Clear and type the country name to trigger dropdown
                combo_input.clear()
                combo_input.send_keys(country_name)
                time.sleep(2)  # Wait for dropdown to appear
                
                # Find and click the option by searching for the option with matching data-value
                try:
                    # Look for the option with the specific data-value attribute
                    option_selector = f'[data-testid="combo-box-option-{country_value}"]'
                    option = self.wait.until(lambda driver: driver.find_element("css selector", option_selector))
                    option.click()
                    logger.info(f"✅ Successfully selected option with value '{country_value}' from {description}")
                    return True
                except:
                    # Fallback: try to find by data-value attribute directly
                    try:
                        option_selector = f'li[data-value="{country_value}"]'
                        option = self.wait.until(lambda driver: driver.find_element("css selector", option_selector))
                        option.click()
                        logger.info(f"✅ Successfully selected option with data-value '{country_value}' from {description}")
                        return True
                    except:
                        logger.error(f"❌ Could not find option with value '{country_value}' in {description}")
                        return False
            else:
                logger.error(f"❌ Could not find {description}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error selecting from {description}: {str(e)}")
            return False
    
    def execute(self):
        """
        Execute Step 8: Handle personal information form
        
        Returns:
            bool: True if step completed successfully, False otherwise
        """
        try:
            self.log_step_info()
            
            # Wait for page to load
            self.wait_for_page_load()
            
            # Fill first name
            logger.info("Filling first name...")
            first_name = self.passport_data.get('first_name', '')
            if first_name:
                if not self.find_and_input_text(self.first_name, first_name, "first name"):
                    logger.error("Failed to input first name")
                    return False
                time.sleep(2)
            
            # Handle former name logic
            former_name = self.passport_data.get('former__name', '')
            if former_name == 1 or former_name == "1":
                logger.info("Former name is 1, clicking Add Other Names button...")
                if not self.find_and_click_button(self.add_other_names_button, "Add Other Names button"):
                    logger.error("Failed to click Add Other Names button")
                    return False
                time.sleep(1)
                
                # Fill former name A
                former_name_a = self.passport_data.get('former_name_a', '')
                if former_name_a:
                    if not self.find_and_input_text(self.former_name_a, former_name_a, "former name A"):
                        logger.error("Failed to input former name A")
                        return False
                    time.sleep(2)
                
                # Fill former name B
                former_name_b = self.passport_data.get('former_name_b', '')
                if former_name_b:
                    if not self.find_and_input_text(self.former_name_b, former_name_b, "former name B"):
                        logger.error("Failed to input former name B")
                        return False
                    time.sleep(2)
                
                # Click Add Name button
                if not self.find_and_click_button(self.add_name_button, "Add Name button"):
                    logger.error("Failed to click Add Name button")
                    return False
                time.sleep(1)
            
            # Fill phone number
            logger.info("Filling phone number...")
            phone_number = self.passport_data.get('phone_number', '')
            if phone_number:
                if not self.find_and_input_text(self.phone_number, phone_number, "phone number"):
                    logger.error("Failed to input phone number")
                    return False
                time.sleep(2)
            
            # Fill email addresses
            logger.info("Filling email addresses...")
            email = self.passport_data.get('email', '')
            if email:
                if not self.find_and_input_text(self.email_address, email, "email address"):
                    logger.error("Failed to input email address")
                    return False
                time.sleep(2)
                
                if not self.find_and_input_text(self.email_verify, email, "email verification"):
                    logger.error("Failed to input email verification")
                    return False
                time.sleep(2)
            
            # Fill SSN (merge ssn_1, ssn_2, ssn_3)
            logger.info("Filling SSN...")
            ssn_1 = self.passport_data.get('ssn_1', '')
            ssn_2 = self.passport_data.get('ssn_2', '')
            ssn_3 = self.passport_data.get('ssn_3', '')
            
            if ssn_1 and ssn_2 and ssn_3:
                full_ssn = f"{ssn_1}{ssn_2}{ssn_3}"
                if not self.find_and_input_text(self.ssn, full_ssn, "SSN"):
                    logger.error("Failed to input SSN")
                    return False
                time.sleep(2)
                
                if not self.find_and_input_text(self.ssn_verify, full_ssn, "SSN verification"):
                    logger.error("Failed to input SSN verification")
                    return False
                time.sleep(2)
            
            # Click Add Address button
            logger.info("Clicking Add Address button...")
            if not self.find_and_click_button(self.add_address_button, "Add Address button"):
                logger.error("Failed to click Add Address button")
                return False
            time.sleep(1)
            
            # Fill address based on permanent_address_same condition
            permanent_address_same = self.passport_data.get('permanent_address_same', '')
            
            # Address 1
            if permanent_address_same == "1" or permanent_address_same == 1:
                address_1 = self.passport_data.get('mailing_address_1', '')
            else:
                address_1 = self.passport_data.get('permanent_address_1', '')
            
            if address_1:
                if not self.find_and_input_text(self.address_1, address_1, "address 1"):
                    logger.error("Failed to input address 1")
                    return False
                time.sleep(2)
            
            # Address 2
            if permanent_address_same == "1" or permanent_address_same == 1:
                address_2 = self.passport_data.get('mailing_address_2', '')
            else:
                address_2 = self.passport_data.get('permanent_address_2', '')
            
            if address_2:
                if not self.find_and_input_text(self.address_2, address_2, "address 2"):
                    logger.error("Failed to input address 2")
                    return False
                time.sleep(2)
            
            # Country selection for address
            if permanent_address_same == "1" or permanent_address_same == 1:
                country_code = self.passport_data.get('mailing_country', '')
            else:
                country_code = self.passport_data.get('permanent_country', '')  # Use permanent_country when addresses are different
            
            if country_code:
                if not self.find_and_select_combo_box_option(self.address_country, country_code, "address country"):
                    logger.error("Failed to select address country")
                    return False
                time.sleep(2)
            
            # City
            if permanent_address_same == "1" or permanent_address_same == 1:
                city = self.passport_data.get('mailing_city', '')
            else:
                city = self.passport_data.get('permanent_city', '')
            
            if city:
                if not self.find_and_input_text(self.address_city, city, "address city"):
                    logger.error("Failed to input address city")
                    return False
                time.sleep(2)
            
            # State selection
            if permanent_address_same == "1" or permanent_address_same == 1:
                state = self.passport_data.get('mailing_state', '')
            else:
                state = self.passport_data.get('permanent_state', '')
            
            if state:
                if not self.find_and_select_option(self.address_state, state, "address state"):
                    logger.error("Failed to select address state")
                    return False
                time.sleep(2)
            
            # ZIP code
            if permanent_address_same == "1" or permanent_address_same == 1:
                zip_code = self.passport_data.get('mailing_zip', '')
            else:
                zip_code = self.passport_data.get('permanent_zip', '')
            
            if zip_code:
                if not self.find_and_input_text(self.address_zip, zip_code, "address ZIP"):
                    logger.error("Failed to input address ZIP")
                    return False
                time.sleep(2)
            
            # Click Add Address submit button
            if not self.find_and_click_button(self.add_address_submit, "Add Address submit button"):
                logger.error("Failed to click Add Address submit button")
                return False
            time.sleep(5)  # Wait 10 seconds after address submit
            
            # Click Continue after address submission
            logger.info("Clicking Continue button after address submission...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button after address submission")
                return False
            time.sleep(5)
            
            # Fill place of birth country
            logger.info("Filling place of birth...")
            country_birth = self.passport_data.get('country_birth', '')
            if country_birth:
                if not self.find_and_select_combo_box_option(self.place_of_birth_country, country_birth, "place of birth country"):
                    logger.error("Failed to select place of birth country")
                    return False
                time.sleep(2)
            
            # State of birth (combo box by name)
            state_birth = self.passport_data.get('state_birth', '')
            if state_birth:
                if not self.find_and_select_combo_box(self.state_of_birth, state_birth, "state of birth"):
                    logger.error("Failed to select state of birth")
                    return False
                time.sleep(2)
            
            # City of birth
            city_birth = self.passport_data.get('city_birth', '')
            if city_birth:
                if not self.find_and_input_text(self.city_of_birth, city_birth, "city of birth"):
                    logger.error("Failed to input city of birth")
                    return False
                time.sleep(2)
            
            # Fill personal details
            logger.info("Filling personal details...")
            
            # Gender (convert "female" to "F", "male" to "M")
            gender = self.passport_data.get('gender', '').lower()
            if gender == "female":
                gender_value = "F"
            elif gender == "male":
                gender_value = "M"
            else:
                gender_value = ""
            
            if gender_value:
                if not self.find_and_select_option(self.gender, gender_value, "gender"):
                    logger.error("Failed to select gender")
                    return False
                time.sleep(2)
            
            # Eye color (convert index to option value)
            eye_color_index = self.passport_data.get('eye_color', '')
            if eye_color_index:
                eye_color_options = ["", "amber", "black", "blue", "brown", "gray", "green", "hazel", "violet"]
                try:
                    eye_color_value = eye_color_options[int(eye_color_index)]
                    if eye_color_value:
                        if not self.find_and_select_option(self.eye_color, eye_color_value, "eye color"):
                            logger.error("Failed to select eye color")
                            return False
                        time.sleep(2)
                except (ValueError, IndexError):
                    logger.warning(f"Invalid eye color index: {eye_color_index}")
            
            # Hair color (convert index to option value)
            hair_color_index = self.passport_data.get('hair_color', '')
            if hair_color_index:
                hair_color_options = ["", "black", "brown", "blonde", "red", "gray", "bald", "other"]
                try:
                    hair_color_value = hair_color_options[int(hair_color_index)]
                    if hair_color_value:
                        if not self.find_and_select_option(self.hair_color, hair_color_value, "hair color"):
                            logger.error("Failed to select hair color")
                            return False
                        time.sleep(2)
                except (ValueError, IndexError):
                    logger.warning(f"Invalid hair color index: {hair_color_index}")
            
            # Height feet
            height_ft = self.passport_data.get('height_ft', '')
            if height_ft:
                if not self.find_and_select_option(self.height_feet, str(height_ft), "height feet"):
                    logger.error("Failed to select height feet")
                    return False
                time.sleep(2)
            
            # Height inches
            height_in = self.passport_data.get('height_in', '')
            if height_in:
                if not self.find_and_select_option(self.height_inches, str(height_in), "height inches"):
                    logger.error("Failed to select height inches")
                    return False
                time.sleep(2)
            
            # Occupation
            occupation = self.passport_data.get('occupation', '')
            if occupation:
                if not self.find_and_input_text(self.occupation, occupation, "occupation"):
                    logger.error("Failed to input occupation")
                    return False
                time.sleep(2)
            
            # Employer or school
            employer_or_school = self.passport_data.get('employer_or_school', '')
            if employer_or_school:
                if not self.find_and_input_text(self.employer_or_school, employer_or_school, "employer or school"):
                    logger.error("Failed to input employer or school")
                    return False
                time.sleep(2)
            
            # Click Continue button
            logger.info("Clicking Continue button...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                return False
            
            logger.info("✅ Step 8 completed successfully - Personal information form submitted")
            return True
            
        except Exception as e:
            logger.error(f"❌ Step 8 failed with error: {str(e)}")
            return False
