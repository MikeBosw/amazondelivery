import os

from mb.amazonslots.lib import phone


def _say(msg: str, *args, **kwargs):
    text = msg.format(*args, **kwargs)
    replacements = [('"', ""), ("\\", ""), ("$", ""), ("<(", "")]
    for a, b in replacements:
        text = text.replace(a, b)
    os.system('say "%s"' % text)


def tell_engineer(msg: str, *args, **kwargs):
    if not phone.send_message(msg.format(*args, **kwargs), phone.Audience.ENGINEERS):
        _say(msg, *args, **kwargs)


def tell_everyone(msg: str, *args, **kwargs):
    if not phone.send_message(msg.format(*args, **kwargs), phone.Audience.EVERYONE):
        _say(msg, *args, **kwargs)
