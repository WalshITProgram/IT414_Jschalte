import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image

def take_screenshot(driver, filename):
    """Take screenshot of the current window."""
    driver.save_screenshot(filename)

def rename_screenshot(filename, passed=True):
    """Rename the screenshot with prefix passed_ or failed_."""
    basename, ext = os.path.splitext(filename)
    if passed:
        new_filename = f"passed_{basename}{ext}"
    else:
        new_filename = f"failed_{basename}{ext}"
    os.rename(filename, new_filename)

def validate_form(driver):
    """Validate the contact form."""
    # Fill in form fields
    first_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "firstName")))
    first_name.clear()
    first_name.send_keys("Jo")  # Less than 3 characters, should fail
    last_name = driver.find_element_by_id("lastName")
    last_name.clear()
    last_name.send_keys("Doe")
    email_address = driver.find_element_by_xpath("//input[@id='emailAddress']")  # Using XPath to locate email input field
    email_address.clear()
    email_address.send_keys("invalidemail")  # Invalid email format, should fail
    phone_number = driver.find_element_by_id("phoneNumber")
    phone_number.clear()
    phone_number.send_keys("1234567890")

    # Take screenshot before submitting
    take_screenshot(driver, "images/before_submit.png")

    # Submit form
    submit_button = driver.find_element_by_id("submitButton")
    submit_button.click()

    # Wait for error messages or success message
    try:
        # Wait for either error message or success message
        error_message = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "text-danger"))
        )
        # Take screenshot of error message
        take_screenshot(driver, "images/error_message.png")
        rename_screenshot("images/error_message.png", passed=False)
    except:
        # If no error message found, assume success message
        take_screenshot(driver, "images/success.png")
        rename_screenshot("images/success.png")
    finally:
        driver.quit()

def main():
    # Set up Selenium webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Open the website
    driver.get("https://ool-content.walshcollege.edu/CourseFiles/IT/IT414/MASTER/Week04/WI20-website-testing-sites/assignment/index.php")

    # Validate the form
    validate_form(driver)

if __name__ == "__main__":
    main()
