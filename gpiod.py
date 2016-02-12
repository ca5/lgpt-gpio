#!/usr/bin/env python
import signal
import RPi.GPIO as GPIO
import time
import logging
from threading import Timer
import uinput

logging.basicConfig(level=logging.DEBUG)
BLINK_FLG = True
GPIO_STAT = {}

# main
# set signal
def signal_exit(signal, frame):
    print "\nexit gpiod ..."
    GPIO.cleanup()
    exit(0)

def gpio_listener(pin, callback):
    callback(pin, GPIO.input(pin))
    Timer(0.01, gpio_listener, kwargs={'pin': pin, 'callback': callback}).start()

def blink_gpio(pin):
    global BLINK_FLG
    if BLINK_FLG:
        GPIO.output(7, GPIO.LOW)
        BLINK_FLG = False
    else:
        GPIO.output(7, GPIO.HIGH)
        BLINK_FLG = True
    Timer(1.0, blink_gpio, [pin]).start()


def push_j(pin, stat):
    if GPIO_STAT[pin] != stat:
        device.emit(uinput.KEY_J, stat)
        GPIO_STAT[pin] = stat

# set signal
signal.signal(signal.SIGTERM, signal_exit)
signal.signal(signal.SIGINT, signal_exit)

# make device
events = (uinput.KEY_ENTER, uinput.KEY_J, uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT, uinput.KEY_RIGHT)
device = uinput.Device(events)

# for activate Piggy tracker
device.emit(uinput.KEY_ENTER, 1)
time.sleep(0.1)
device.emit(uinput.KEY_ENTER, 0)

# initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO_STAT[11] = GPIO.LOW

# listen GPIO in background
gpio_listener(11, push_j)
blink_gpio(7)

while True:
    time.sleep(10)
    #if GPIO.input(11) == 1:
    #    device.emit(uinput.KEY_J, 1)
    #    time.sleep(0.1)
    #    device.emit(uinput.KEY_J, 0)
