# import pytest
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from pages.sign_in_page import SignInPage
# import time
# from config import INVALID_EMAIL, INVALID_PASSWORD
# from config import EMAIL, PASSWORD


# # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# @pytest.fixture
# def driver():
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     yield driver
#     driver.quit()

# def test_login_fails_with_invalid_email(driver):
#     page = SignInPage(driver)
#     page.load()
#     page.login(INVALID_EMAIL, PASSWORD, remember=False)
#     # Wait for error message or failed login indication
#     assert page.is_invalid_credentials_alert_present()
#     time.sleep(2)

# def test_login_fails_with_invalid_password(driver):
#     page = SignInPage(driver)
#     page.load()
#     page.login(EMAIL, INVALID_PASSWORD, remember=False)
#     # Wait for error message or failed login indication
#     assert page.is_invalid_credentials_alert_present()
#     time.sleep(2)
