import asyncio

from selenium.webdriver.remote.webdriver import WebDriver

from mb.amazonslots import pages
from mb.amazonslots.lib import alerts
from mb.amazonslots.lib.wfaf import FoodService
from mb.amazonslots.navigation import current_page, try_to_go
from mb.amazonslots.navigation.navigation import go_or_throw
from mb.amazonslots.pages import NO_PAGE, CART_PAGE, cart

CRY_FOR_HELP = "Oh lord. The slots page went away. Awaiting human assistance."


async def go_to_slots_page(d: WebDriver, service: FoodService):
    slots_page = pages.SLOTS_PAGE_BY_FOOD_SERVICE[service]
    if current_page(d) == slots_page:
        # already here; just refresh the page
        if await try_to_go(d, slots_page):
            return
        else:
            print("attempted to refresh slots page; ended up somewhere else")
    interim_pages = [
        pages.CART_PAGE,
        pages.DID_YOU_FORGET_PAGE,
        pages.SUBSTITUTIONS_PAGE,
    ]
    attempts = 0
    while attempts < 3:
        attempts += 1
        await go_or_throw(d, pages.CART_PAGE)
        await wait_for_cart_items(d, service)
        # yes, we try to get past the interim pages a few times in a row
        if current_page(d) in interim_pages and await try_to_go(d, slots_page):
            break
        if current_page(d) in interim_pages and await try_to_go(d, slots_page):
            break
        if current_page(d) in interim_pages and await try_to_go(d, slots_page):
            break
        if current_page(d) == pages.RECOMMENDATIONS_PAGE:
            # this page offers no way forward to the slots page; start over.
            print("reached annoying recommendations page; waiting 3s to retry")
            await asyncio.sleep(3)
            continue
        if current_page(d) not in interim_pages:
            msg = "tried to reach the slots page, ended up here unexpectedly:"
            raise RuntimeError(msg, current_page(d))
        print("failed to reach slots page (attempt %s/3)" % attempts)

    if current_page(d, pages.GUEST_PAGE) != slots_page:
        alerts.tell_engineer(CRY_FOR_HELP)
        while current_page(d, pages.GUEST_PAGE) != slots_page:
            await asyncio.sleep(3)


async def wait_for_cart_items(driver: WebDriver, service: FoodService):
    if current_page(driver, NO_PAGE) != CART_PAGE:
        raise RuntimeError("not on cart page")
    while not cart.get_cart_state(driver).is_cart_ready(service):
        # this means a live, editable order is already in the cart, or that
        # the cart is empty. either way, just spin here until it changes.
        print("waiting for %s cart to fill up or become unmodifiable" % service)
        await go_or_throw(driver, CART_PAGE)
        await asyncio.sleep(30)
