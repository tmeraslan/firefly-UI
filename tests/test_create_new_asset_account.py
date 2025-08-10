import unittest
import tempfile
import shutil
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.sign_in_page import SignInPage
from pages.home_page import HomePage
from config import EMAIL, PASSWORD


expected_date = "August 1st, 2025 - August 31st, 2025"


class TestCreateAssetAccount(unittest.TestCase):

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

    def test_create_new_asset_account(self):
        sign_in = SignInPage(self.driver)
        sign_in.load()
        sign_in.sign_in_flow(EMAIL, PASSWORD)

        home = HomePage(self.driver)
        self.assertTrue(home.is_dashboard_loaded(EMAIL, expected_date))
        home.go_to_asset_accounts()
        home.click_asset_accounts()
        home.click_create_new_asset_account()
        home.insert_a_name_of_account()
        home.click_store_new_asset_account()
        self.assertTrue(home.i_see_success_alert())
        time.sleep(10)


if __name__ == "__main__":
    unittest.main()
