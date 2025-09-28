# tests/test_setup.py
import tempfile
import shutil
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from pathlib import Path
import os
import time

class SETUPTEST(unittest.TestCase):
    def setUp(self):
        options = Options()

        if os.getenv("HEADLESS", "false").lower() == "true":
            options.add_argument("--headless=new")
            options.add_argument("--window-size=1366,900")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.run_tmp = Path(tempfile.mkdtemp(prefix=f"chrome-run-{int(time.time())}-"))
        self.user_data_dir = self.run_tmp / "profile"
        self.cache_dir = self.run_tmp / "cache"
        self.download_dir = self.run_tmp / "downloads"
        for p in (self.user_data_dir, self.cache_dir, self.download_dir):
            p.mkdir(parents=True, exist_ok=True)

        options.add_argument(f"--user-data-dir={self.user_data_dir}")
        options.add_argument(f"--disk-cache-dir={self.cache_dir}")

        prefs = {
            "download.default_directory": str(self.download_dir.resolve()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)

        service = Service()  
        self.driver = webdriver.Chrome(service=service, options=options)

        if os.getenv("HEADLESS", "false").lower() != "true":
            try:
                self.driver.maximize_window()
            except Exception:
                pass

    def tearDown(self):
        try:
            self.driver.quit()
        finally:
            shutil.rmtree(self.run_tmp, ignore_errors=True)





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