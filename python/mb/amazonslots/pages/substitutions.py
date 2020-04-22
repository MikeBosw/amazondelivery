from selenium.webdriver.remote.webdriver import WebDriver


def has_substitutions_title(driver: WebDriver):
    headers = driver.find_elements_by_tag_name("h1")
    for header in headers:
        if str(header.text).lower() == "substitution preferences":
            return True
    return False


def get_do_not_substitute_boxes(driver: WebDriver):
    return driver.find_elements_by_css_selector('[data-action="doNotSubItem"]')


def is_on_substitutions_page(driver: WebDriver):
    return has_substitutions_title(driver)


def click_all_do_not_substitute_boxes(driver: WebDriver):
    print("checking all do-not-substitute boxes")
    for box in get_do_not_substitute_boxes(driver):
        box.click()


def get_continue_button_maybe(driver: WebDriver):
    buttons = driver.find_elements_by_css_selector("span.a-button")
    for button in buttons:
        if button.text == "Continue":
            return button
    return None


async def click_continue(driver: WebDriver):
    if not is_on_substitutions_page(driver):
        raise RuntimeError("not on the substitutions page")
    click_all_do_not_substitute_boxes(driver)
    print("clicking through the substitutions page")
    get_continue_button_maybe(driver).click()
