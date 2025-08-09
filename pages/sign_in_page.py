
#sign_in_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import URL

class SignInPage:

    SIGN_IN_TEXT = (By.XPATH, "//*[contains(text(), 'Sign in to start your session')]")
    SIGN_IN_BUTTON = (By.XPATH, "//button[contains(text(), 'Sign in')]")
    EMAIL_INPUT = (By.XPATH, "//input[@type='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@type='password']")
    REMEMBER_LABEL = (By.XPATH, "//*[contains(text(), 'Remember me')]")
    REMEMBER_CHECKBOX = (By.XPATH, "//input[@type='checkbox']")
    SUCCESS_TOAST = (By.ID, "toast-container")  # נניח שזו ההודעה שמופיעה
    USER_EMAIL_TOP_RIGHT = (By.XPATH, "//span[contains(@class, 'navbar-text') and contains(text(), '@')]")
    FIREFLYIII_TOP_LEFT_BUTTON = (By.CLASS_NAME, "logo-lg")
    expected_email = "tmeraslan1@gmail.com"
    SIDE_BAR_BUTTON = (By.ID, "sidebar-toggle")
    ALERT_INVALID_CREDENTIALS = (By.XPATH, "//div[contains(@class, 'alert-danger')]")


    def __init__(self, driver):
        self.driver = driver            
        self.URL = URL

    def load(self):
        self.driver.get(self.URL)

    def is_sign_in_text_present(self):
        return len(self.driver.find_elements(*self.SIGN_IN_TEXT)) > 0

    def is_sign_in_button_present(self):
        return len(self.driver.find_elements(*self.SIGN_IN_BUTTON)) > 0

    def is_email_input_present(self):
        return len(self.driver.find_elements(*self.EMAIL_INPUT)) > 0

    def is_password_input_present(self):
        return len(self.driver.find_elements(*self.PASSWORD_INPUT)) > 0

    def is_remember_label_present(self):
        return len(self.driver.find_elements(*self.REMEMBER_LABEL)) > 0

    def is_remember_checkbox_present(self):
        return len(self.driver.find_elements(*self.REMEMBER_CHECKBOX)) > 0

    def login(self, email, password, remember=False):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.EMAIL_INPUT)
        )
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        if remember:
            checkbox = self.driver.find_element(*self.REMEMBER_CHECKBOX)
            if not checkbox.is_selected():
                checkbox.click()
        self.driver.find_element(*self.SIGN_IN_BUTTON).click()

        return self  # Returns the same page to maintain page chaining.


    def is_logged_in_successfully(self):

        
        # Wait for the FireflyIII button (top left)
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.FIREFLYIII_TOP_LEFT_BUTTON)
        )

        # Check user email top right
        email_elem = self.driver.find_element(
            By.XPATH, f"//*[contains(text(), '{self.expected_email}')]"
        )

        if not email_elem.is_displayed():
            return False
            
        if len(self.driver.find_elements(*self.SIDE_BAR_BUTTON)) != 1:
            return False
        
        return True

    def sign_in_flow(self, email, password):

        assert self.is_sign_in_text_present()
        assert self.is_sign_in_button_present()
        assert self.is_email_input_present()
        assert self.is_password_input_present()
        assert self.is_remember_label_present()
        assert self.is_remember_checkbox_present()

        # Making a connection
        self.login(email, password, remember=True)

        #Success check
        assert self.is_logged_in_successfully()
        return True

    def is_invalid_credentials_alert_present(self):
        return len(self.driver.find_elements(*self.ALERT_INVALID_CREDENTIALS)) > 0