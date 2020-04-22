from selenium.webdriver.remote.webdriver import WebDriver

from mb.amazonslots.lib.auth import is_signed_in
from mb.amazonslots.lib.urls import BASE_URL


async def jump_to_guest_page(driver: WebDriver):
    driver.get(BASE_URL)


def is_on_guest_page(driver: WebDriver):
    return driver.current_url.startswith(BASE_URL) and not is_signed_in(driver)


def is_on_signed_in_page(driver: WebDriver):
    return driver.current_url.startswith(BASE_URL) and is_signed_in(driver)
