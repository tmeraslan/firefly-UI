# pages/sign_in_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import string

class HomePage:
    DASHBOARD_SIDEBAR = (By.XPATH, "//span[contains(text(), 'Dashboard')]")
    FIREFLYIII_LOGO = (By.CLASS_NAME, "logo-lg")
    USER_EMAIL_TOP_RIGHT = (By.XPATH, "//span[contains(@class, 'navbar-text') and contains(text(), '@')]")
    DATE_RANGE_TOP = (By.XPATH, "//span[contains(text(), 'August')]")
    ACCOUNTS_SIDEBAR_BUTTON = (By.ID, "account-menu")
    ASSET_ACCOUNTS_LINK = (By.XPATH, "//a[contains(text(), 'Asset accounts')]")
    ASSET_ACCOUNTS_BUTTON= (By.XPATH, "//a[span[text()='Asset accounts']]")
    CREATE_a_NEW_ASSET_ACCOUNT_BUTTON = (By.CLASS_NAME,"btn-success")
    ASSET_ACCOUNT_FORM = (By.XPATH, "//h1[contains(text(), 'Create asset account')]")
    NAME_INPUT = (By.ID,"ffInput_name")
    STORE_NEW__ASSET_ACCOUNT_BUTTON = (By.XPATH, "//button[contains(text(),'Store new asset account')]")
    ALERT_SUCCESS = (By.CLASS_NAME, "alert-success")
    FIREFLYIII_TOP_LEFT_BUTTON = (By.CLASS_NAME, "logo-lg")
    SIDE_BAR_BUTTON = (By.ID, "sidebar-toggle")
    EXPENSE_ACCOUNTS_BUTTON = ( By.XPATH, "//a[span[text()='Expense accounts']]")
    CREATE_AN__EXPENSE_ACCOUNT_BUTTON = (By.CLASS_NAME, "btn-success")
    STORE_NEW__EXPENSE_ACCOUNT_BUTTON = (By.XPATH, "//button[contains(text(),'Store new expense account')]")




    def __init__(self, driver):
        self.driver = driver

    def is_dashboard_loaded(self, expected_email, expected_date):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.DASHBOARD_SIDEBAR)
        )
        assert self.driver.find_element(*self.FIREFLYIII_LOGO).is_displayed()
        assert self.driver.find_element(By.XPATH, f"//*[contains(text(), '{expected_email}')]").is_displayed()
        assert self.driver.find_element(By.XPATH, f"//*[contains(text(), '{expected_date}')]").is_displayed()
        return True

    def go_to_asset_accounts(self):
        self.driver.find_element(*self.ACCOUNTS_SIDEBAR_BUTTON).click()
    
    def click_asset_accounts(self):
        self.driver.find_element(*self.ASSET_ACCOUNTS_BUTTON).click()

    def click_create_new_asset_account(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CREATE_a_NEW_ASSET_ACCOUNT_BUTTON)
        )
        self.driver.find_element(*self.CREATE_a_NEW_ASSET_ACCOUNT_BUTTON).click()

    def generate_random_name(self, length=4):
      return ''.join(random.choices(string.ascii_letters, k=length))

    def insert_a_name_of_account(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.NAME_INPUT)
        )
        random_name = self.generate_random_name()+ "Account"
        self.driver.find_element(*self.NAME_INPUT).send_keys(random_name)

    def click_store_new_asset_account(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.STORE_NEW__ASSET_ACCOUNT_BUTTON)
        )
        self.driver.find_element(*self.STORE_NEW__ASSET_ACCOUNT_BUTTON).click()

    def i_see_success_alert(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.ALERT_SUCCESS)
        )
        return self.driver.find_element(*self.ALERT_SUCCESS).is_displayed()

    def is_create_new_asset_account_successful(self):
        return self.i_see_success_alert()

    def click_expense_accounts(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EXPENSE_ACCOUNTS_BUTTON)
        )
        self.driver.find_element(*self.EXPENSE_ACCOUNTS_BUTTON).click()

    def click_create_new_expense_account(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.CREATE_AN__EXPENSE_ACCOUNT_BUTTON)
        )
        self.driver.find_element(*self.CREATE_AN__EXPENSE_ACCOUNT_BUTTON).click()

    def click_store_new_expense_account(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.STORE_NEW__EXPENSE_ACCOUNT_BUTTON)
        )
        self.driver.find_element(*self.STORE_NEW__EXPENSE_ACCOUNT_BUTTON).click()

    def is_create_new_expense_account_successful(self):
        return self.i_see_success_alert()
