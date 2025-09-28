# tests/test_receipt.py
import unittest, os, tempfile, time
from io import BytesIO
from PIL import Image, ImageDraw

from pages.sign_in_page import SignInPage
from pages.home_page import HomePage
from pages.receipt_page import ReceiptPage
from pages.accounts_page import AccountsPage
from config import EMAIL, PASSWORD
from tests.test_setup import SETUPTEST

# --- Applitools (optional: runs only if an API key exists in .env) ---
APPLITOOLS_API_KEY = os.getenv("APPLITOOLS_API_KEY")
USE_EYES = bool(APPLITOOLS_API_KEY)
if USE_EYES:
    from applitools.selenium import Eyes, Target
    from applitools.common import RectangleSize


def create_valid_receipt_jpg_tmp(width=800, height=600):
    """Generate a realistic-looking temporary JPG receipt and return its path."""
    img = Image.new("RGB", (width, height), (255, 255, 255))
    d = ImageDraw.Draw(img)
    lines = [
        "Store: SuperMart",
        "Date: 2025-09-23",
        "Item A   2 x 15.00 = 30.00",
        "VAT: 5.10",
        "Total: 35.10 ILS",
        "Thank you!"
    ]
    y = 40
    for line in lines:
        d.text((40, y), line, fill=(0, 0, 0))
        y += 40

    buf = BytesIO()
    img.save(buf, format="JPEG", quality=90)
    fd, path = tempfile.mkstemp(suffix=".jpg")
    os.close(fd)
    with open(path, "wb") as f:
        f.write(buf.getvalue())

    if os.path.getsize(path) < 5_000:
        raise RuntimeError("Generated JPG is too small; add more content to resemble a real receipt.")
    return path


class TestReceiptInboxParse(SETUPTEST):

    def setUp(self):
        super().setUp()
        # Initialize Applitools Eyes only if an API key is provided
        self.eyes = None
        if USE_EYES:
            self.eyes = Eyes()
            self.eyes.api_key = APPLITOOLS_API_KEY
            self.eyes.open(
                self.driver,
                app_name="Firefly-UI",
                test_name=self._testMethodName,  # current test name
                viewport_size=RectangleSize(1280, 900),
            )

    def tearDown(self):
        # Close Eyes if it was started
        if self.eyes:
            try:
                self.eyes.close()
            finally:
                self.eyes.abort_if_not_closed()
        super().tearDown()

    def eyes_check(self, name: str):
        """Safe visual check: only runs if Eyes is enabled."""
        if self.eyes:
            self.eyes.check(name, Target.window().fully())

            

    def test_receipt_inbox_parse_image(self):
        sign_in = SignInPage(self.driver)
        sign_in.load()
        sign_in.sign_in_flow(EMAIL, PASSWORD)

        home = HomePage(self.driver)
        self.assertTrue(home.is_dashboard_loaded(EMAIL))
        home.go_to_receipt_inbox()

        receipt = ReceiptPage(self.driver)
        self.assertTrue(receipt.is_receipt_page_loaded())
        self.eyes_check("Receipt Inbox loaded")

        img_path = create_valid_receipt_jpg_tmp()
        try:
            receipt.upload_image(img_path)
            receipt.click_parse()
            self.assertTrue(receipt.wait_for_parsed_result_panel())
            self.eyes_check("Parsed result panel")

            # ✅ שמור את ה-merchant **לפני** יצירת הטרנזאקציה
            merchant_for_search = receipt.get_parsed_merchant_text().strip()
            total_str = receipt.get_parsed_total_amount_text()

            receipt.select_asset_account_by_text("myAssetAccount", slow=True, delay=0.8)
            receipt.select_expense_account_by_text("myExpenseAccount", slow=True, delay=0.8)
            receipt.click_create_transaction()
            self.assertTrue(receipt.wait_for_create_transaction_feedback())
            self.eyes_check("After Create Transaction")

            # ודא שיש הודעת פידבק (לא מצפה ל-ID בתוך ההודעה)
            alert_text = receipt.get_alert_text()
            self.assertTrue(alert_text)

            # ✅ חזור לעמוד ה-Receipt Inbox כדי שהטופס חיפוש יהיה נוכח
            home.go_to_receipt_inbox()

            # ✅ חיפוש לפי merchant ששמרנו
            self.assertTrue(merchant_for_search, "Parsed merchant should not be empty before searching")
            receipt.search_receipts(merchant=merchant_for_search)
            self.assertTrue(
                receipt.is_result_present_by_merchant(merchant_for_search),
                f"Expected results containing merchant '{merchant_for_search}'"
            )

            # שליפת ה-Receipt ID מהתוצאות ואז חיפוש לפי ID
            receipt_id = receipt.get_first_result_receipt_id()
            self.assertIsNotNone(receipt_id, "Expected to extract a receipt id from search results")

            receipt.search_receipts(receipt_id=receipt_id)
            self.assertTrue(
                receipt.is_result_present_by_id(receipt_id),
                f"Expected to find a result containing receipt id '{receipt_id}'"
            )

            time.sleep(4)

        finally:
            try:
                os.remove(img_path)
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main()






# APPLITOOLS_API_KEY = 3ZOobxQAY0XGqAidWXFRhxljqGncbZVRaCKbmczJ107xw110

# # tests/test_receipt.py
# import unittest, os, tempfile, time
# from io import BytesIO
# from PIL import Image, ImageDraw
# from pages.sign_in_page import SignInPage
# from pages.home_page import HomePage
# from pages.receipt_page import ReceiptPage
# from config import EMAIL, PASSWORD
# from tests.test_setup import SETUPTEST
# from pages.accounts_page import AccountsPage

# def create_valid_receipt_jpg_tmp(width=800, height=600):
#     img = Image.new("RGB", (width, height), (255, 255, 255))
#     d = ImageDraw.Draw(img)
#     lines = [
#         "Store: SuperMart",
#         "Date: 2025-09-23",
#         "Item A   2 x 15.00 = 30.00",
#         "VAT: 5.10",
#         "Total: 35.10 ILS",
#         "Thank you!"
#     ]
#     y = 40
#     for line in lines:
#         d.text((40, y), line, fill=(0, 0, 0))
#         y += 40

#     buf = BytesIO()
#     img.save(buf, format="JPEG", quality=90)
#     fd, path = tempfile.mkstemp(suffix=".jpg")
#     os.close(fd)
#     with open(path, "wb") as f:
#         f.write(buf.getvalue())

#     if os.path.getsize(path) < 5_000:
#         raise RuntimeError("Generated JPG is too small; increase content to look like a real receipt.")
#     return path


# class TestReceiptInboxParse(SETUPTEST):

#     def test_receipt_inbox_parse_image(self):
#         sign_in = SignInPage(self.driver)
#         sign_in.load()
#         sign_in.sign_in_flow(EMAIL, PASSWORD)

#         home = HomePage(self.driver)
#         self.assertTrue(home.is_dashboard_loaded(EMAIL))
#         home.go_to_receipt_inbox()
#         receipt = ReceiptPage(self.driver)
#         self.assertTrue(receipt.is_receipt_page_loaded())
#         img_path = create_valid_receipt_jpg_tmp()

#         receipt.upload_image(img_path)
#         receipt.click_parse()


#         self.assertTrue(receipt.wait_for_parsed_result_panel())

#         merchant = receipt.get_parsed_merchant_text()
#         total_str = receipt.get_parsed_total_amount_text()

#         receipt.select_asset_account_by_text("myAssetAccount", slow=True, delay=0.8)
#         receipt.select_expense_account_by_text("myExpenseAccount", slow=True, delay=0.8)
#         receipt.click_create_transaction()
#         self.assertTrue(receipt.wait_for_create_transaction_feedback())

 
#         from pages.accounts_page import AccountsPage    
#         accounts = AccountsPage(self.driver)

#         # 1) Asset accounts
#         self.assertTrue(accounts.open_asset_accounts_list())
#         self.assertTrue(accounts.assert_account_present("myAssetAccount"))

#         # 2) Expense accounts
#         self.assertTrue(accounts.open_expense_accounts_list())
#         self.assertTrue(accounts.assert_account_present("myExpenseAccount"))


#         try:
#             os.remove(img_path)
#         except OSError:
#             pass


#         time.sleep(4)


# if __name__ == "__main__":
#     unittest.main()






#pytest tests/test_receipt.py -q --alluredir=allure-results
#allure serve allure-results


# לשכבת UI (Selenium/Playwright) – תנסה Applitools Eyes → ייתן לך בדיקות ויזואליות עם AI.

# ל־API & Backend – לשלב CodiumAI או GPT-based tools ליצירת טסטים אוטומטיים.

# ל־CI/CD – להכניס self-healing AI (Testim/Mabl) אם תרצה לבדוק ממשק משתמש חי בלולאה.

#Applitools Eyes