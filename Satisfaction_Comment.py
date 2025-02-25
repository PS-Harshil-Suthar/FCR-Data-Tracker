from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Set path to GeckoDriver (Update with your actual path)
geckodriver_path = "D:\\first_call_response_counter\\geckodriver.exe"  # Update with your actual path
# Firefox options
firefox_options = webdriver.FirefoxOptions()
# firefox_options.add_argument("--headless")  # Uncomment to run in headless mode

# Initialize service
service = Service(geckodriver_path)
driver = webdriver.Firefox(service=service, options=firefox_options)

# Open JIRA login page
driver.get("https://3eco.atlassian.net")  # Replace with your actual JIRA URL

# Wait for manual login
input("Log in to JIRA manually and press Enter to continue...")

# Wait until the page loads fully
time.sleep(5)

# Debug: Print page source to check if feedback elements are present
print(driver.page_source)

# Wait for feedback elements
try:
    feedback_elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid^="servicedesk-reports-satisfaction.ui.table.feedback-table--row-feedback"]'))
    )
except:
    print("⚠️ Timed out waiting for feedback elements to load.")
    feedback_elements = []

# Extract feedback data
feedback_data = [feedback.get_attribute("innerText") for feedback in feedback_elements]

# Check if we extracted data
if not feedback_data:
    print("⚠️ No satisfaction feedback found!")
else:
    print(f"✅ Extracted {len(feedback_data)} feedback entries.")

# Save feedback data to CSV
df = pd.DataFrame(feedback_data, columns=["Satisfaction Feedback"])
df.to_csv("satisfaction_feedback.csv", index=False, encoding="utf-8")

print("✅ Satisfaction feedback exported to 'satisfaction_feedback.csv'")

# Close the driver
driver.quit()
