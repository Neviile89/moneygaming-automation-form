import os
import shutil
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_registration_form():
    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--headless")  # Optional: Use headless mode for CI stability

    # Create a unique user data directory for each session
    unique_dir = f"/tmp/chrome_user_data_{os.getpid()}"
    options.add_argument(f"--user-data-dir={unique_dir}")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.110 Safari/537.36"
    )

    # WebDriver setup
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(120)
    driver.maximize_window()

    try:
        # Retry logic for loading the page
        retries = 3
        for attempt in range(retries):
            try:
                print(f"Attempt {attempt + 1} to load the page...")
                driver.get("https://moneygaming.qa.gameaccount.com/")
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(5)
        else:
            raise Exception("All attempts to load the page failed.")

        # Click the JOIN NOW button to open the registration page
        join_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "JOIN NOW!"))
        )
        join_now_button.click()

        # Wait for the registration form to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "form"))
        )

        # Fill out the form
        title_dropdown = Select(driver.find_element(By.ID, "title"))
        title_dropdown.select_by_visible_text("Mr")

        # Enter first and last names
        first_name_field = driver.find_element(By.ID, "forename")
        first_name_field.send_keys("John")

        surname_field = driver.find_element(By.NAME, "map(lastName)")
        surname_field.send_keys("Doe")

        # Agree to terms and conditions
        terms_checkbox = driver.find_element(By.NAME, "map(terms)")
        terms_checkbox.click()

        # Submit the form
        driver.find_element(By.ID, "form").submit()

        # Validate the error message under the date of birth box
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//label[@for='dob']//following-sibling::div[@class='error']",
                )
            )
        )

        assert error_message.text == "This field is required", "Error message does not match!"

    finally:
        # Close the browser and clean up the user data directory
        driver.quit()
        if os.path.exists(unique_dir):
            shutil.rmtree(unique_dir)


if __name__ == "__main__":
    test_registration_form()
