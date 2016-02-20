#!/usr/bin/env python
import uinput
import time

events = (uinput.KEY_ENTER, uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT)
device = uinput.Device(events)

time.sleep(10)
device.emit(uinput.KEY_ENTER, 1)
time.sleep(0.1)
device.emit(uinput.KEY_ENTER, 0)
