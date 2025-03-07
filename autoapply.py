import os
import time
import fitz  # PyMuPDF for PDFs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# ======= CONFIGURE THESE SETTINGS =======
LINKEDIN_EMAIL = "EmaiL Here"
LINKEDIN_PASSWORD = "Password Here"
RESUME_PATH = "resume.pdf"  # Ensure this is the correct path
JOB_SEARCH_QUERY = "IT Manager"
LOCATION = "United States"
# ========================================

# Function to initialize Selenium WebDriver
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in the background
    options.add_argument("--disable-blink-features=AutomationControlled")

    service = Service(ChromeDriverManager().install())  # Auto-downloads latest ChromeDriver
    driver = webdriver.Chrome(service=service, options=options)  # Use Service object
    return driver

# Function to log into LinkedIn
def login_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)
    
    try:
        driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
        driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD, Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        print(f"❌ LinkedIn login failed: {e}")
        driver.quit()
        exit()

# Function to extract Easy Apply job listings
def extract_job_descriptions(driver):
    job_url = f"https://www.linkedin.com/jobs/search/?keywords={JOB_SEARCH_QUERY.replace(' ', '%20')}&location={LOCATION.replace(' ', '%20')}&f_AL=true&f_EA=true"
    driver.get(job_url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    job_cards = soup.find_all("a", class_="base-card__full-link")

    jobs = []
    for card in job_cards:  # Get all Easy Apply jobs
        job_link = card["href"]
        jobs.append(job_link)
    
    return jobs

# Function to auto-submit applications
def auto_apply(driver):
    while True:
        jobs = extract_job_descriptions(driver)

        for job_link in jobs:
            print(f"Applying to: {job_link}")
            driver.get(job_link)
            time.sleep(3)

            try:
                # Scroll to ensure Easy Apply button is visible
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # Locate Easy Apply button
                easy_apply_button = None
                possible_selectors = [
                    "//button[contains(text(), 'Easy Apply')]",
                    "//button[contains(text(), 'Apply Now')]",
                    "//button[contains(@class, 'jobs-apply-button')]"
                ]

                for selector in possible_selectors:
                    try:
                        easy_apply_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        if easy_apply_button:
                            break  # Stop searching once we find the button
                    except:
                        continue

                if easy_apply_button:
                    easy_apply_button.click()
                    time.sleep(2)

                    # Upload resume
                    upload_button = driver.find_element(By.XPATH, "//input[@type='file']")
                    upload_button.send_keys(os.path.abspath(RESUME_PATH))
                    time.sleep(2)

                    # Click "Submit Application"
                    submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit application')]")
                    submit_button.click()
                    time.sleep(2)

                    print(f"✅ Successfully applied for {job_link}")
                else:
                    print(f"⚠️ No Easy Apply button found for {job_link}")

            except Exception as e:
                print(f"❌ Error applying for {job_link}: {e}")
        
        print("🔄 Refreshing job search and continuing...")
        time.sleep(60)  # Wait before reloading job listings

# Main execution
if __name__ == "__main__":
    driver = init_driver()
    login_linkedin(driver)
    auto_apply(driver)
    driver.quit()
