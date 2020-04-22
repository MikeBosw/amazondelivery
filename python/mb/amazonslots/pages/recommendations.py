from selenium.webdriver.remote.webdriver import WebDriver


def is_on_recommendations_page(driver: WebDriver):
    if "recommended for you," in str(driver.page_source).lower():
        return True
    return False
