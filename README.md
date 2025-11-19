# Passport Renewal Automation

Automated passport renewal application processing using Undetected ChromeDriver.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your API endpoint:
   ```env
   API_ENDPOINT=https://your-backend-api.com/api/passport-applications
   ```

## Running the Script

### Basic Usage

```bash
python main.py
```

The script will:
- Continuously fetch passport applications from the API
- Process each application through all 15 steps
- Update the backend with success/failure status
- Run until manually stopped (Ctrl+C)

### Command Line Options

```bash
# Process normal applications (default)
python main.py --method normal

# Process failed applications with specific error code
python main.py --method failed --error-code STEP6_ERROR
```

## Requirements

- Python 3.x
- Google Chrome browser installed
- Internet connection
- Backend API endpoint configured in `.env`
