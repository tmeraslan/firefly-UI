# tests/test_setup.py
import unittest, os, uuid, pathlib, shutil
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class SETUPTEST(unittest.TestCase):
    def setUp(self):
        options = Options()

        # השתמש בבינארי שהותקן (לא Chrome for Testing)
        options.binary_location = "/usr/bin/google-chrome"

        # Headed כברירת מחדל
        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1920,1080")
        else:
            options.add_argument("--start-maximized")

        # דגלים ליציבות
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")  # משאיר לנו שליטה בפרופיל ב-/dev/shm
        options.add_argument("--no-first-run")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--password-store=basic")
        options.add_argument("--use-mock-keychain")

        # >>> פרופיל ייחודי על tmpfs שתומך בנעילות
        base = pathlib.Path("/dev/shm") / f"selenium-profiles-{os.getuid()}"
        base.mkdir(parents=True, exist_ok=True)
        self.user_data_dir = base / f"profile-{uuid.uuid4().hex}"
        self.user_data_dir.mkdir(mode=0o700)
        options.add_argument(f"--user-data-dir={self.user_data_dir}")
        options.add_argument("--profile-directory=Profile 1")

        # תן ל-Selenium Manager להביא דרייבר תואם
        self.driver = webdriver.Chrome(service=Service(), options=options)

    def tearDown(self):
        try:
            self.driver.quit()
        finally:
            shutil.rmtree(self.user_data_dir, ignore_errors=True)






# # tests/test_setup.py
# import tempfile
# import shutil
# import unittest
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import os
# import time

# class SETUPTEST(unittest.TestCase):
#     def setUp(self):
#         options = Options()
#         if os.getenv("HEADLESS", "false").lower() == "true":
#             options.add_argument("--headless=new")
            

#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         # # Create a temporary profile folder -user data
#         self.user_data_dir = tempfile.mkdtemp(prefix=f"chrome-user-data-uid-{time.time()}")
#         options.add_argument(f"--user-data-dir={self.user_data_dir}")

#         # # It's important to add the window-size before creating the driver
        
#         self.driver = webdriver.Chrome(options=options)
#         self.driver.maximize_window()

#     def tearDown(self):
#         self.driver.quit()
#         shutil.rmtree(self.user_data_dir, ignore_errors=True)