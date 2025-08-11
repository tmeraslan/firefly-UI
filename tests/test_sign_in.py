import unittest
from tests.test_setup import SETUPTEST   
from pages.sign_in_page import SignInPage
from config import EMAIL, PASSWORD

class TestSignInFlow(SETUPTEST): 
    def test_sign_in_flow(self):
        page = SignInPage(self.driver)
        page.load()
        self.assertTrue(page.sign_in_flow(EMAIL, PASSWORD))


if __name__ == "__main__":
    unittest.main()
