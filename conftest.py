# conftest.py
import os
import pytest
import datetime
from dotenv import load_dotenv

# טען משתני .env לכל הטסטים
load_dotenv()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # הרץ את הטסט וקבל דוח
    outcome = yield
    report = outcome.get_result()

    # Screenshot אוטומטי בכישלון של שלב ה-call
    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            os.makedirs("screenshots", exist_ok=True)
            file_name = f"screenshots/{item.name}_{now}.png"
            driver.save_screenshot(file_name)
            print(f"\n📸 Screenshot saved to: {file_name}")









# #conftest.py
# import pytest
# import datetime

# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     #get the test result 
#     outcome = yield
#     report = outcome.get_result()

#     # Only if the test failed and at the "call" stage (the run itself)
#     if report.when == 'call' and report.failed:
#         driver = item.funcargs.get('driver')
#         if driver:
#             now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             file_name = f"screenshots/{item.name}_{now}.png"
#             driver.save_screenshot(file_name)
#             print(f"\n📸 Screenshot saved to: {file_name}")
