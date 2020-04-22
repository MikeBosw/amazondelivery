from typing import Callable

from selenium.webdriver.chrome.webdriver import WebDriver

from mb.amazonslots.lib.wfaf import FoodService
from mb.amazonslots.pages.base import is_on_guest_page, is_on_signed_in_page
from mb.amazonslots.pages.cart import is_on_cart_page
from mb.amazonslots.pages.did_you_forget import is_on_did_you_forget_page
from mb.amazonslots.pages.recommendations import is_on_recommendations_page
from mb.amazonslots.pages.sign_in_again import is_on_sign_in_again_page
from mb.amazonslots.pages.slots import is_on_slots_page
from mb.amazonslots.pages.substitutions import is_on_substitutions_page


class Page(object):
    def __init__(
        self,
        name: str,
        is_on_page: Callable[[WebDriver], bool],
        is_signed_in: bool = True,
    ):
        self.name = name
        self.is_on_page = is_on_page
        self.is_signed_in = is_signed_in

    def __repr__(self) -> str:
        return "<Page: %s>" % self.name


NO_PAGE = Page("[no page]", lambda _: False, is_signed_in=False)
GUEST_PAGE = Page("GUEST_PAGE", is_on_guest_page, is_signed_in=False)
SIGNED_IN_PAGE = Page("SIGNED_IN_PAGE", is_on_signed_in_page)
CART_PAGE = Page("CART_PAGE", is_on_cart_page)
RECOMMENDATIONS_PAGE = Page("RECOMMENDATIONS_PAGE", is_on_recommendations_page)
DID_YOU_FORGET_PAGE = Page("DID_YOU_FORGET_PAGE", is_on_did_you_forget_page)
SLOTS_PAGE_WF = Page("SLOTS_PAGE_WHOLE_FOODS", is_on_slots_page)
SLOTS_PAGE_AF = Page("SLOTS_PAGE_AMAZON_FRESH", is_on_slots_page)
SIGN_IN_AGAIN_PAGE = Page("SIGN_IN_AGAIN_PAGE", is_on_sign_in_again_page)
SUBSTITUTIONS_PAGE = Page("SUBSTITUTIONS", is_on_substitutions_page)

SLOTS_PAGE_BY_FOOD_SERVICE = {
    FoodService.AMAZON_FRESH: SLOTS_PAGE_AF,
    FoodService.WHOLE_FOODS: SLOTS_PAGE_WF,
}
