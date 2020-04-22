from selenium.webdriver.remote.webdriver import WebDriver


def is_on_slots_page(driver: WebDriver):
    html = str(driver.page_source)
    if "schedule your order" not in html.lower():
        return False
    if "select a location" not in html.lower():
        return False
    if "select a time" not in html.lower():
        return False
    return True


def is_slot_open(slot):
    price = slot.find_element_by_class_name("ufss-slot-price-container")
    if "not available" in str(price.text).lower():
        return False
    return True


def get_all_slots(driver: WebDriver):
    return driver.find_elements_by_class_name("ufss-slot-container")


def get_open_slots(driver: WebDriver):
    all_slots = get_all_slots(driver)
    return [s for s in all_slots if is_slot_open(s)]
