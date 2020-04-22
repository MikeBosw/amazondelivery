from selenium.webdriver.remote.webdriver import WebDriver

from mb.amazonslots.lib import alerts
from mb.amazonslots.lib.auth import get_credentials_maybe


def is_on_sign_in_again_page(driver: WebDriver):
    return "keep me signed in" in str(driver.page_source).lower()


def get_password_field(driver: WebDriver):
    return driver.find_element_by_css_selector("input[type=password]")


def enter_password(password_field, password):
    password_field.click()
    password_field.send_keys(password)


def get_sign_in_button(driver: WebDriver):
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if str(button.text).lower() == "sign-in":
            return button
    raise RuntimeError("could not find sign-in button")


async def reauth_maybe(driver: WebDriver):
    if not is_on_sign_in_again_page(driver):
        raise RuntimeError("not on sign-in-again page")
    credentials = get_credentials_maybe()
    if not credentials:
        alerts.tell_engineer("They want you to re-enter your password.")
        return
    _, password = credentials
    print("password was provided; attempting to enter it")
    pwf = get_password_field(driver)
    enter_password(pwf, password)
    get_sign_in_button(driver).click()
