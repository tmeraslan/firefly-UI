import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.sign_in_page import SignInPage
import time
from config import INVALID_EMAIL, INVALID_PASSWORD
from config import EMAIL, PASSWORD
from selenium.webdriver.chrome.options import Options
import tempfile
import shutil


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # צור תיקיית פרופיל זמנית ל-user data
    user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)
    options.add_argument("window-size=1920,1080")
    yield driver

    driver.quit()

    # מחק את תיקיית הפרופיל אחרי סגירת הדרייבר
    shutil.rmtree(user_data_dir, ignore_errors=True)

def test_login_fails_with_invalid_email(driver):
    page = SignInPage(driver)
    page.load()
    page.login(INVALID_EMAIL, PASSWORD, remember=False)
    # Wait for error message or failed login indication
    assert page.is_invalid_credentials_alert_present()
    time.sleep(2)

def test_login_fails_with_invalid_password(driver):
    page = SignInPage(driver)
    page.load()
    page.login(EMAIL, INVALID_PASSWORD, remember=False)
    # Wait for error message or failed login indication
    assert page.is_invalid_credentials_alert_present()
    time.sleep(2)
