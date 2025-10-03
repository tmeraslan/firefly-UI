# pages/receipt_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import re


import random
import string
import time


class ReceiptPage:

 
    RECEIPT_INBOX_TEXT = (By.LINK_TEXT, "Receipt Inbox")

    PARSE_BUTTON = (By.XPATH, "//button[contains(normalize-space(.), 'Parse')]")
    FILE_INPUT = (By.ID, "file")

    PARSED_PANEL_HEADING = (By.XPATH, "//div[contains(@class,'panel-heading') and normalize-space()='Parsed result']")
    ASSET_LABEL = (By.XPATH, "//label[contains(normalize-space(.), 'Asset Account')]")
    EXPENSE_LABEL = (By.XPATH, "//label[contains(normalize-space(.), 'Expense Account')]")
    RAW_TEXT_TITLE = (By.XPATH, "//p/strong[normalize-space(.)='Extracted Receipt Text']")

    ASSET_SELECT = (By.NAME, "asset_account_id")
    EXPENSE_SELECT = (By.NAME, "expense_account_id")
    CREATE_TX_BUTTON = (By.XPATH, "//button[normalize-space()='Create Transaction']")

    ALERT_ANY = (By.CSS_SELECTOR, ".alert, .alert-success, .alert-info, .alert-danger")

    MERCHANT_DD = (By.XPATH, "//dt[normalize-space()='Merchant']/following-sibling::dd[1]")
    TOTAL_DD    = (By.XPATH, "//dt[normalize-space()='Total Amount']/following-sibling::dd[1]")


    # --- Alerts & Search form ---
    ALERT_SUCCESS = (By.CSS_SELECTOR, ".alert-success")  # אופציונלי: יש גם ALERT_ANY שכבר מוגדר
    SEARCH_ID_INPUT = (By.ID, "id")
    SEARCH_MERCHANT_INPUT = (By.ID, "merchant")
    SEARCH_BUTTON = (By.XPATH, "//button[normalize-space()='Search']")
    SEARCH_RESULTS_TABLE = (By.CSS_SELECTOR, "table")
    RECEIPT_RESULTS_LINKS = (By.CSS_SELECTOR, "table a")





    def __init__(self, driver):
        self.driver = driver
        # self.last_created_account_name = None

    def is_receipt_page_loaded(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.RECEIPT_INBOX_TEXT)
        )
        assert self.driver.find_element(*self.RECEIPT_INBOX_TEXT).is_displayed()
        assert self.driver.find_element(*self.PARSE_BUTTON).is_displayed()
        return True
    

    def upload_image(self, file_path: str):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.FILE_INPUT)
        )
        self.driver.find_element(*self.FILE_INPUT).send_keys(file_path)

    def click_parse(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.PARSE_BUTTON)
        ).click()

    def wait_for_parsed_result_panel(self, timeout: int = 120):
 
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.PARSED_PANEL_HEADING)
        )
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.ASSET_LABEL)
        )
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.EXPENSE_LABEL)
        )
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.RAW_TEXT_TITLE)
        )
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.ASSET_SELECT)
        )
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.EXPENSE_SELECT)
        )
        WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(self.CREATE_TX_BUTTON)
        )
        return True

    def select_asset_account_by_text(self, visible_text: str, slow: bool = False, delay: float = 0.7):
        select_el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.ASSET_SELECT)
        )
        if slow:
            ActionChains(self.driver).move_to_element(select_el).pause(delay).click().pause(delay).perform()
        sel = Select(select_el)
        if slow:
            time.sleep(delay)
        sel.select_by_visible_text(visible_text)
        if slow:
            time.sleep(delay)

    def select_expense_account_by_text(self, visible_text: str, slow: bool = False, delay: float = 0.7):
        select_el = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.EXPENSE_SELECT)
        )
        if slow:
            ActionChains(self.driver).move_to_element(select_el).pause(delay).click().pause(delay).perform()
        sel = Select(select_el)
        if slow:
            time.sleep(delay)
        sel.select_by_visible_text(visible_text)
        if slow:
            time.sleep(delay)

    def click_create_transaction(self):
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(self.CREATE_TX_BUTTON)
            ).click()

    def wait_for_create_transaction_feedback(self, timeout: int = 30):

        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.ALERT_ANY)
        )
        return True
#######################################

    def get_parsed_merchant_text(self) -> str:
        el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.MERCHANT_DD)
        )
        return el.text.strip()

    def get_parsed_total_amount_text(self) -> str:
        """
        Return the amount text as displayed (e.g., '303' or '303.00').
        For convenience, normalize it to digits and a dot only; if the normalized
        string is empty, fall back to the raw text.
        """
        el = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.TOTAL_DD)
        )
        raw = el.text.strip()
        # Keep only digits and a dot to avoid currency symbol/locale issues
        normalized = re.sub(r"[^0-9.]", "", raw)
        return normalized or raw
    

    #///////////////////////////

    def get_alert_text(self) -> str:
        """מחזיר את טקסט ההודעה (הצלחה/מידע/שגיאה) לאחר Create Transaction."""
        el = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.ALERT_ANY)
        )
        return el.text.strip()

    def extract_receipt_id_from_alert(self) -> str:
        """
        מנסה לחלץ Receipt ID מהודעת ההצלחה.
        קודם מחפש UUID קלאסי (36 תווים), ואם לא – דפוס כללי אחרי 'Receipt ID' או 'ID'.
        """
        txt = self.get_alert_text()
        # UUID (לרוב v4)
        m = re.search(r"\b[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}\b", txt)
        if m:
            return m.group(0)
        # Receipt ID: XXXXX או ID: XXXXX
        m = re.search(r"(?:Receipt ID|ID)\s*[:#]?\s*([A-Za-z0-9\-]{6,})", txt)
        if m:
            return m.group(1)
        return None


    def _type_into(self, locator, text, slow=False, per_char_delay=0.08):
            el = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
            el.clear()
            if slow:
                for ch in text:
                    el.send_keys(ch)
                    time.sleep(per_char_delay)
            else:
                el.send_keys(text)

    def _slow_click(self, locator, slow=False, delay=0.6):
        btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(locator))
        if slow:
            ActionChains(self.driver).move_to_element(btn).pause(delay).perform()
        btn.click()
        if slow:
            time.sleep(delay)

    def search_receipts(self, receipt_id: str = None, merchant: str = None, *, slow: bool = False, delay: float = 0.6, per_char_delay: float = 0.1):
        """
        חיפוש קבלות לפי ID או merchant.
        slow=True => הקלדה איטית + פאוזות לפני/אחרי קליק + המתנות לשינוי URL.
        """
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.SEARCH_BUTTON))

        # נקה ומלא
        if receipt_id:
            self._type_into(self.SEARCH_ID_INPUT, receipt_id, slow=slow, per_char_delay=per_char_delay)
            # אם ממלאים id – ננקה merchant
            self._type_into(self.SEARCH_MERCHANT_INPUT, "", slow=False)
        elif merchant:
            # אם ממלאים merchant – ננקה id
            self._type_into(self.SEARCH_ID_INPUT, "", slow=False)
            self._type_into(self.SEARCH_MERCHANT_INPUT, merchant, slow=slow, per_char_delay=per_char_delay)

        old_url = self.driver.current_url

        self._slow_click(self.SEARCH_BUTTON, slow=slow, delay=delay)

        # המתן לשינוי כתובת (query params משתנים) או לטבלת תוצאות
        try:
            WebDriverWait(self.driver, 15).until(lambda d: d.current_url != old_url)
        except Exception:
            pass  # אם ה-URL לא השתנה, נמשיך להמתין לטבלה

        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.SEARCH_RESULTS_TABLE))

        if slow:
            time.sleep(delay)


    def is_result_present_by_merchant(self, merchant: str) -> bool:
        """בודק אם המילה/ה-merchant מופיע/ה בטבלת התוצאות."""
        table = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.SEARCH_RESULTS_TABLE)
        )
        return merchant.lower() in table.text.lower()

    def is_result_present_by_id(self, receipt_id: str) -> bool:
        """בודק אם ה-Receipt ID מופיע בטבלת התוצאות או בעמוד."""
        try:
            table = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.SEARCH_RESULTS_TABLE)
            )
            return (receipt_id in table.text) or (receipt_id in self.driver.page_source)
        except Exception:
            return receipt_id in self.driver.page_source
        
    
    def get_first_result_receipt_id(self) -> str:
        """
        מחזיר את ה-Receipt ID מתוך תוצאות החיפוש (השורה הראשונה שמכילה UUID).
        קודם מחפש UUID בטקסט הטבלה, ואם לא נמצא – מנסה דרך href/טקסט של קישורים.
        """
        table = WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.SEARCH_RESULTS_TABLE)
        )

        import re
        uuid_re = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")

        # נסה למצוא UUID ישירות בטקסט הטבלה
        m = uuid_re.search(table.text or "")
        if m:
            return m.group(0)

        # אם לא נמצא, עבור על קישורים בתוך הטבלה (טקסט ו-href)
        for a in table.find_elements(*self.RECEIPT_RESULTS_LINKS):
            blob = f"{a.text or ''} {(a.get_attribute('href') or '')}"
            m = uuid_re.search(blob)
            if m:
                return m.group(0)

        return None

    
