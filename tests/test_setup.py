# tests/test_setup.py
import tempfile
import shutil
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class SETUPTEST(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Create a temporary profile folder -user data
        self.user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
        options.add_argument(f"--user-data-dir={self.user_data_dir}")

        # It's important to add the window-size before creating the driver
        options.add_argument("window-size=1920,1080")

        self.driver = webdriver.Chrome(options=options)

    def tearDown(self):
        self.driver.quit()
        shutil.rmtree(self.user_data_dir, ignore_errors=True)
