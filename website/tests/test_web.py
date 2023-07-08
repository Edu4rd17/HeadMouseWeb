from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pytest
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def test_loginWrongCredentials():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Login']").click()

    driver.find_element(By.NAME, "email").send_keys("testlogin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword")

    # Scroll to the bottom of the page to avoid virtual keyboard covering the button
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element(By.NAME, "submitLogin").click()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Wrong username or password." in flash_message

    driver.close()


def test_loginInvalidEmail():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Login']").click()

    driver.find_element(By.NAME, "email").send_keys(
        "invaliddemail@example.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element(By.NAME, "submitLogin").click()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "This account does not exist." in flash_message

    driver.close()


def test_invalidPassword():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Register']").click()

    driver.find_element(By.NAME, "firstName").send_keys("Test")
    driver.find_element(By.NAME, "lastName").send_keys("Test")
    driver.find_element(By.NAME, "email").send_keys(
        "testuserrggsngfr@example.com")
    # Number 23 from the big list of naughty strings
    driver.find_element(By.NAME, "password").send_keys("\\")
    driver.find_element(By.NAME, "password2").send_keys("\\")
    country = Select(driver.find_element(By.NAME, "country"))
    time.sleep(3)
    country.select_by_visible_text("Ireland")
    gender = Select(driver.find_element(By.NAME, "gender"))
    gender.select_by_visible_text("Male")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # wait for page to scroll

    submit_button = driver.find_element(By.NAME, "submitRegister")
    ActionChains(driver).move_to_element(submit_button).click().perform()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Password must be at least 7 characters." in flash_message

    driver.close()


def test_firstnameFormat():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Register']").click()

    # Number 148 from the big list of naughty strings
    driver.find_element(By.NAME, "firstName").send_keys("åß∂ƒ©˙∆˚¬…æ")
    driver.find_element(By.NAME, "lastName").send_keys("Test")
    driver.find_element(By.NAME, "email").send_keys("example@yahoo.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword")
    driver.find_element(By.NAME, "password2").send_keys("testpassword")
    country = Select(driver.find_element(By.NAME, "country"))
    time.sleep(5)
    country.select_by_visible_text("Ireland")
    gender = Select(driver.find_element(By.NAME, "gender"))
    gender.select_by_visible_text("Male")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    submit_button = driver.find_element(By.NAME, "submitRegister")
    ActionChains(driver).move_to_element(submit_button).click().perform()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "First name should contain only letters." in flash_message

    driver.close()


def test_changePassword():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Login']").click()

    driver.find_element(By.NAME, "email").send_keys(
        "testuser@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("passwordtest")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    driver.find_element(By.NAME, "submitLogin").click()

    time.sleep(2)

    driver.find_element(By.XPATH, "//a[text()='Profile']").click()

    change_pass_btn = driver.find_element(By.ID, "change-pass-btn")
    change_pass_btn.click()

    # Update password
    driver.find_element(By.NAME, "currentPassword").send_keys("passwordtest")
    driver.find_element(By.NAME, "newPassword").send_keys("newpassword")
    driver.find_element(
        By.NAME, "confirmNewPassword").send_keys("newpassword")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element(By.NAME, "changePassword").click()

    # Verify password was updated
    flash_message = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "Password changed successfully!" in flash_message

    time.sleep(3)

    driver.find_element(By.XPATH, "//a[text()='Logout']").click()

    # Login with new password
    driver.find_element(By.XPATH, "//a[text()='Login']").click()
    driver.find_element(By.NAME, "email").send_keys(
        "testuser@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("newpassword")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    driver.find_element(By.NAME, "submitLogin").click()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-success").text
    assert "Logged in successfully!" in flash_message

    driver.close()


def test_passwordsMatch():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Register']").click()

    driver.find_element(By.NAME, "firstName").send_keys("Test")
    driver.find_element(By.NAME, "lastName").send_keys("Test")
    driver.find_element(By.NAME, "email").send_keys(
        "testuserrggsngfr@example.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword1")
    driver.find_element(By.NAME, "password2").send_keys("testpassword2")
    country = Select(driver.find_element(By.NAME, "country"))
    time.sleep(2)
    country.select_by_visible_text("Ireland")
    gender = Select(driver.find_element(By.NAME, "gender"))
    gender.select_by_visible_text("Male")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    submit_button = driver.find_element(By.NAME, "submitRegister")
    ActionChains(driver).move_to_element(submit_button).click().perform()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Passwords do not match." in flash_message

    driver.close()


def test_uniqueEmail():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Register']").click()

    driver.find_element(By.NAME, "firstName").send_keys("Test")
    driver.find_element(By.NAME, "lastName").send_keys("Test")
    driver.find_element(By.NAME, "email").send_keys("testlogin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword")
    driver.find_element(By.NAME, "password2").send_keys("testpassword")
    country = Select(driver.find_element(By.NAME, "country"))
    time.sleep(4)
    country.select_by_visible_text("Ireland")
    gender = Select(driver.find_element(By.NAME, "gender"))
    gender.select_by_visible_text("Male")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    submit_button = driver.find_element(By.NAME, "submitRegister")
    ActionChains(driver).move_to_element(submit_button).click().perform()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "This email is already linked to an account!" in flash_message

    driver.close()


def test_passwordEmptySpaces():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Register']").click()

    driver.find_element(By.NAME, "firstName").send_keys("Test")
    driver.find_element(By.NAME, "lastName").send_keys("Test")
    driver.find_element(By.NAME, "email").send_keys(
        "testuserrggsngfr@example.com")
    # Number 577 from the big list of naughty strings
    driver.find_element(By.NAME, "password").send_keys(
        "<i onwheel=alert(224)> Scroll over me </i>")
    driver.find_element(By.NAME, "password2").send_keys(
        "<i onwheel=alert(224)> Scroll over me </i>")
    country = Select(driver.find_element(By.NAME, "country"))
    time.sleep(4)
    country.select_by_visible_text("Ireland")
    gender = Select(driver.find_element(By.NAME, "gender"))
    gender.select_by_visible_text("Male")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    submit_button = driver.find_element(By.NAME, "submitRegister")
    ActionChains(driver).move_to_element(submit_button).click().perform()

    flash_message = driver.find_element(By.CLASS_NAME, "alert-danger").text
    assert "Password should not contain spaces." in flash_message

    driver.close()


def test_scrollDownButton():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    scroll_down_button = driver.find_element(By.ID, "scroll-down-button")
    scroll_down_button.click()

    time.sleep(1)

    scroll_position = driver.execute_script("return window.pageYOffset;")
    assert scroll_position == 200, "Page did not scroll down by 200 pixels."

    driver.close()


def test_scrollUpButton():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    # Scroll down the page first to create a scrolling context
    driver.execute_script("window.scrollTo(0, 500);")
    time.sleep(1)

    scroll_up_button = driver.find_element(By.ID, "scroll-up-button")
    scroll_up_button.click()

    time.sleep(1)

    # Get the current scroll position and check that it has changed
    current_scroll_position = driver.execute_script(
        "return window.pageYOffset;")
    assert current_scroll_position < 500

    driver.close()


def test_navigationBarLoggedIn():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Login']").click()

    driver.find_element(By.NAME, "email").send_keys(
        "testlogin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("passwordtest")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element(By.NAME, "submitLogin").click()
    # Check that the navigation bar contains the expected links
    expected_links = ['home', 'about us', 'profile', 'youtube', 'logout']
    actual_links = [link.text.lower()
                    for link in driver.find_elements(By.XPATH, "//nav//a")]
    assert set(expected_links) == set(actual_links)

    driver.close()


def test_navigationBarLoggedOut():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    # Check that the navigation bar contains the expected links
    expected_links = ['home', 'about us', 'login', 'register']
    actual_links = [link.text.lower() for link in driver.find_elements(
        By.XPATH, "//nav//a")]
    assert set(expected_links) == set(actual_links)

    driver.close()


def test_editProfile():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Login']").click()

    driver.find_element(By.NAME, "email").send_keys(
        "testlogin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("passwordtest")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    driver.find_element(By.NAME, "submitLogin").click()

    time.sleep(2)
    driver.find_element(By.XPATH, "//a[text()='Profile']").click()

    time.sleep(2)

    edit_details_btn = driver.find_element(By.ID, "edit-details-btn")
    edit_details_btn.click()

    # Edit profile information
    driver.find_element(By.NAME, "firstName").clear()
    driver.find_element(By.NAME, "firstName").send_keys("NewFirstName")
    driver.find_element(By.NAME, "lastName").clear()
    driver.find_element(By.NAME, "lastName").send_keys("NewLastName")
    country = Select(driver.find_element(By.NAME, "country"))
    time.sleep(4)
    country.select_by_visible_text("Ireland")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.find_element(By.NAME, "saveDetails").click()

    time.sleep(2)

    edit_details_btn = driver.find_element(By.ID, "edit-details-btn")
    edit_details_btn.click()

    # Verify changes were saved
    assert driver.find_element(By.NAME, "firstName").get_attribute(
        "value").lower() == "newfirstname"
    assert driver.find_element(By.NAME, "lastName").get_attribute(
        "value").lower() == "newlastname"

    driver.close()


def test_register_and_redirect():
    driver = webdriver.Chrome()
    driver.get("http://127.0.0.1:5000")

    driver.find_element(By.XPATH, "//a[text()='Register']").click()

    driver.find_element(By.NAME, "firstName").send_keys("Test")
    driver.find_element(By.NAME, "lastName").send_keys("Test")
    driver.find_element(By.NAME, "email").send_keys("newtestuser8@example.com")
    driver.find_element(By.NAME, "password").send_keys("testpassword")
    driver.find_element(By.NAME, "password2").send_keys("testpassword")
    country = Select(driver.find_element(By.NAME, "country"))
    time.sleep(2)
    country.select_by_visible_text("Ireland")
    gender = Select(driver.find_element(By.NAME, "gender"))
    gender.select_by_visible_text("Male")

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # Click the submit button using ActionChains
    submit_button = driver.find_element(By.NAME, "submitRegister")
    ActionChains(driver).move_to_element(submit_button).click().perform()

    time.sleep(2)
    assert "Account created successfully!" in driver.page_source
    assert driver.current_url == "http://127.0.0.1:5000/"

    driver.close()
