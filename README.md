# Passport Renewal Automation

A Python-based web automation framework using Undetected ChromeDriver for automating passport renewal applications through the U.S. Department of State's Online Passport Renewal (OPR) system.

## Features

- **Undetected Automation**: Uses undetected_chromedriver to avoid detection
- **Multi-Application Processing**: Process multiple passport applications in sequence
- **Error Handling**: Comprehensive logging and error management with backend status updates
- **Step-by-Step Execution**: 14 automated steps covering the entire renewal process
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
1. Fetch passport applications from the backend API (first 5)
2. Process each application through all 14 steps
3. Stop processing if any step fails and update the backend with error details
4. Update the backend with success status if all steps pass
5. Move to the next application

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

## Backend API Integration

### Status Update API

After processing each application, the script automatically updates the backend with the application status.

**Endpoint**: `API_ENDPOINT`  
**Method**: `POST`

**Request Body (Success)**:
```json
{
  "id": "12312",
  "renewal_status": "2"
}
```

**Request Body (Failure)**:
```json
{
  "id": "12312",
  "renewal_status": "1",
  "renewal_error": "{\"code\": \"TRAVEL_PLANS_ERROR\", \"message\": \"Your travel is before the expected arrival of your new passport.\"}"
}
```

**Status Codes**:
- `"1"` - Application failed (error details provided in `renewal_error`)
- `"2"` - Application completed successfully

**Error Codes**:
- `TRAVEL_PLANS_ERROR` - Travel date conflicts detected
- `CONTINUE_BUTTON_NOT_FOUND` - UI element not found
- `CONTINUE_BUTTON_DISABLED` - Form validation failed
- `STEP_FAILED` - Generic step failure
- `APPLICATION_EXCEPTION` - Unexpected error during processing

### Data Fetch API

The script fetches passport applications from the backend at startup.

**Endpoint**: `API_ENDPOINT`  
**Method**: `GET`

**Expected Response**:
```json
{
  "data": [
    {
      "id": "12312",
      "data": "{...passport application data as JSON string...}"
    },
    ...
  ]
}
```

## Error Handling and Flow Control

### Step Failure Behavior

When any step fails during processing:
1. The error code and message are captured from the step result
2. Processing stops immediately for that application (remaining steps are skipped)
3. The backend is notified via POST to `API_ENDPOINT` with:
   - `renewal_status`: `"1"` (failed)
   - `renewal_error`: JSON string containing `code` and `message`
4. The automation moves to the next application in the queue

### Success Behavior

When all 14 steps complete successfully:
1. The backend is notified via POST to `API_ENDPOINT` with:
   - `renewal_status`: `"2"` (success)
   - No `renewal_error` field
2. The automation moves to the next application in the queue

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
