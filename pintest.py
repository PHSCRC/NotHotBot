#!/usr/bin/env python3

import RPi.GPIO as GPIO
import sys
import time

def callback(pin):
    out = GPIO.input(pin)
    print(pin, out)

def main(pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    GPIO.add_event_detect(pin, GPIO.BOTH, callback=callback)
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main(int(sys.argv[1]))
