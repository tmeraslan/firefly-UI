
# conftest.py
import os
import pytest
import datetime
from dotenv import load_dotenv

load_dotenv()

# ✨ חדש:
try:
    import allure
except ImportError:
    allure = None

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('driver')
        if driver:
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            os.makedirs("screenshots", exist_ok=True)
            file_name = f"screenshots/{item.name}_{now}.png"
            driver.save_screenshot(file_name)
            print(f"\n📸 Screenshot saved to: {file_name}")

            # ✨ Allure attachment (אם מותקן)
            if allure:
                try:
                    allure.attach.file(file_name, name=f"{item.name}_screenshot", attachment_type=allure.attachment_type.PNG)
                except Exception:
                    pass
                # אפשר גם לצרף HTML של העמוד
                try:
                    page_source = driver.page_source
                    allure.attach(page_source, name=f"{item.name}_dom.html", attachment_type=allure.attachment_type.HTML)
                except Exception:
                    pass

# ✨ אופציונלי: יצירת environment.properties ל-Allure
def pytest_sessionstart(session):
    # ניצור קובץ בספריית התוצאות (אם לא קיימת עדיין – pytest ייצור בזמן הריצה)
    os.makedirs("allure-results", exist_ok=True)
    env_path = os.path.join("allure-results", "environment.properties")
    with open(env_path, "w", encoding="utf-8") as f:
        f.write(f"FIREFLY_URL={os.getenv('FIREFLY_URL','')}\n")
        f.write(f"HEADLESS={os.getenv('HEADLESS','')}\n")
        f.write(f"CI={os.getenv('CI','')}\n")



# # conftest.py
# import os
# import pytest
# import datetime
# from dotenv import load_dotenv

# load_dotenv()

# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report = outcome.get_result()

#     if report.when == 'call' and report.failed:
#         driver = item.funcargs.get('driver')
#         if driver:
#             now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#             os.makedirs("screenshots", exist_ok=True)
#             file_name = f"screenshots/{item.name}_{now}.png"
#             driver.save_screenshot(file_name)
#             print(f"\n📸 Screenshot saved to: {file_name}")









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
