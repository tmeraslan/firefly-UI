#test_sig_in.py
import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.sign_in_page import SignInPage
from config import EMAIL, PASSWORD
from selenium.webdriver.chrome.options import Options
import tempfile
import shutil


@pytest.fixture
def driver():
    options = Options()
    # options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # צור תיקיית פרופיל זמנית ל-user data
    user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver

    driver.quit()

    # מחק את תיקיית הפרופיל אחרי סגירת הדרייבר
    shutil.rmtree(user_data_dir, ignore_errors=True)

def test_sign_in_flow(driver):
    page = SignInPage(driver)
    page.load()
    # Element testing
    assert page.sign_in_flow(EMAIL, PASSWORD)




