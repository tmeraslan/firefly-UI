import unittest
import tempfile
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.sign_in_page import SignInPage
from config import INVALID_EMAIL, INVALID_PASSWORD, EMAIL, PASSWORD


class TestSignInFails(unittest.TestCase):

    def setUp(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("window-size=1920,1080")

        # צור תיקיית פרופיל זמנית ל-user data
        self.user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
        options.add_argument(f"--user-data-dir={self.user_data_dir}")

        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()
        shutil.rmtree(self.user_data_dir, ignore_errors=True)

    def test_login_fails_with_invalid_email(self):
        page = SignInPage(self.driver)
        page.load()
        page.login(INVALID_EMAIL, PASSWORD, remember=False)
        self.assertTrue(page.is_invalid_credentials_alert_present())
        time.sleep(2)

    def test_login_fails_with_invalid_password(self):
        page = SignInPage(self.driver)
        page.load()
        page.login(EMAIL, INVALID_PASSWORD, remember=False)
        self.assertTrue(page.is_invalid_credentials_alert_present())
        time.sleep(2)


if __name__ == "__main__":
    unittest.main()
