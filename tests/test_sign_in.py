#test_sig_in.py
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.sign_in_page import SignInPage
email= "tmeraslan1@gmail.com"
password= "r_ATzrCF9NFjMCF123"

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

def test_sign_in_flow(driver):
    page = SignInPage(driver)
    page.load()
    # בדיקת אלמנטים
    assert page.is_sign_in_text_present()
    assert page.is_sign_in_button_present()
    assert page.is_email_input_present()
    assert page.is_password_input_present()
    assert page.is_remember_label_present()
    assert page.is_remember_checkbox_present()

    # ביצוע התחברות
    page.login(email, password, remember=True)

    #בדיקת הצלחה
    assert page.is_logged_in_successfully()


