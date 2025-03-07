# autoapply
# LinkedIn Auto Apply Bot

This script automates the process of applying for jobs on LinkedIn using Selenium. It continuously applies to all available "Easy Apply" jobs based on your specified job search criteria.

## Features
- Logs into LinkedIn automatically.
- Searches for jobs based on user-defined keywords and location.
- Applies to all "Easy Apply" jobs with a pre-uploaded resume.
- Runs indefinitely, continuously applying for new jobs.

## Requirements
### **Install Dependencies**
Ensure you have the following installed:

- **Python 3.x**
- **Google Chrome** (latest version)
- **ChromeDriver** (managed automatically)
- Required Python packages:

```sh
pip install selenium beautifulsoup4 webdriver-manager pymupdf
```

## Configuration
Before running the script, update the following settings in the script:

- **LinkedIn Login Credentials**
- **Path to Resume File**
- **Job Search Keywords**
- **Location Preference**

Example settings:

```python
LINKEDIN_EMAIL = "your_email@example.com"
LINKEDIN_PASSWORD = "your_password"
RESUME_PATH = "path/to/resume.pdf"
JOB_SEARCH_QUERY = "IT Manager"
LOCATION = "United States"
```

## How to Run
1. Clone the repository:

```sh
git clone https://github.com/yourusername/LinkedIn-AutoApply.git
cd LinkedIn-AutoApply
```

2. Run the script:

```sh
python auto_apply.py
```

## Notes
- This script runs indefinitely and refreshes job listings every 60 seconds.
- Ensure that LinkedIn does not flag your account for excessive automation.
- If an "Apply" button redirects to an external website, manual application may be required.

## Disclaimer
This script is for educational purposes only. Use at your own risk. Automating job applications on LinkedIn may violate their Terms of Service.

