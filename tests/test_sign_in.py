#test_sig_in.py
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.sign_in_page import SignInPage
from config import EMAIL, PASSWORD

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

def test_sign_in_flow(driver):
    page = SignInPage(driver)
    page.load()
    # Element testing
    assert page.sign_in_flow(EMAIL, PASSWORD)




