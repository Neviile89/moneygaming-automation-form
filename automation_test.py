from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def test_registration_form():
    # Set Chrome options to run headlessly
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")  # Disable sandboxing for CI environments
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode
    chrome_options.add_argument("--disable-dev-shm-usage")  # Fix potential memory issues
    chrome_options.add_argument("--remote-debugging-port=9222")  # Enable debugging port (optional)

    # Force the use of ChromeDriver 114 despite version mismatch
    chrome_options.add_argument('--disable-software-rasterizer')  # Disable GPU rasterization

    # Initialize the WebDriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()

    try:
        # Navigating to the website
        driver.get("https://moneygaming.qa.gameaccount.com/")

        # Click the JOIN NOW button to open the registration page
        join_now_button = driver.find_element(By.LINK_TEXT, "JOIN NOW!")
        join_now_button.click()

        # Wait until the form is loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "form"))
        )

        # Selecting title
        title_dropdown = Select(driver.find_element(By.ID, "title"))
        title_dropdown.select_by_visible_text("Mr")  # You can replace "Mr" with another value if needed

        # Filling in first and surname
        first_name_field = driver.find_element(By.ID, "forename")
        first_name_field.send_keys("John")

        surname_field = driver.find_element(By.NAME, "map(lastName)")
        surname_field.send_keys("Doe")

        # Agree to terms and conditions
        terms_checkbox = driver.find_element(By.NAME, "map(terms)")
        terms_checkbox.click()

        # Submit the form by clicking the JOIN NOW button
        join_now_button = driver.find_element(By.ID, "form")
        join_now_button.submit()

        # Wait for the error message under the date of birth box to appear
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[@for='dob']//following-sibling::div[@class='error']"))
        )

        # Verify that the error message is correct
        assert error_message.text == "This field is required", "Error message does not match!"

    finally:
        driver.quit()

if __name__ == "__main__":
    test_registration_form()
