#!/usr/bin/env python
import signal
import RPi.GPIO as GPIO
import time
import logging
from threading import Timer

logging.basicConfig(level=logging.DEBUG)

# main
# set signal
def signal_exit(signal, frame):
    print "\nexit gpiod ..."
    GPIO.cleanup()
    exit(0)

signal.signal(signal.SIGTERM, signal_exit)
signal.signal(signal.SIGINT, signal_exit)

def gpio_listener(pin, callback):
    callback(GPIO.input(pin))
    Timer(1.0, gpio_listener, kwargs={'pin': pin, 'callback': callback}).start()

def debug(message):
    print "debug", message


GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

gpio_listener(11, debug)

while True:
    GPIO.output(7, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(7, GPIO.LOW)
    time.sleep(1)
