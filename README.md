Credit for the original idea goes to whoever made [this](https://github.com/pcomputo/Whole-Foods-Delivery-Slot).

The idea is that instead of repeatedly refreshing the Amazon Fresh delivery page, you run this program in the background, leaving it open until it announces that a slot has opened up.

If you give it Twilio account details you'll get an SMS text. Otherwise it uses the `say` command on your computer.

Requirements
---

* Amazon Fresh or Whole Foods
* Chrome WebDriver
* Python 3.8, but feel free to try a lower version and lmk how it goes
* either Twilio or a `say` command in your `PATH` environmennt variable

Installation
---

Optionally, create and activate a virtual env.

```
virtualenv -p /path/to/python3 ~/.virtualenvs/amazonslots
~/.virtualenvs/amazonslots
```

Clone this repo. Then, from within the repo...

`pip install -r requirements.txt`

Instructions
---

*NOTE: auto sign-in doesn't work when your 2FA is enabled.*

Create a file `python/username.secret` and `python/password.secret` to automate sign-in.

If you have Twilio, create a file `python/twilio_sid.secret` and `python/twilio_token.secret`, then follow the instructions in `python/phone_numbers.json.example`.

From within the repo, run...

```
PYTHONPATH=./python python python/mb/amazonslots/main.py
```

You should see Chrome launch and gradually proceed through all the screens to the delivery slot page. Keep an eye on the script's output in case it gets stuck. The slots page reloads automatically at regular intervals.

If you don't have Twilio, the `say` command is the mechanism for notifying you. On a Mac, `say` is a text-to-speech command and it comes with the OS. On other operating systems you'll probably need to change this part of the script - or add a `say` command to your `PATH` that does what you want.

Caveats
---

If Amazon thinks about contemplating the idea of the concept of the prospect of a change to their UX, this script will break.

