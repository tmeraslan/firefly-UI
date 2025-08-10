import unittest
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.sign_in_page import SignInPage
from config import EMAIL, PASSWORD

class TestSignInFlow(unittest.TestCase):
    def setUp(self):
        options = Options()
        # options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # צור תיקיית פרופיל זמנית ל-user data
        self.user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
        options.add_argument(f"--user-data-dir={self.user_data_dir}")

        # חשוב להוסיף את ה-window-size לפני יצירת הדרייבר
        options.add_argument("window-size=1920,1080")

        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()
        shutil.rmtree(self.user_data_dir, ignore_errors=True)

    def test_sign_in_flow(self):
        page = SignInPage(self.driver)
        page.load()
        self.assertTrue(page.sign_in_flow(EMAIL, PASSWORD))


if __name__ == "__main__":
    unittest.main()
