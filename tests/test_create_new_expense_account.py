import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.sign_in_page import SignInPage
from pages.home_page import HomePage
from config import EMAIL, PASSWORD
from tests.test_setup import SETUPTEST
import time



expected_date = "August 1st, 2025 - August 31st, 2025"


class TestCreateExpenseAccount(SETUPTEST):


    def test_create_new_expense_account(self):
        sign_in = SignInPage(self.driver)
        sign_in.load()
        sign_in.sign_in_flow(EMAIL, PASSWORD)

        home = HomePage(self.driver)
        self.assertTrue(home.is_dashboard_loaded(EMAIL, expected_date))
        home.go_to_asset_accounts()
        home.click_expense_accounts()
        home.click_create_new_expense_account()
        home.insert_a_name_of_account()
        home.click_store_new_expense_account()
        self.assertTrue(home.is_create_new_expense_account_successful())



if __name__ == "__main__":
    unittest.main()
