import json
import os
from enum import Enum
from typing import Tuple, Optional, List, NewType
from twilio.rest import Client

PhoneNumber = NewType("PhoneNumber", str)

_INIT = False
_CLIENT: Optional[Client] = None
__PHONE_NUMBERS = None
TWILIO_SID_PATH = "twilio_sid.secret"
TWILIO_TOKEN_PATH = "twilio_token.secret"
PHONE_NUMBERS_PATH = "phone_numbers.json.secret"


class Audience(Enum):
    EVERYONE = 0
    ENGINEERS = 1


class PhoneNumbers(object):
    def __init__(
        self, engineers: List[PhoneNumber], users: List[PhoneNumber], app: PhoneNumber
    ):
        self.engineers = [e for e in set(engineers)]
        self.users = [u for u in set(users)]
        self.app = app

    def get(self, audience: Audience):
        if audience == Audience.ENGINEERS:
            return self.engineers
        elif audience == Audience.EVERYONE:
            return self.users + self.engineers
        else:
            raise RuntimeError("unrecognized audience type: %s", audience)


def _phone_numbers() -> Optional[PhoneNumbers]:
    return __PHONE_NUMBERS


def _init():
    global _CLIENT, _INIT, __PHONE_NUMBERS
    if not _INIT:
        __PHONE_NUMBERS = _get_phone_numbers_maybe()
        _CLIENT = _create_client_maybe()
        _INIT = True


def _create_client_maybe():
    credentials = _get_credentials_maybe()
    if not credentials:
        return None
    phone_numbers = _get_phone_numbers_maybe()
    if not phone_numbers:
        return None
    account_sid, auth_token = credentials
    return Client(account_sid, auth_token)


def _get_phone_numbers_maybe() -> Optional[PhoneNumbers]:
    if not os.path.exists(PHONE_NUMBERS_PATH):
        return None
    with open(PHONE_NUMBERS_PATH) as pnf:
        numbers = json.load(pnf)
    return PhoneNumbers(numbers["engineers"], numbers["users"], numbers["app"])


def _get_credentials_maybe() -> Optional[Tuple[str, str]]:
    if not os.path.exists(TWILIO_SID_PATH) or not os.path.exists(TWILIO_TOKEN_PATH):
        return None
    with open(TWILIO_SID_PATH) as tf:
        sid = tf.read().strip()
    with open(TWILIO_TOKEN_PATH) as tf:
        token = tf.read().strip()
    return sid, token


def send_message(msg: str, audience: Audience) -> bool:
    _init()
    if not _CLIENT:
        return False
    numbers = _phone_numbers()
    for recipient in numbers.get(audience):
        result = _CLIENT.messages.create(to=recipient, from_=numbers.app, body=msg)
        print("sent msg %s to %s: %s" % (result.sid, recipient, msg))
    return True
