# Passport Renewal Automation

A Python-based web automation framework using Undetected ChromeDriver for automating passport renewal applications through the U.S. Department of State's Online Passport Renewal (OPR) system.

## Features

- **Undetected Automation**: Uses undetected_chromedriver to avoid detection
- **Continuous Processing**: Runs in an infinite loop, continuously checking for new applications
- **Single Application Workflow**: Fetches and processes one application at a time from the API
- **Smart Waiting**: Automatically waits 60 seconds when no applications are available
- **Error Handling**: Comprehensive logging and error management with backend status updates
- **Step-by-Step Execution**: 15 automated steps covering the entire renewal process (including payment)
- **Backend Integration**: Automatic status updates via REST API
- **Failure Handling**: Stops processing and reports errors for failed applications

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Chrome Browser**: Make sure you have Google Chrome installed on your system.

3. **Environment Variables**: Create a `.env` file in the project root with the following variables:
   ```env
   # API endpoint for both fetching passport data and updating status
   API_ENDPOINT=https://your-backend-api.com/api/passport-applications
   ```

## Quick Start

### Running the Automation

```bash
# Run the main automation script
python main.py
```

The script will:
1. Set up ChromeDriver and navigate to the OPR website once
2. Run in a continuous loop:
   - Fetch a single passport application from the backend API
   - If no application available, wait 60 seconds and check again
   - Process the application through all 15 steps
   - Update the backend with appropriate status (success or failure)
   - Navigate back to the start page for the next application
3. Continue until manually stopped (Ctrl+C)

### Automation Steps

The automation executes the following steps for each application:

1. Landing Page
2. What You Need
3. Eligibility Requirements
4. Upcoming Travel
5. Terms and Conditions
6. What Are You Renewing
7. Passport Photo Upload
8. Personal Information
9. Emergency Contact
10. Passport Options
11. Mailing Address
12. Passport Delivery
13. Review Order
14. Statement of Truth
15. Payment

## Backend API Integration

### Data Fetch API

The script continuously fetches passport applications from the backend in a loop.

**Endpoint**: `API_ENDPOINT`  
**Method**: `GET`

**Expected Response**:
```json
{
  "data": [
    {
      "id": "12312",
      "data": "{...passport application data as JSON string...}"
    }
  ]
}
```

**Behavior**:
- The script fetches **one application at a time** (first item in the array)
- If `data` array is empty or no applications available, the script waits 60 seconds before checking again
- After processing, the script fetches the next application

### Status Update API

After processing each application, the script automatically updates the backend with the application status.

**Endpoint**: `API_ENDPOINT`  
**Method**: `POST`

**Request Body (Success)**:
```json
{
  "id": "12312",
  "renewal_status": "5"
}
```

**Request Body (Failure in Steps 1-14)**:
```json
{
  "id": "12312",
  "renewal_status": "2",
  "renewal_error": "{\"code\": \"TRAVEL_PLANS_ERROR\", \"message\": \"Your travel is before the expected arrival of your new passport.\"}"
}
```

**Request Body (Failure in Step 15 - Payment)**:
```json
{
  "id": "12312",
  "renewal_status": "3",
  "renewal_error": "{\"code\": \"PAYMENT_ERROR\", \"message\": \"Payment processing failed.\"}"
}
```

**Status Codes**:
- `"2"` - Application failed in steps 1-14 (error details provided in `renewal_error`)
- `"3"` - Application failed in step 15 (Payment) (error details provided in `renewal_error`)
- `"5"` - Application completed successfully

**Error Codes**:
- `TRAVEL_PLANS_ERROR` - Travel date conflicts detected
- `CONTINUE_BUTTON_NOT_FOUND` - UI element not found
- `CONTINUE_BUTTON_DISABLED` - Form validation failed
- `STEP_FAILED` - Generic step failure
- `APPLICATION_EXCEPTION` - Unexpected error during processing
- `PAYMENT_ERROR` - Payment processing failed

## Error Handling and Flow Control

### Step Failure Behavior

When any step fails during processing:
1. The error code and message are captured from the step result
2. Processing stops immediately for that application (remaining steps are skipped)
3. The backend is notified via POST to `API_ENDPOINT` with:
   - For failures in steps 1-14: `renewal_status`: `"2"` (failed)
   - For failures in step 15 (Payment): `renewal_status`: `"3"` (payment failed)
   - `renewal_error`: JSON string containing `code` and `message`
4. The script navigates back to the start page and fetches the next application

### Success Behavior

When all 15 steps complete successfully:
1. The backend is notified via POST to `API_ENDPOINT` with:
   - `renewal_status`: `"5"` (success)
   - No `renewal_error` field
2. The script navigates back to the start page and fetches the next application

### No Data Available Behavior

When no application data is available from the API:
1. The script logs "No application data available from API"
2. Waits 60 seconds
3. Checks the API again for new applications
4. Continues this cycle until new data is available or the script is stopped (Ctrl+C)

## Required Data Fields in API Response

The passport application data must include the following fields:

### Personal Information Fields
Standard fields like `first_name`, `last_name`, `email`, address fields, etc.

### Photo URL (Required)
- **Field**: `photo_url`
- **Type**: String (URL)
- **Description**: Direct URL to the passport photo image
- **Supported formats**: JPEG, JPG, PNG
- **Example**: `"https://example.com/photos/passport-photo.jpg"`
- **Behavior**: The script will download the photo from this URL and upload it in Step 7

### Billing Information (Required)
- **Field**: `billing_info`
- **Type**: Object or JSON string
- **Description**: Payment/billing information for Step 15 (Payment)
- **Required subfields**:
  - `cardholder_name`: Full name on the card (e.g., "John Smith")
  - `cc_number`: Credit card number without spaces (e.g., "4111111111111111")
  - `cc_exp_month`: Expiration month as number (e.g., "8" for August)
  - `cc_exp_year`: Expiration year last 2 digits (e.g., "30" for 2030)
  - `cc_cvv`: Security code (e.g., "123")
  - `payment_option`: Card type value as string (e.g., "3" for American Express)
    - "0" = Visa
    - "1" = Mastercard  
    - "2" = Discover
    - "3" = American Express
    - Note: The script automatically adds +1 to skip the "Select" placeholder option in the dropdown

**Example billing_info object**:
```json
{
  "cardholder_name": "John Smith",
  "cc_number": "376743655814011",
  "cc_exp_month": "8",
  "cc_exp_year": "30",
  "cc_cvv": "1345",
  "payment_option": "3"
}
```

**Payment Option Mapping:**
- `"0"` → Visa (dropdown index 1)
- `"1"` → Mastercard (dropdown index 2)
- `"2"` → Discover (dropdown index 3)
- `"3"` → American Express (dropdown index 4)

### Step Result Format

Each step can return either:
- **Boolean**: `True` for success, `False` for failure
- **Dictionary**: 
  ```python
  {
    'status': bool,      # True/False
    'code': str,         # Error code or 'SUCCESS'
    'message': str       # Descriptive message
  }
  ```

## Troubleshooting

### Common Issues

1. **API_ENDPOINT not found**: Ensure you have created a `.env` file with the `API_ENDPOINT` variable.

2. **Backend API connection failed**: 
   - Verify the endpoint URLs in `.env` are correct
   - Check network connectivity
   - Ensure the backend API is running and accessible

3. **ChromeDriver version mismatch**: The script automatically downloads ChromeDriver, but ensure:
   - You have internet access
   - Google Chrome is installed and up-to-date
   - The script has permission to download files

4. **Step failures**: 
   - Check the logs for specific error codes and messages
   - Verify the passport data format matches the expected structure
   - Ensure all required fields are provided in the application data

5. **Browser crashes**: 
   - Check available system memory
   - Update Chrome browser to the latest version
   - Try running with fewer concurrent applications

### Debug Mode

The script uses Python's logging module. Logs are output to the console with timestamps and log levels. Key information includes:
- Step execution status
- Error codes and messages
- API request/response status
- Application processing results

## File Structure

```
├── main.py                          # Main automation script
├── passport_data.json              # Sample passport data (for testing)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .env                           # Environment variables (not in repo)
└── steps/                         # Step implementations
    ├── __init__.py
    ├── base_step.py               # Base class for all steps
    ├── step1_landing_page.py      # Step 1: Landing Page
    ├── step2_what_you_need.py     # Step 2: What You Need
    ├── step3_eligibility_requirements.py  # Step 3: Eligibility
    ├── step4_upcoming_travel.py   # Step 4: Upcoming Travel
    ├── step5_terms_and_conditions.py      # Step 5: Terms
    ├── step6_what_are_you_renewing.py     # Step 6: What Are You Renewing
    ├── step7_passport_photo.py    # Step 7: Passport Photo Upload
    ├── step8_personal_information.py      # Step 8: Personal Information
    ├── step9_emergency_contact.py # Step 9: Emergency Contact
    ├── step10_passport_options.py # Step 10: Passport Options
    ├── step11_mailing_address.py  # Step 11: Mailing Address
    ├── step12_passport_delivery.py        # Step 12: Passport Delivery
    ├── step13_review_order.py     # Step 13: Review Order
    └── step14_statement_of_truth.py       # Step 14: Statement of Truth
```

## Key Features

### Multi-Application Processing
- Processes multiple passport applications sequentially
- Maintains browser session between applications
- Automatic navigation back to start for next application

### Robust Error Handling
- Captures specific error codes and messages from each step
- Stops processing on first failure
- Reports detailed error information to backend
- Continues with next application after failure

### Backend Integration
- Fetches application data from REST API
- Updates application status after each application
- Sends detailed error information for failed applications
- Confirms successful completion for passed applications
