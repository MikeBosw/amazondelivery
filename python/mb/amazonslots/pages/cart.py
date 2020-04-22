from selenium.webdriver.remote.webdriver import WebDriver

from mb.amazonslots.lib.urls import CART_URL
from mb.amazonslots.lib.wfaf import FoodService


class CartState:
    def __init__(self, has_amazon_fresh: bool, has_whole_foods: bool):
        self.has_whole_foods = has_whole_foods
        self.has_amazon_fresh = has_amazon_fresh

    def is_cart_ready(self, service: FoodService):
        if service == FoodService.AMAZON_FRESH:
            return self.has_amazon_fresh
        elif service == FoodService.WHOLE_FOODS:
            return self.has_whole_foods
        else:
            raise RuntimeError("unrecognized food service: %s" % service)


def get_cart_state(driver: WebDriver) -> CartState:
    if not is_on_cart_page(driver):
        raise RuntimeError("not currently on cart page")
    has_af = bool(get_af_checkout_button_maybe(driver))
    has_wf = bool(get_wf_checkout_button_maybe(driver))
    return CartState(has_amazon_fresh=has_af, has_whole_foods=has_wf)


async def jump_to_cart_page(driver: WebDriver):
    driver.get(CART_URL)
    if not is_on_cart_page(driver):
        raise RuntimeError("was not able to land on cart page")


def get_af_checkout_button_maybe(driver: WebDriver):
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if str(button.text).lower() == "checkout amazon fresh cart":
            return button.find_element_by_tag_name("input")
    return None


def get_wf_checkout_button_maybe(driver: WebDriver):
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if str(button.text).lower() == "checkout whole foods market cart":
            return button.find_element_by_tag_name("input")
    return None


def has_shopping_cart_title(driver: WebDriver):
    headers = driver.find_elements_by_tag_name("h2")
    for header in headers:
        if str(header.text).lower() == "shopping cart":
            return True
    return False


def get_add_to_af_button_maybe(driver: WebDriver):
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if str(button.text).lower() == "add to amazon fresh order":
            return button


def get_add_to_wf_button_maybe(driver: WebDriver):
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if str(button.text).lower() == "add to whole foods order":
            return button


async def click_af_checkout(driver: WebDriver):
    button = get_af_checkout_button_maybe(driver)
    if not button:
        raise RuntimeError("not on the cart page")
    button.click()


async def click_wf_checkout(driver: WebDriver):
    button = get_wf_checkout_button_maybe(driver)
    if not button:
        raise RuntimeError("not on the cart page")
    button.click()


def is_on_cart_page(driver: WebDriver):
    if has_shopping_cart_title(driver):
        return True
    if get_af_checkout_button_maybe(driver):
        return True
    if get_add_to_af_button_maybe(driver):
        return True
    if get_wf_checkout_button_maybe(driver):
        return True
    if get_add_to_wf_button_maybe(driver):
        return True
    return False
