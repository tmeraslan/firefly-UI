# pages/accounts_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AccountsPage:
    ACCOUNT_MENU = (By.ID, "account-menu")
    ACCOUNT_MENU_TOGGLE = (By.CSS_SELECTOR, "#account-menu > a")

    ASSET_ACCOUNTS_LINK = (By.CSS_SELECTOR, 'a[href$="/accounts/asset"]')
    ASSET_ACCOUNTS_BY_TEXT = (By.XPATH, '//a[.//span[normalize-space()="Asset accounts"]]')
    EXPENSE_ACCOUNTS_LINK = (By.CSS_SELECTOR, 'a[href$="/accounts/expense"]')
    EXPENSE_ACCOUNTS_BY_TEXT = (By.XPATH, '//a[.//span[normalize-space()="Expense accounts"]]')

    def ACCOUNT_IN_LIST(self, name: str):
        return (By.XPATH, f'//table//a[normalize-space()="{name}"]'
                          f' | //ul//a[normalize-space()="{name}"]')

    def __init__(self, driver):
        self.driver = driver

    def _ensure_menu_open(self):
        menu = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(self.ACCOUNT_MENU))
        if "menu-open" not in (menu.get_attribute("class") or ""):
            self.driver.find_element(*self.ACCOUNT_MENU_TOGGLE).click()
            WebDriverWait(self.driver, 10).until(
                lambda d: "menu-open" in d.find_element(*self.ACCOUNT_MENU).get_attribute("class")
            )

    def _click_link(self, by_text_locator, by_href_locator):
        self._ensure_menu_open()
        wait = WebDriverWait(self.driver, 15)
        try:
            link = wait.until(EC.element_to_be_clickable(by_text_locator))
        except Exception:
            link = wait.until(EC.element_to_be_clickable(by_href_locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
        try:
            link.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", link)
        return True

    def open_asset_accounts_list(self):
        self._click_link(self.ASSET_ACCOUNTS_BY_TEXT, self.ASSET_ACCOUNTS_LINK)
        WebDriverWait(self.driver, 15).until(EC.url_contains("/accounts/asset"))
        return True

    def open_expense_accounts_list(self):
        self._click_link(self.EXPENSE_ACCOUNTS_BY_TEXT, self.EXPENSE_ACCOUNTS_LINK)
        WebDriverWait(self.driver, 15).until(EC.url_contains("/accounts/expense"))
        return True

    def assert_account_present(self, name: str):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.ACCOUNT_IN_LIST(name))
        )
        return True
