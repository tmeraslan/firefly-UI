#tests/test_sign_in_fails.py
import unittest
from pages.sign_in_page import SignInPage
from config import INVALID_EMAIL, INVALID_PASSWORD, EMAIL, PASSWORD
from tests.test_setup import SETUPTEST

class TestSignInFails(SETUPTEST):


    def test_login_fails_with_invalid_email(self):
        page = SignInPage(self.driver)
        page.load()
        page.login(INVALID_EMAIL, PASSWORD, remember=False)
        self.assertTrue(page.is_invalid_credentials_alert_present())

    def test_login_fails_with_invalid_password(self):
        page = SignInPage(self.driver)
        page.load()
        page.login(EMAIL, INVALID_PASSWORD, remember=False)
        self.assertTrue(page.is_invalid_credentials_alert_present())


if __name__ == "__main__":
    unittest.main()
