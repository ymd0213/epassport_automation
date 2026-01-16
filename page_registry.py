"""
Page Registry Module
Maps detected page keys to their corresponding step classes
"""

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


class PageRegistry:
    """Registry mapping page keys to step classes and their configurations"""
    
    def __init__(self):
        """Initialize the page registry with all step mappings"""
        
        # Define the step sequence
        self.step_sequence = [
            'step1_landing',
            'step2_what_you_need',
            'step3_eligibility',
            'step4_upcoming_travel',
            'step5_terms',
            'step6_renewing',
            'step7_photo',
            'step8_personal_info',
            'step9_emergency_contact',
            'step10_passport_options',
            'step11_mailing_address',
            'step12_delivery',
            'step13_review',
            'step14_statement',
            'step15_payment',
            'confirmation'
        ]
        
        # Map page keys to step configurations
        self.page_map = {
            'step1_landing': {
                'num': 1,
                'name': 'Landing Page',
                'class': Step1LandingPage,
                'requires_data': False
            },
            'step2_what_you_need': {
                'num': 2,
                'name': 'What You Need',
                'class': Step2WhatYouNeed,
                'requires_data': False
            },
            'step3_eligibility': {
                'num': 3,
                'name': 'Eligibility Requirements',
                'class': Step3EligibilityRequirements,
                'requires_data': False
            },
            'step4_upcoming_travel': {
                'num': 4,
                'name': 'Upcoming Travel',
                'class': Step4UpcomingTravel,
                'requires_data': True
            },
            'step5_terms': {
                'num': 5,
                'name': 'Terms and Conditions',
                'class': Step5TermsAndConditions,
                'requires_data': False
            },
            'step6_renewing': {
                'num': 6,
                'name': 'What Are You Renewing',
                'class': Step6WhatAreYouRenewing,
                'requires_data': True
            },
            'step7_photo': {
                'num': 7,
                'name': 'Passport Photo Upload',
                'class': Step7PassportPhoto,
                'requires_data': True
            },
            'step8_personal_info': {
                'num': 8,
                'name': 'Personal Information',
                'class': Step8PersonalInformation,
                'requires_data': True
            },
            'step9_emergency_contact': {
                'num': 9,
                'name': 'Emergency Contact',
                'class': Step9EmergencyContact,
                'requires_data': True
            },
            'step10_passport_options': {
                'num': 10,
                'name': 'Passport Options',
                'class': Step10PassportOptions,
                'requires_data': True
            },
            'step11_mailing_address': {
                'num': 11,
                'name': 'Mailing Address',
                'class': Step11MailingAddress,
                'requires_data': True
            },
            'step12_delivery': {
                'num': 12,
                'name': 'Passport Delivery',
                'class': Step12PassportDelivery,
                'requires_data': True
            },
            'step13_review': {
                'num': 13,
                'name': 'Review Order',
                'class': Step13ReviewOrder,
                'requires_data': True
            },
            'step14_statement': {
                'num': 14,
                'name': 'Statement of Truth',
                'class': Step14StatementOfTruth,
                'requires_data': True
            },
            'step15_payment': {
                'num': 15,
                'name': 'Payment',
                'class': Step15Payment,
                'requires_data': True
            },
            'confirmation': {
                'num': 16,
                'name': 'Confirmation',
                'class': None,  # No processing needed for confirmation
                'requires_data': False
            }
        }
    
    def get_step_config(self, page_key):
        """
        Get step configuration for a given page key
        
        Args:
            page_key: The page key to look up
            
        Returns:
            dict: Step configuration or None if not found
        """
        return self.page_map.get(page_key)
    
    def get_step_instance(self, page_key, driver, data=None):
        """
        Create a step instance for the given page key
        
        Args:
            page_key: The page key to create instance for
            driver: Selenium WebDriver instance
            data: Passport data (required for some steps)
            
        Returns:
            Step instance or None if page not found or is confirmation
        """
        config = self.get_step_config(page_key)
        
        if not config or not config['class']:
            return None
        
        # Create instance based on whether it requires data
        if config['requires_data']:
            return config['class'](driver, data)
        else:
            return config['class'](driver)
    
    def get_next_expected_page(self, current_page_key):
        """
        Get the next expected page in the sequence
        
        Args:
            current_page_key: Current page key
            
        Returns:
            str: Next page key or None if at end
        """
        try:
            current_index = self.step_sequence.index(current_page_key)
            if current_index < len(self.step_sequence) - 1:
                return self.step_sequence[current_index + 1]
        except ValueError:
            pass
        
        return None
    
    def get_step_number(self, page_key):
        """
        Get the step number for a page key
        
        Args:
            page_key: The page key
            
        Returns:
            int: Step number or None if not found
        """
        config = self.get_step_config(page_key)
        return config['num'] if config else None
    
    def get_step_name(self, page_key):
        """
        Get the step name for a page key
        
        Args:
            page_key: The page key
            
        Returns:
            str: Step name or None if not found
        """
        config = self.get_step_config(page_key)
        return config['name'] if config else None
