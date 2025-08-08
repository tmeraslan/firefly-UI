import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.sign_in_page import SignInPage
from pages.home_page import HomePage
import time

email = "tmeraslan1@gmail.com"
password = "r_ATzrCF9NFjMCF123"
expected_date = "August 1st, 2025 - August 31st, 2025"

@pytest.fixture
def driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver
    driver.quit()

def test_create_new_asset_account(driver):
    sign_in = SignInPage(driver)
    sign_in.load()
    sign_in.sign_in_flow(email, password)

    home = HomePage(driver)
    assert home.is_dashboard_loaded(email, expected_date)
    home.go_to_asset_accounts()
    home.click_asset_accounts()
    home.click_create_new_asset_account()
    home.insert_a_name_of_account()
    home.click_store_new_asset_account()
    assert home.i_see_success_alert()
    time.sleep(10)