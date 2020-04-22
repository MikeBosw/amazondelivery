import asyncio
from typing import Dict, Tuple, Optional, Callable, Awaitable

from selenium.webdriver.remote.webdriver import WebDriver

from mb.amazonslots.lib.auth import is_signed_in, sign_in, persist_cookies
from mb.amazonslots.pages import (
    CART_PAGE,
    RECOMMENDATIONS_PAGE,
    SLOTS_PAGE_WF,
    SLOTS_PAGE_AF,
    DID_YOU_FORGET_PAGE,
    SIGN_IN_AGAIN_PAGE,
    SIGNED_IN_PAGE,
    GUEST_PAGE,
    Page,
    did_you_forget,
    NO_PAGE,
    cart,
    SUBSTITUTIONS_PAGE,
    substitutions,
)
from mb.amazonslots.pages.base import jump_to_guest_page
from mb.amazonslots.pages.cart import jump_to_cart_page

_LAST_SLOTS_PAGE_ATTEMPT: Optional[Page] = None

_PAGE_GUESSES = [
    CART_PAGE,
    RECOMMENDATIONS_PAGE,
    DID_YOU_FORGET_PAGE,
    SUBSTITUTIONS_PAGE,
    SIGN_IN_AGAIN_PAGE,
    SIGNED_IN_PAGE,
    GUEST_PAGE,
]

# the value None as the 1st element of a tuple means a transition from anywhere
TRANSITIONS: Dict[
    Tuple[Optional[Page], Page], Callable[[WebDriver], Awaitable[None]]
] = {
    (None, GUEST_PAGE): jump_to_guest_page,
    (None, CART_PAGE): jump_to_cart_page,
    (DID_YOU_FORGET_PAGE, SLOTS_PAGE_WF): did_you_forget.click_continue,
    (DID_YOU_FORGET_PAGE, SLOTS_PAGE_AF): did_you_forget.click_continue,
    (CART_PAGE, SLOTS_PAGE_AF): cart.click_af_checkout,
    (CART_PAGE, SLOTS_PAGE_WF): cart.click_wf_checkout,
    (SUBSTITUTIONS_PAGE, SLOTS_PAGE_WF): substitutions.click_continue,
}


def current_page(driver: WebDriver, default=None):
    """
    Returns the current page, or default if the current page can't be determined
    and default is not None. If default is None and the current page can't be
    determined, raises an error. If you want a None-like value to be returned
    instead of an error being raised, use pages.NO_PAGE.
    """
    if _LAST_SLOTS_PAGE_ATTEMPT is not None:
        if _LAST_SLOTS_PAGE_ATTEMPT.is_on_page(driver):
            return _LAST_SLOTS_PAGE_ATTEMPT
    for page in _PAGE_GUESSES:
        if page.is_on_page(driver):
            return page
    if default is None:
        raise RuntimeError("could not determine what the current page is")
    return default


async def go_or_throw(driver: WebDriver, there: Page):
    if not await try_to_go(driver, there):
        raise RuntimeError("was unable to go to %s" % there)


async def try_to_go(driver: WebDriver, there: Page) -> bool:
    result = await _try_to_go(driver, there)
    print("arrived at %s" % current_page(driver, NO_PAGE))
    return result


async def _try_to_go(driver, there):
    here = current_page(driver, NO_PAGE)
    print("attempting to go from %s to %s" % (here, there))
    if there == SLOTS_PAGE_AF or there == SLOTS_PAGE_WF:
        # this ugliness is 'cuz the AF and WF slots pages are indistinguishable
        global _LAST_SLOTS_PAGE_ATTEMPT
        _LAST_SLOTS_PAGE_ATTEMPT = there
    if here == there:
        # this is just a page refresh
        driver.get(driver.current_url)
        return current_page(driver, NO_PAGE) == there
    if not here.is_signed_in and there is not GUEST_PAGE:
        await sign_in(driver)
        here = current_page(driver)
    if here == there:
        # the sign-in sufficed
        return True
    if (here, there) in TRANSITIONS:
        transition = TRANSITIONS[(here, there)]
    elif (None, there) in TRANSITIONS:
        transition = TRANSITIONS[(None, there)]
    else:
        raise RuntimeError(
            "tried to get from %s to %s but found no route" % (here, there)
        )
    await transition(driver)
    if is_signed_in(driver):
        persist_cookies(driver)
    # this delay seems necessary sometimes for accurate get_current_page
    await asyncio.sleep(1)
    return current_page(driver, NO_PAGE) == there
