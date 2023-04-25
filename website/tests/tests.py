# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytest
import time
from selenium.webdriver.common.action_chains import ActionChains


def test_login_invalid_email():
    # Open the browser
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    # Click on the login link in the navigation bar
    driver.find_element(By.XPATH, "//a[text()='Login']").click()

    # Fill in the login form with an invalid email
    driver.find_element(By.NAME, "email").send_keys(
        "invalid_email@example.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword")
    driver.find_element(By.NAME, "submitLogin").click()

    # Check that a flash message is displayed with the correct error message
    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "This account does not exist." in flash_message

    # Close the browser
    driver.close()


def test_login_wrong_credentials():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Login']").click()

    driver.find_element(By.NAME, "email").send_keys("iacobed2001@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword")
    driver.find_element(By.NAME, "submitLogin").click()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Wrong username or password." in flash_message

    driver.close()


# def test_register_and_redirect():
#     driver = webdriver.Chrome()
#     driver.get("http://127.0.0.1:5000")

#     driver.find_element(By.XPATH, "//a[text()='Register']").click()

#     driver.find_element(By.NAME, "firstName").send_keys("Test")
#     driver.find_element(By.NAME, "lastName").send_keys("Test")
#     driver.find_element(By.NAME, "email").send_keys("testuserrr@example.com")
#     driver.find_element(By.NAME, "password").send_keys("testpassword")
#     driver.find_element(By.NAME, "password2").send_keys("testpassword")
#     country = Select(driver.find_element(By.NAME, "country"))
#     time.sleep(2)
#     country.select_by_visible_text("Ireland")
#     gender = Select(driver.find_element(By.NAME, "gender"))
#     gender.select_by_visible_text("Male")

#     # Scroll to the bottom of the page to avoid virtual keyboard covering the button
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(1)  # wait for page to scroll

#     # Click the submit button using ActionChains
#     submit_button = driver.find_element(By.NAME, "submitRegister")
#     ActionChains(driver).move_to_element(submit_button).click().perform()

#     assert "Account created successfully!" in driver.page_source
#     assert driver.current_url == "http://127.0.0.1:5000/"

#     driver.close()
