import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to take a screenshot of the webpage
def take_screenshot(driver, file_name):
    driver.save_screenshot(os.path.join("D:\\Documents\\Walsh\\IT_414\\IT414_Jschalte\\IT414_Jschalte\\Week_4\\images", file_name))

# Function to rename the screenshot with prefix passed_ or failed_
def rename_screenshot(filename, passed=True):
    basename, ext = os.path.splitext(filename)
    prefix = "passed_" if passed else "failed_"
    new_filename = f"{prefix}{basename}"
    os.rename(os.path.join("D:\\Documents\\Walsh\\IT_414\\IT414_Jschalte\\IT414_Jschalte\\Week_4\\images", filename), os.path.join("D:\\Documents\\Walsh\\IT_414\\IT414_Jschalte\\IT414_Jschalte\\Week_4\\images", new_filename))

# Function to validate the contact form
def validate_form(driver):
    # Fill in form fields
    first_name = driver.find_element(By.ID, "firstName")
    first_name.clear()
    first_name.send_keys("Jon")
    last_name = driver.find_element(By.ID, "lastName")  
    last_name.clear()
    last_name.send_keys("Doe")
    email_address = driver.find_element(By.ID, "emailAddress")  
    email_address.clear()
    email_address.send_keys("")  # Empty email address
    phone_number = driver.find_element(By.ID, "phoneNumber")  
    phone_number.clear()
    phone_number.send_keys("1234567890")

    # Take a screenshot of the form with filled values
    take_screenshot(driver, "initial_form_with_values.png")

    # Click the submit button
    submit_button = driver.find_element(By.ID, "my_submit")
    submit_button.click()

    # Wait for error messages or success message
    try:
        # Wait for success message to become visible
        success_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "alert-success"))
        )
        # Take a screenshot of the success message
        take_screenshot(driver, "success.png")
        rename_screenshot("success.png")
    except:
        # Take a screenshot of failed validation
        take_screenshot(driver, "form_validation.png")
        if os.path.exists(os.path.join("D:\\Documents\\Walsh\\IT_414\\IT414_Jschalte\\IT414_Jschalte\\Week_4\\images", "form_validation.png")):
            rename_screenshot("form_validation.png", passed=False)
        take_screenshot(driver, "failed_validation.png")
        rename_screenshot("failed_validation.png", passed=False)
        print("Validation failed. Please interact with the page to correct.")
        # Wait indefinitely until the user interacts with the page
        driver.execute_script("document.querySelector('.form-signin').addEventListener('click', function(){})")
        print("Interaction detected. Refreshing the page.")
        time.sleep(8)  # Wait for 8 seconds before retrying
        driver.refresh()  # Refresh the page
        # Adding a delay for refreshing
        time.sleep(5)

def main():
    # Set up Selenium webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    # Open the website
    driver.get("https://ool-content.walshcollege.edu/CourseFiles/IT/IT414/MASTER/Week04/WI20-website-testing-sites/assignment/index.php")

    # Take a screenshot of the initial form
    take_screenshot(driver, "initial_form.png")

    # Validate the form
    validate_form(driver)

    # Wait for a few seconds before closing the browser
    time.sleep(5)

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    main()

