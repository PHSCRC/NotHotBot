#----------------------------------------------------------------------
# Based on:
# rotary_encoder.py from https://github.com/guyc/py-gaugette
# Guy Carpenter, Clearwater Software
#

import math
import threading

import RPi.GPIO as GPIO

class Encoder:

    def __init__(self, a_pin, b_pin, debug=False):
        self.debug = debug
        self.a_pin = a_pin
        self.b_pin = b_pin
        self._steps = 0
        self._last_delta = 0
        self.lock = threading.Lock()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(a_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(b_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        # steps_per_cycle and self.remainder are only used in get_cycles which
        # returns a coarse-granularity step count.  By default
        # steps_per_cycle is 4 as there are 4 steps per
        # detent on my encoder, and get_cycles() will return a signed
        # count of full detent steps.
        self._steps_per_cycle = 4
        self._remainder = 0


    def _rotation_sequence(self):
        return (self.a_last ^ self.b_last) | self.b_last << 1

    def _update(self):
        delta = 0
        r_seq = self._rotation_sequence()
        if r_seq != self.r_seq:
            delta = (r_seq - self.r_seq) % 4
            if delta == 3:
                delta = -1
            elif delta == 2:
                delta = int(math.copysign(delta, self._last_delta))  # same direction as previous, 2 steps

            self._last_delta = delta
            self.r_seq = r_seq
        self._steps += delta

    def start(self):
        def a_update(channel):
            temp = GPIO.input(channel)
            with self.lock:
                self.a_last = temp
                self._update()
            if self.debug:
                print('A')
        def b_update(channel):
            temp = GPIO.input(channel)
            with self.lock:
                self.b_last = temp
                self._update()
            if self.debug:
                print('B')
        self.a_last = GPIO.input(self.a_pin)
        self.b_last = GPIO.input(self.b_pin)
        self.r_seq = self._rotation_sequence()
        GPIO.add_event_detect(self.a_pin, GPIO.BOTH, callback=a_update)
        GPIO.add_event_detect(self.b_pin, GPIO.BOTH, callback=b_update)

    def get_steps(self):
        with self.lock:
            steps = self._steps
            self._steps = 0
        return steps

    # get_cycles returns a scaled down step count to match (for example)
    # the detents on an encoder switch.  If you have 4 delta steps between
    # each detent, and you want to count only full detent steps, use
    # get_cycles() instead of get_delta().  It returns -1, 0 or 1.  If
    # you have 2 steps per detent, set encoder.steps_per_cycle to 2
    # before you call this method.
    def get_cycles(self):
        self._remainder += self.get_steps()
        cycles = self._remainder // self._steps_per_cycle
        self._remainder %= self._steps_per_cycle # remainder always remains positive
        return cycles


def createLeftRight():
    l, r = Encoder(27, 22), Encoder(17, 19)
    l.start()
    r.start()
    return l, r
