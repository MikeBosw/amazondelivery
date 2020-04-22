Credit for the idea goes to https://github.com/pcomputo/Whole-Foods-Delivery-Slot.

The idea is that instead of repeatedly refreshing the Amazon Fresh delivery page, you run this program in the background, leaving it open until it announces that a slot has opened up.

If you give it Twilio account details you'll get an SMS text. Otherwise it uses the "say" command on your computer.

Requirements
---

Amazon Fresh.

Chrome WebDriver.

Python 3.8. With lower versions of Python ymmv.

A command called `say` in your `PATH` variable that takes written English as input and communicates it to you. For example, on OS X, the `say` command is a built-in text-to-speech program that will literally say the words it's given out loud using your computer's audio.

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

From within the repo, run...

```
cd python
python mb/amazonslots/main.py
```

Chrome should launch. You will have to log in manually - at least the first time. Once logged in, you should be navigated through a couple screens to the Amazon Fresh delivery window page.

Leave Chrome running. The page reloads automatically at regular intervals.

Note that the `say` command is the mechanism for notifying you. On a Mac, `say` is a text-to-speech command and it comes with the OS. On other operating systems you'll probably need to change this part of the script - or add a `say` command to your `PATH` that does what you want.

Caveats
---

If Amazon thinks about contemplating the idea of the concept of the prospect of a change to their UX, this script will break.

