#!/usr/bin/env python
import asyncio

from selenium import webdriver

from mb.amazonslots import pages
from mb.amazonslots.lib import alerts
from mb.amazonslots.lib.wfaf import FoodService
from mb.amazonslots.navigation import try_to_go
from mb.amazonslots.pages.slots import get_open_slots
from mb.amazonslots.setup import go_to_slots_page

SLOT_OPEN_MSG_FMT = (
    "{slots} slots for delivery are open! The time is now! "
    "Come and get a slot! This is it, folks! Oh boy. Oh wow."
)


async def main():
    driver = webdriver.Chrome()
    service = FoodService.WHOLE_FOODS

    if not await try_to_go(driver, pages.GUEST_PAGE):
        raise RuntimeError("failed to reach guest page")

    if not await try_to_go(driver, pages.SIGNED_IN_PAGE):
        raise RuntimeError("failed to reach signed-in home page")

    asyncio.ensure_future(announce_status_forever(service))
    await monitor_slots_forever(driver, service)


async def announce_status_forever(service: FoodService):
    alerts.tell_engineer("launching delivery slot monitor for {}", service)
    while True:
        await asyncio.sleep(60 * 90)
        alerts.tell_engineer("delivery slot monitor for {} is still alive", service)


async def monitor_slots_forever(driver, service: FoodService):
    prev_slot_count = None
    while True:
        await go_to_slots_page(driver, service)
        slot_count = len(get_open_slots(driver))
        print("%s slots available right now" % slot_count)
        if slot_count and not prev_slot_count:
            alerts.tell_everyone(SLOT_OPEN_MSG_FMT, slots=slot_count)
        elif prev_slot_count and not slot_count:
            alerts.tell_everyone("Slots became unavailable.")
        prev_slot_count = slot_count
        await asyncio.sleep(45)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
