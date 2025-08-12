# tests/test_setup.py
import tempfile
import shutil
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

class SETUPTEST(unittest.TestCase):
    def setUp(self):
        options = Options()
        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
  
        # # Create a temporary profile folder -user data
        # self.user_data_dir = tempfile.mkdtemp(prefix="chrome-user-data-")
        # options.add_argument(f"--user-data-dir={self.user_data_dir}")

        # # It's important to add the window-size before creating the driver
        # options.add_argument("window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=options)
        self.driver.maximize_window()

    def tearDown(self):
        self.driver.quit()
        # shutil.rmtree(self.user_data_dir, ignore_errors=True)
