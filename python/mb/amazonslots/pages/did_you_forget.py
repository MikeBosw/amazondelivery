from selenium.webdriver.remote.webdriver import WebDriver


def has_did_you_forget_title(driver: WebDriver):
    headers = driver.find_elements_by_tag_name("h1")
    for header in headers:
        if str(header.text).lower() == "before you checkout":
            return True
    return False


def get_continue_button_maybe(driver: WebDriver):
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if button.text == "Continue":
            return button
    return None


async def click_continue(driver: WebDriver):
    if not is_on_did_you_forget_page(driver):
        raise RuntimeError("not on the did-you-forget page")

    print("clicking through the did-you-forget page")
    get_continue_button_maybe(driver).click()


def is_on_did_you_forget_page(d: WebDriver):
    return bool(has_did_you_forget_title(d) and get_continue_button_maybe(d))
