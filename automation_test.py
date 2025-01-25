from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

def test_registration_form():
    # Set Chrome options to specify a unique user data directory
    options = webdriver.ChromeOptions()
    user_data_dir = os.path.join(os.getcwd(), "user-data-dir")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # Web driver
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        # Navigating to the website
        driver.get("https://moneygaming.qa.gameaccount.com/")

        # Click the JOIN NOW button to open the registration page
        join_now_button = driver.find_element(By.LINK_TEXT, "JOIN NOW!")
        join_now_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "form"))
        )

        title_dropdown = Select(driver.find_element(By.ID, "title"))
        title_dropdown.select_by_visible_text("Mr")  # I have to replace "Mr" with desired value if needed (check again)

        # first and surname
        first_name_field = driver.find_element(By.ID, "forename")
        first_name_field.send_keys("John")

        surname_field = driver.find_element(By.NAME, "map(lastName)")
        surname_field.send_keys("Doe")

        terms_checkbox = driver.find_element(By.NAME, "map(terms)")
        terms_checkbox.click()

        # Submit the form by clicking the JOIN NOW button
        join_now_button = driver.find_element(By.ID, "form")
        join_now_button.submit()

        # Have to validate the error message under the date of birth box
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='dob']//following-sibling::div[@class='error']"))
        )

        assert error_message.text == "This field is required", "Error message does not match!"

    finally:
        driver.quit()

if __name__ == "__main__":
    test_registration_form()

    # Just testing to trigger the CI pipeline
    # And a second test to trigger the CI pipeline (just to be sure it works)
    # Third test to trigger the CI pipeline
    # Still trying to create a proper pull request
    # Changed the test branch, now it should work
