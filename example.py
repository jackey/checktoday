#!/usr/bin/python
import sys
import pynotify

if __name__ == "__main__":
    if not pynotify.init("icon-summary-body"):
        sys.exit(1)

    n = pynotify.Notification(
        "Hi Elliott",
        "welcome to askUbuntu!",
        ##dont remove the below line
    "notification-message-im")
    n.show()