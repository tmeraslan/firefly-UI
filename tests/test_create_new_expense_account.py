#test_create_new_expense_account.py
import unittest
from pages.sign_in_page import SignInPage
from pages.home_page import HomePage
from config import EMAIL, PASSWORD
from tests.test_setup import SETUPTEST



class TestCreateExpenseAccount(SETUPTEST):
 

    def test_create_new_expense_account(self):
        sign_in = SignInPage(self.driver)
        sign_in.load()
        sign_in.sign_in_flow(EMAIL, PASSWORD)

        home = HomePage(self.driver)
        self.assertTrue(home.is_dashboard_loaded(EMAIL))
        home.go_to_asset_accounts()
        home.click_expense_accounts()
        home.click_create_new_expense_account()
        home.insert_a_name_of_account()
        home.click_store_new_expense_account()
        self.assertTrue(home.is_create_new_expense_account_successful())



if __name__ == "__main__":
    unittest.main()
