import asyncio
import os
import pickle
import traceback
from typing import Optional, Tuple

from selenium.webdriver.remote.webdriver import WebDriver

from mb.amazonslots.lib.urls import BASE_URL

COOKIES_PATH = "cookies.pkl.secret"
USERNAME_PATH = "username.secret"
PASSWORD_PATH = "password.secret"


def is_signed_in(driver: WebDriver):
    if not str(driver.current_url).startswith(BASE_URL):
        return False
    if has_sign_in_title(driver):
        return True
    if get_sign_in_link_maybe(driver) is None:
        return True
    return False


def has_sign_in_title(driver: WebDriver):
    # the first guest sign-in page has this title
    h1 = driver.find_elements_by_tag_name("h1")
    h2 = driver.find_elements_by_tag_name("h2")
    for header in h1 + h2:
        if str(header.text).lower() in ["sign-in", "sign in"]:
            return True
    return False


def get_sign_in_link_maybe(driver: WebDriver):
    # the guest home page has a sign-in link
    links = driver.find_elements_by_css_selector("a[data-nav-role=signin]")
    for link in links:
        if "sign in" in str(link.text).lower():
            return link
    return None


def get_email_field(driver: WebDriver):
    # the first guest sign-in page has an email field
    fields = driver.find_elements_by_css_selector("input[type=email]")
    if len(fields) != 1:
        raise RuntimeError("expected exactly 1 email field, found: %s" % fields)
    return fields[0]


def get_password_field(driver: WebDriver):
    # the second guest sign-in page has a password field
    fields = driver.find_elements_by_css_selector("input[type=password]")
    if len(fields) != 1:
        raise RuntimeError("expected exactly 1 email field, found: %s" % fields)
    return fields[0]


def get_credentials_maybe() -> Optional[Tuple[str, str]]:
    """Returns credentials, if any, provided by the environment."""
    username, password = None, None
    if os.path.exists(USERNAME_PATH) and os.path.exists(PASSWORD_PATH):
        try:
            with open(USERNAME_PATH) as username_file:
                username = username_file.read().strip()
            with open(PASSWORD_PATH) as password_file:
                password = password_file.read().strip()
        except IOError:
            print(traceback.format_exc())
            print("error attempting to read username, password, or both")
    if username and password:
        return username, password
    return None


def persist_cookies(driver: WebDriver):
    with open(COOKIES_PATH, "wb") as cookies_file:
        pickle.dump(driver.get_cookies(), cookies_file)


def restore_cookies(driver: WebDriver):
    if os.path.exists(COOKIES_PATH):
        with open(COOKIES_PATH, "rb") as cookies_file:
            cookies = pickle.load(cookies_file)
    else:
        cookies = []
    print("restoring %s cookies from disk" % len(cookies))
    for cookie in cookies:
        if "expiry" in cookie:
            cookie["expiry"] = int(cookie["expiry"])
        driver.add_cookie(cookie)


def get_continue_button(driver: WebDriver):
    # both sign-in pages have a continue button
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if button.text == "Continue":
            return button
    raise RuntimeError("could not find continue button on sign-in page")


def get_sign_in_button(driver: WebDriver):
    # both sign-in pages have a continue button
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if str(button.text).lower() == "sign-in":
            return button
    raise RuntimeError("could not find sign-in button on sign-in page")


def get_remember_me_box(driver: WebDriver):
    boxes = driver.find_elements_by_css_selector(
        "input[type=checkbox][name=rememberMe]"
    )
    if len(boxes) != 1:
        raise RuntimeError("expected exactly one remember-me box, found: %s", boxes)
    return boxes[0]


async def sign_in(driver: WebDriver):
    print("attempting sign-in")
    restore_cookies(driver)
    driver.get(BASE_URL)
    if is_signed_in(driver):
        return
    credentials = get_credentials_maybe()
    if credentials:
        username, password = credentials
        await sign_in_manually(driver, username, password)
    if not is_signed_in(driver):
        print("sign-in failed; awaiting manual sign-in")
        while not is_signed_in(driver):
            await asyncio.sleep(1)
    persist_cookies(driver)
    print("sign-in detected")


async def sign_in_manually(driver: WebDriver, username: str, password: str):
    print("credentials were provided; attempting manual sign-in")
    sign_in_link = get_sign_in_link_maybe(driver)
    if not sign_in_link:
        raise RuntimeError("could not find sign-in link")
    sign_in_link.click()
    print("clicked sign-in link; waiting 1s")
    await asyncio.sleep(1)
    email_field = get_email_field(driver)
    email_field.click()
    email_field.send_keys(username)
    get_continue_button(driver).click()
    print("entered email and clicked continue button; waiting 1s")
    await asyncio.sleep(1)
    password_field = get_password_field(driver)
    password_field.click()
    password_field.send_keys(password)
    get_remember_me_box(driver).click()
    get_sign_in_button(driver).click()
    print("entered password and clicked sign-in button; waiting 1s")
    await asyncio.sleep(1)
