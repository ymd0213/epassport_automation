"""
Step 8: Personal Information Page Automation
Handles comprehensive personal information form with conditional logic
"""

import time
import logging
import re
from .base_step import BaseStep

logger = logging.getLogger(__name__)


class Step8PersonalInformation(BaseStep):
    """Step 8: Personal information page automation"""
    
    def __init__(self, driver, passport_data):
        super().__init__(driver, "Step 8: Personal Information")
        self.passport_data = passport_data
        
        # Country mapping from passport data format (2-letter codes) to target format (3-letter codes)
        # Source: country-birth select element | Target: placeOfBirth select element
        self.country_mapping = {
            "US": {"name": "United States", "value": "USA"},
            "AF": {"name": "Afghanistan", "value": "AFG"},
            "AX": {"name": "Akrotiri Sovereign Base Area", "value": "XAK"},  # Not in target, using placeholder
            "AL": {"name": "Albania", "value": "ALB"},
            "AG": {"name": "Algeria", "value": "DZA"},
            "AN": {"name": "Andorra", "value": "AND"},
            "AO": {"name": "Angola", "value": "AGO"},
            "AV": {"name": "Anguilla", "value": "AIA"},
            "AY": {"name": "Antarctica", "value": "ATA"},  # Not in target, using ISO code
            "AC": {"name": "Antigua and Barbuda", "value": "ATG"},
            "AR": {"name": "Argentina", "value": "ARG"},
            "AM": {"name": "Armenia", "value": "ARM"},
            "AA": {"name": "Aruba", "value": "ABW"},
            "AT": {"name": "Ashmore And Cartier Islands", "value": "XAT"},  # Not in target, using placeholder
            "AS": {"name": "Australia", "value": "AUS"},
            "AU": {"name": "Austria", "value": "AUT"},
            "AJ": {"name": "Azerbaijan", "value": "AZE"},
            "BF": {"name": "Bahamas, The", "value": "BHS"},
            "BA": {"name": "Bahrain", "value": "BHR"},
            "FQ": {"name": "Baker Island", "value": "XBK"},
            "BG": {"name": "Bangladesh", "value": "BGD"},
            "BB": {"name": "Barbados", "value": "BRB"},
            "BO": {"name": "Belarus", "value": "BLR"},
            "BE": {"name": "Belgium", "value": "BEL"},
            "BH": {"name": "Belize", "value": "BLZ"},
            "BN": {"name": "Benin", "value": "BEN"},
            "BD": {"name": "Bermuda", "value": "BMU"},
            "BT": {"name": "Bhutan", "value": "BTN"},
            "BL": {"name": "Bolivia", "value": "BOL"},
            "BK": {"name": "Bosnia and Herzegovina", "value": "BIH"},
            "BC": {"name": "Botswana", "value": "BWA"},
            "BV": {"name": "Bouvet Island", "value": "BVT"},  # Not in target, using ISO code
            "BR": {"name": "Brazil", "value": "BRA"},
            "IO": {"name": "British Indian Ocean Territory", "value": "IOT"},  # Not in target, using ISO code
            "BX": {"name": "Brunei", "value": "BRN"},
            "BU": {"name": "Bulgaria", "value": "BGR"},
            "UV": {"name": "Burkina Faso", "value": "BFA"},
            "BM": {"name": "Burma", "value": "MMR"},
            "BY": {"name": "Burundi", "value": "BDI"},
            "CB": {"name": "Cambodia", "value": "KHM"},
            "CM": {"name": "Cameroon", "value": "CMR"},
            "CA": {"name": "Canada", "value": "CAN"},
            "CV": {"name": "Cabo Verde", "value": "CPV"},
            "CJ": {"name": "Cayman Islands", "value": "CYM"},
            "CT": {"name": "Central African Republic", "value": "CAF"},
            "CD": {"name": "Chad", "value": "TCD"},
            "CI": {"name": "Chile", "value": "CHL"},
            "CH": {"name": "China", "value": "CHN"},
            "KT": {"name": "Christmas Island", "value": "CXR"},  # Not in target, using ISO code
            "IP": {"name": "Clipperton Island", "value": "CPT"},  # Not in target, using ISO code
            "CK": {"name": "Cocos Keeling Islands", "value": "CCK"},  # Not in target, using ISO code
            "CO": {"name": "Colombia", "value": "COL"},
            "CN": {"name": "Comoros", "value": "COM"},
            "CF": {"name": "Congo-Brazzaville", "value": "COG"},
            "CG": {"name": "Congo-Kinshasa", "value": "COD"},
            "CW": {"name": "Cook Islands", "value": "COK"},
            "CR": {"name": "Coral Sea Islands", "value": "XCR"},  # Not in target, using placeholder
            "CS": {"name": "Costa Rica", "value": "CRI"},
            "IV": {"name": "Côte d'Ivoire", "value": "CIV"},
            "HR": {"name": "Croatia", "value": "HRV"},
            "CU": {"name": "Cuba", "value": "CUB"},
            "CY": {"name": "Cyprus", "value": "CYP"},
            "EZ": {"name": "Czech Republic", "value": "CZE"},
            "DA": {"name": "Denmark", "value": "DNK"},
            "DX": {"name": "Dhekelia Sovereign Base Area", "value": "XDX"},  # Not in target, using placeholder
            "DJ": {"name": "Djibouti", "value": "DJI"},
            "DO": {"name": "Dominica", "value": "DMA"},
            "DR": {"name": "Dominican Republic", "value": "DOM"},
            "TT": {"name": "Timor-Leste", "value": "TLS"},
            "EC": {"name": "Ecuador", "value": "ECU"},
            "EG": {"name": "Egypt", "value": "EGY"},
            "ES": {"name": "El Salvador", "value": "SLV"},
            "EK": {"name": "Equatorial Guinea", "value": "GNQ"},
            "ER": {"name": "Eritrea", "value": "ERI"},
            "EN": {"name": "Estonia", "value": "EST"},
            "ET": {"name": "Ethiopia", "value": "ETH"},
            "FK": {"name": "Falkland Islands (Islas Malvinas)", "value": "FLK"},
            "FO": {"name": "Faroe Islands", "value": "FRO"},
            "FJ": {"name": "Fiji", "value": "FJI"},
            "FI": {"name": "Finland", "value": "FIN"},
            "FR": {"name": "France", "value": "FRA"},
            "FP": {"name": "French Polynesia", "value": "PYF"},
            "FS": {"name": "French Southern And Antarctic Lands", "value": "ATF"},  # Not in target, using ISO code
            "GB": {"name": "Gabon", "value": "GAB"},
            "GA": {"name": "Gambia, The", "value": "GMB"},
            "GG": {"name": "Georgia", "value": "GEO"},
            "GM": {"name": "Germany", "value": "DEU"},
            "GH": {"name": "Ghana", "value": "GHA"},
            "GI": {"name": "Gibraltar", "value": "GIB"},
            "GR": {"name": "Greece", "value": "GRC"},
            "GL": {"name": "Greenland", "value": "GRL"},
            "GJ": {"name": "Grenada", "value": "GRD"},
            "GT": {"name": "Guatemala", "value": "GTM"},
            "GK": {"name": "Guernsey", "value": "GGY"},
            "GV": {"name": "Guinea", "value": "GIN"},
            "PU": {"name": "Guinea-Bissau", "value": "GNB"},
            "GY": {"name": "Guyana", "value": "GUY"},
            "HA": {"name": "Haiti", "value": "HTI"},
            "HM": {"name": "Heard Island And Mcdonald Islands", "value": "HMD"},  # Not in target, using ISO code
            "VT": {"name": "Holy See", "value": "VAT"},  # Not in target, using ISO code
            "HO": {"name": "Honduras", "value": "HND"},
            "HK": {"name": "Hong Kong SAR", "value": "HKG"},
            "HQ": {"name": "Howland Island", "value": "XHO"},
            "HU": {"name": "Hungary", "value": "HUN"},
            "IC": {"name": "Iceland", "value": "ISL"},
            "IN": {"name": "India", "value": "IND"},
            "ID": {"name": "Indonesia", "value": "IDN"},
            "IR": {"name": "Iran", "value": "IRN"},
            "IZ": {"name": "Iraq", "value": "IRQ"},
            "EI": {"name": "Ireland", "value": "IRL"},
            "IM": {"name": "Isle Of Man", "value": "IMN"},
            "IS": {"name": "Israel", "value": "ISR"},
            "IT": {"name": "Italy", "value": "ITA"},
            "JM": {"name": "Jamaica", "value": "JAM"},
            "JN": {"name": "Jan Mayen", "value": "SJM"},  # Not in target, using ISO code
            "JA": {"name": "Japan", "value": "JPN"},
            "DQ": {"name": "Jarvis Island", "value": "XJV"},  # Not in target, using placeholder
            "JE": {"name": "Jersey", "value": "JEY"},
            "JQ": {"name": "Johnston Atoll", "value": "XJA"},
            "JO": {"name": "Jordan", "value": "JOR"},
            "KZ": {"name": "Kazakhstan", "value": "KAZ"},
            "KE": {"name": "Kenya", "value": "KEN"},
            "KQ": {"name": "Kingman Reef", "value": "XKR"},  # Not in target, using placeholder
            "KR": {"name": "Kiribati", "value": "KIR"},
            "KN": {"name": "Korea North", "value": "PRK"},  # Not in target, using ISO code
            "KS": {"name": "Korea, Republic of", "value": "KOR"},
            "KU": {"name": "Kuwait", "value": "KWT"},
            "KG": {"name": "Kyrgyzstan", "value": "KGZ"},
            "LA": {"name": "Laos", "value": "LAO"},
            "LG": {"name": "Latvia", "value": "LVA"},
            "LE": {"name": "Lebanon", "value": "LBN"},
            "LT": {"name": "Lesotho", "value": "LSO"},
            "LI": {"name": "Liberia", "value": "LBR"},
            "LY": {"name": "Libya", "value": "LBY"},
            "LS": {"name": "Liechtenstein", "value": "LIE"},
            "LH": {"name": "Lithuania", "value": "LTU"},
            "LU": {"name": "Luxembourg", "value": "LUX"},
            "MC": {"name": "Macau SAR", "value": "MAC"},
            "MK": {"name": "North Macedonia", "value": "MKD"},
            "MA": {"name": "Madagascar", "value": "MDG"},
            "MI": {"name": "Malawi", "value": "MWI"},
            "MY": {"name": "Malaysia", "value": "MYS"},
            "MV": {"name": "Maldives", "value": "MDV"},
            "ML": {"name": "Mali", "value": "MLI"},
            "MT": {"name": "Malta", "value": "MLT"},
            "RM": {"name": "Marshall Islands", "value": "MHL"},
            "MR": {"name": "Mauritania", "value": "MRT"},
            "MP": {"name": "Mauritius", "value": "MUS"},
            "MF": {"name": "Mayotte", "value": "MYT"},
            "MX": {"name": "Mexico", "value": "MEX"},
            "FM": {"name": "Micronesia, Federated States Of", "value": "FSM"},
            "MQ": {"name": "Midway Islands", "value": "XMI"},  # Not in target, using placeholder
            "MD": {"name": "Moldova", "value": "MDA"},
            "MN": {"name": "Monaco", "value": "MCO"},
            "MG": {"name": "Mongolia", "value": "MNG"},
            "MJ": {"name": "Montenegro", "value": "MNE"},
            "MH": {"name": "Montserrat", "value": "MSR"},
            "MO": {"name": "Morocco", "value": "MAR"},
            "MZ": {"name": "Mozambique", "value": "MOZ"},
            "WA": {"name": "Namibia", "value": "NAM"},
            "NR": {"name": "Nauru", "value": "NRU"},
            "BQ": {"name": "Navassa Island", "value": "XNV"},  # Not in target, using placeholder
            "NP": {"name": "Nepal", "value": "NPL"},
            "NL": {"name": "Netherlands", "value": "NLD"},
            "NT": {"name": "Netherlands Antilles", "value": "ANT"},  # Not in target, using ISO code (dissolved)
            "NC": {"name": "New Caledonia", "value": "NCL"},
            "NZ": {"name": "New Zealand", "value": "NZL"},
            "NU": {"name": "Nicaragua", "value": "NIC"},
            "NG": {"name": "Niger", "value": "NER"},
            "NI": {"name": "Nigeria", "value": "NGA"},
            "NE": {"name": "Niue", "value": "NIU"},
            "NF": {"name": "Norfolk Island", "value": "NFK"},
            "CQ": {"name": "Northern Mariana Islands", "value": "MNP"},  # Not in target, using ISO code
            "NO": {"name": "Norway", "value": "NOR"},
            "MU": {"name": "Oman", "value": "OMN"},
            "PK": {"name": "Pakistan", "value": "PAK"},
            "PS": {"name": "Palau", "value": "PLW"},
            "LQ": {"name": "Palmyra Atoll", "value": "XPL"},
            "PM": {"name": "Panama", "value": "PAN"},
            "PP": {"name": "Papua New Guinea", "value": "PNG"},
            "PF": {"name": "Paracel Islands", "value": "XPI"},  # Not in target, using placeholder
            "PA": {"name": "Paraguay", "value": "PRY"},
            "PE": {"name": "Peru", "value": "PER"},
            "RP": {"name": "Philippines", "value": "PHL"},
            "PC": {"name": "Pitcairn Islands", "value": "PCN"},
            "PL": {"name": "Poland", "value": "POL"},
            "PO": {"name": "Portugal", "value": "PRT"},
            "QA": {"name": "Qatar", "value": "QAT"},
            "RO": {"name": "Romania", "value": "ROU"},
            "RS": {"name": "Russia", "value": "RUS"},
            "RW": {"name": "Rwanda", "value": "RWA"},
            "SH": {"name": "Saint Helena", "value": "SHN"},
            "SC": {"name": "Saint Kitts and Nevis", "value": "KNA"},
            "ST": {"name": "Saint Lucia", "value": "LCA"},
            "SB": {"name": "Saint Pierre and Miquelon", "value": "SPM"},
            "VC": {"name": "Saint Vincent and the Grenadines", "value": "VCT"},
            "WS": {"name": "Samoa", "value": "WSM"},
            "SM": {"name": "San Marino", "value": "SMR"},
            "TP": {"name": "Sao Tome and Principe", "value": "STP"},
            "SA": {"name": "Saudi Arabia", "value": "SAU"},
            "SG": {"name": "Senegal", "value": "SEN"},
            "RB": {"name": "Serbia", "value": "SRB"},
            "SE": {"name": "Seychelles", "value": "SYC"},
            "SL": {"name": "Sierra Leone", "value": "SLE"},
            "SN": {"name": "Singapore", "value": "SGP"},
            "LO": {"name": "Slovakia", "value": "SVK"},
            "SI": {"name": "Slovenia", "value": "SVN"},
            "BP": {"name": "Solomon Islands", "value": "SLB"},
            "SO": {"name": "Somalia", "value": "SOM"},
            "SF": {"name": "South Africa", "value": "ZAF"},
            "SX": {"name": "South Georgia And South Sandwich Islands", "value": "SGS"},  # Not in target, using ISO code
            "SP": {"name": "Spain", "value": "ESP"},
            "PG": {"name": "Spratly Islands", "value": "XSP"},  # Not in target, using placeholder
            "CE": {"name": "Sri Lanka", "value": "LKA"},
            "SU": {"name": "Sudan", "value": "SDN"},
            "NS": {"name": "Suriname", "value": "SUR"},
            "SV": {"name": "Svalbard", "value": "SJM"},  # Not in target, using ISO code
            "WZ": {"name": "Eswatini", "value": "SWZ"},
            "SW": {"name": "Sweden", "value": "SWE"},
            "SZ": {"name": "Switzerland", "value": "CHE"},
            "SY": {"name": "Syria", "value": "SYR"},
            "TW": {"name": "Taiwan", "value": "TWN"},
            "TI": {"name": "Tajikistan", "value": "TJK"},
            "TZ": {"name": "Tanzania", "value": "TZA"},
            "TH": {"name": "Thailand", "value": "THA"},
            "TO": {"name": "Togo", "value": "TGO"},
            "TL": {"name": "Tokelau", "value": "TKL"},
            "TN": {"name": "Tonga", "value": "TON"},
            "TD": {"name": "Trinidad and Tobago", "value": "TTO"},
            "TS": {"name": "Tunisia", "value": "TUN"},
            "TU": {"name": "Turkey", "value": "TUR"},
            "TX": {"name": "Turkmenistan", "value": "TKM"},
            "TK": {"name": "Turks and Caicos Islands", "value": "TCA"},
            "TV": {"name": "Tuvalu", "value": "TUV"},
            "UG": {"name": "Uganda", "value": "UGA"},
            "UP": {"name": "Ukraine", "value": "UKR"},
            "AE": {"name": "United Arab Emirates", "value": "ARE"},
            "UK": {"name": "United Kingdom", "value": "GBR"},
            "UY": {"name": "Uruguay", "value": "URY"},
            "UZ": {"name": "Uzbekistan", "value": "UZB"},
            "NH": {"name": "Vanuatu", "value": "VUT"},
            "VE": {"name": "Venezuela", "value": "VEN"},
            "VM": {"name": "Vietnam", "value": "VNM"},
            "VI": {"name": "Virgin Islands British", "value": "VGB"},
            "WQ": {"name": "Wake Island", "value": "XWK"},
            "WF": {"name": "Wallis and Futuna", "value": "WLF"},
            "WI": {"name": "Western Sahara", "value": "ESH"},  # Not in target, using ISO code
            "YM": {"name": "Yemen", "value": "YEM"},
            "ZA": {"name": "Zambia", "value": "ZMB"},
            "ZI": {"name": "Zimbabwe", "value": "ZWE"}
        }
        
        # State code to full name mapping for state of birth combo box
        self.state_mapping = {
            "AL": "Alabama",
            "AK": "Alaska",
            "AS": "American Samoa",
            "AZ": "Arizona",
            "AR": "Arkansas",
            "CA": "California",
            "CO": "Colorado",
            "CT": "Connecticut",
            "DE": "Delaware",
            "DC": "District Of Columbia",
            "FL": "Florida",
            "GA": "Georgia",
            "GU": "Guam",
            "HI": "Hawaii",
            "ID": "Idaho",
            "IL": "Illinois",
            "IN": "Indiana",
            "IA": "Iowa",
            "KS": "Kansas",
            "KY": "Kentucky",
            "LA": "Louisiana",
            "ME": "Maine",
            "MD": "Maryland",
            "MA": "Massachusetts",
            "MI": "Michigan",
            "UM": "Midway Islands",
            "MN": "Minnesota",
            "MS": "Mississippi",
            "MO": "Missouri",
            "MT": "Montana",
            "NE": "Nebraska",
            "NV": "Nevada",
            "NH": "New Hampshire",
            "NJ": "New Jersey",
            "NM": "New Mexico",
            "NY": "New York",
            "NC": "North Carolina",
            "ND": "North Dakota",
            "MP": "Northern Mariana Islands",
            "OH": "Ohio",
            "OK": "Oklahoma",
            "OR": "Oregon",
            "PA": "Pennsylvania",
            "PR": "Puerto Rico",
            "RI": "Rhode Island",
            "SC": "South Carolina",
            "SD": "South Dakota",
            "TN": "Tennessee",
            "TX": "Texas",
            "VI": "U.S. Virgin Islands",
            "UT": "Utah",
            "VT": "Vermont",
            "VA": "Virginia",
            "WA": "Washington",
            "WV": "West Virginia",
            "WI": "Wisconsin",
            "WY": "Wyoming"
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
    
    def check_for_errors(self):
        """
        Check for error messages after button clicks
        
        Returns:
            dict or None: Error data if found, None if no errors
        """
        try:
            # Look for error alert body
            error_alert = self.driver.find_element("css selector", "div.usa-alert__body")
            if error_alert:
                # Find all span elements with class "text-bold" inside the alert
                try:
                    bold_spans = error_alert.find_elements("css selector", "span.text-bold")
                    if bold_spans:
                        error_messages = []
                        for span in bold_spans:
                            if span.text.strip():
                                error_messages.append(span.text.strip())
                        
                        if error_messages:
                            error_message = ", ".join(error_messages)
                            logger.error(f"❌ Error found: {error_message}")
                            page_code = self.get_page_name_code()
                            return {
                                'status': False,
                                'code': f'{page_code}_FORM_VALIDATION_ERROR',
                                'message': error_message
                            }
                except:
                    # If we can't find specific bold spans, get the general error text
                    error_text = error_alert.text.strip()
                    if error_text:
                        logger.error(f"❌ General error found: {error_text}")
                        page_code = self.get_page_name_code()
                        return {
                            'status': False,
                            'code': f'{page_code}_PERSONAL_INFORMATION_ERROR',
                            'message': error_text
                        }
        except:
            # No error alert found
            pass
        
        return None
    
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
                time.sleep(0.5)  # Wait for dropdown to appear
                
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
                time.sleep(0.5)
            
            # Fill phone number
            logger.info("Filling phone number...")
            phone_number = self.passport_data.get('phone_number', '')
            if phone_number:
                # Remove dashes from phone number
                phone_number = re.sub(r'[^0-9]', '', phone_number)
                if not self.find_and_input_text(self.phone_number, phone_number, "phone number"):
                    logger.error("Failed to input phone number")
                    return False
                time.sleep(0.5)
            
            # Fill email addresses
            logger.info("Filling email addresses...")
            email = self.passport_data.get('email', '')
            if email:
                if not self.find_and_input_text(self.email_address, email, "email address"):
                    logger.error("Failed to input email address")
                    return False
                time.sleep(0.5)
                
                if not self.find_and_input_text(self.email_verify, email, "email verification"):
                    logger.error("Failed to input email verification")
                    return False
                time.sleep(0.5)
            
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
                time.sleep(0.5)
                
                if not self.find_and_input_text(self.ssn_verify, full_ssn, "SSN verification"):
                    logger.error("Failed to input SSN verification")
                    return False
                time.sleep(0.5)
            
            # Click Add Address button
            logger.info("Clicking Add Address button...")
            if not self.find_and_click_button(self.add_address_button, "Add Address button"):
                logger.error("Failed to click Add Address button")
                return False
            time.sleep(1)
            
            # Check for errors after Add Address button click
            error_result = self.check_for_errors()
            if error_result:
                return error_result
            
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
                time.sleep(0.5)
            
            # Address 2
            if permanent_address_same == "1" or permanent_address_same == 1:
                address_2 = self.passport_data.get('mailing_address_2', '')
            else:
                address_2 = self.passport_data.get('permanent_address_2', '')
            
            if address_2:
                if not self.find_and_input_text(self.address_2, address_2, "address 2"):
                    logger.error("Failed to input address 2")
                    return False
                time.sleep(0.5)
            
            # Country selection for address
            if permanent_address_same == "1" or permanent_address_same == 1:
                country_code = self.passport_data.get('mailing_country', '')
            else:
                country_code = self.passport_data.get('permanent_country', '')  # Use permanent_country when addresses are different
            
            if country_code:
                if not self.find_and_select_combo_box_option(self.address_country, country_code, "address country"):
                    logger.error("Failed to select address country")
                    return False
                time.sleep(0.5)
            
            # City
            if permanent_address_same == "1" or permanent_address_same == 1:
                city = self.passport_data.get('mailing_city', '')
            else:
                city = self.passport_data.get('permanent_city', '')
            
            if city:
                if not self.find_and_input_text(self.address_city, city, "address city"):
                    logger.error("Failed to input address city")
                    return False
                time.sleep(0.5)
            
            # State selection
            if permanent_address_same == "1" or permanent_address_same == 1:
                state = self.passport_data.get('mailing_state', '')
            else:
                state = self.passport_data.get('permanent_state', '')
            
            if state:
                if not self.find_and_select_option(self.address_state, state, "address state"):
                    logger.error("Failed to select address state")
                    return False
                time.sleep(0.5)
            
            # ZIP code
            if permanent_address_same == "1" or permanent_address_same == 1:
                zip_code = self.passport_data.get('mailing_zip', '')
            else:
                zip_code = self.passport_data.get('permanent_zip', '')
            
            if zip_code:
                if not self.find_and_input_text(self.address_zip, zip_code, "address ZIP"):
                    logger.error("Failed to input address ZIP")
                    return False
                time.sleep(0.5)
            
            # Click Add Address submit button
            if not self.find_and_click_button(self.add_address_submit, "Add Address submit button"):
                logger.error("Failed to click Add Address submit button")
                return False
            time.sleep(2)  # Wait 10 seconds after address submit
            
            # Check for errors after Add Address submit button click
            error_result = self.check_for_errors()
            if error_result:
                return error_result
            
            # Click Continue after address submission
            logger.info("Clicking Continue button after address submission...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button after address submission")
                return False
            time.sleep(2)
            
            # Check for errors after Continue button click
            error_result = self.check_for_errors()
            if error_result:
                return error_result
            
            # Fill place of birth country
            logger.info("Filling place of birth...")
            country_birth = self.passport_data.get('country_birth', '')
            if country_birth:
                if not self.find_and_select_combo_box_option(self.place_of_birth_country, country_birth, "place of birth country"):
                    logger.error("Failed to select place of birth country")
                    return False
                time.sleep(0.5)
            
            # State of birth (combo box with state code)
            state_birth = self.passport_data.get('state_birth', '')
            if state_birth:
                # Map state code to full state name for combo box
                state_code = state_birth.upper()
                state_name = self.state_mapping.get(state_code, state_birth)
                if state_name != state_birth:
                    logger.info(f"Converting state code '{state_birth}' to full name '{state_name}' for state of birth")
                
                # Use the new state-specific combo box function
                if not self.find_and_select_state_combo_box(self.state_of_birth, state_code, state_name, "state of birth"):
                    logger.error("Failed to select state of birth")
                    return False
                time.sleep(0.5)
            
            # City of birth
            city_birth = self.passport_data.get('city_birth', '')
            if city_birth:
                # Filter to allow only letters, numbers, apostrophes, hyphens, and periods
                city_birth = re.sub(r'[^a-zA-Z0-9\'-.\s]', '', city_birth)
                city_birth = re.sub(r'\s*,\s*', ' ', city_birth)
                if not self.find_and_input_text(self.city_of_birth, city_birth, "city of birth"):
                    logger.error("Failed to input city of birth")
                    return False
                time.sleep(0.5)
            
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
                time.sleep(0.5)
            
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
                        time.sleep(0.5)
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
                        time.sleep(0.5)
                except (ValueError, IndexError):
                    logger.warning(f"Invalid hair color index: {hair_color_index}")
            
            # Height feet
            height_ft = self.passport_data.get('height_ft', '')
            if height_ft:
                if not self.find_and_select_option(self.height_feet, str(height_ft), "height feet"):
                    logger.error("Failed to select height feet")
                    return False
                time.sleep(0.5)
            
            # Height inches
            height_in = self.passport_data.get('height_in', '')
            if height_in:
                if not self.find_and_select_option(self.height_inches, str(height_in), "height inches"):
                    logger.error("Failed to select height inches")
                    return False
                time.sleep(0.5)
            
            # Occupation
            occupation = self.passport_data.get('occupation', '')
            if occupation:
                occupation = re.sub(r'[^a-zA-Z0-9]', '', occupation)
                if not self.find_and_input_text(self.occupation, occupation, "occupation"):
                    logger.error("Failed to input occupation")
                    return False
                time.sleep(0.5)
            
            # Employer or school
            employer_or_school = self.passport_data.get('employer_or_school', '')
            if employer_or_school:
                employer_or_school = re.sub(r'[^a-zA-Z0-9]', '', employer_or_school)
                if not self.find_and_input_text(self.employer_or_school, employer_or_school, "employer or school"):
                    logger.error("Failed to input employer or school")
                    return False
                time.sleep(0.5)
            
            # Click Continue button
            logger.info("Clicking Continue button...")
            if not self.find_and_click_button(self.continue_button, "Continue button"):
                logger.error("Failed to click Continue button")
                page_code = self.get_page_name_code()
                return {
                    'status': False,
                    'code': f'{page_code}_BUTTON_CLICK_FAILED',
                    'message': 'We couldn\'t proceed with your request. Please try again.'
                }
            
            # Wait 2 seconds after clicking continue button
            logger.info("waiting 2 seconds after clicking Continue...")
            time.sleep(2)
            
            # Check for errors after final Continue button click
            logger.info("Checking for errors after clicking Continue...")
            error_result = self.check_for_page_errors()
            if error_result:
                return error_result
            
            logger.info("✅ Step 8 completed successfully - Personal information form submitted")
            return {
                'status': True,
                'code': 'SUCCESS',
                'message': 'Step 8 completed successfully - Personal information form submitted'
            }
            
        except Exception as e:
            logger.error(f"❌ Step 8 failed with error: {str(e)}")
            page_code = self.get_page_name_code()
            return {
                'status': False,
                'code': f'{page_code}_EXCEPTION',
                'message': 'We encountered an issue processing your personal information. Please try again.'
            }
