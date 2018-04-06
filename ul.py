import RPi.GPIO as GPIO
import math, time

GPIO.setmode(GPIO.BCM)

class HcSr04:
    PULSE_TRIGGER = 0.00001  # 10 μsec
    SPEED_OF_SOUND = 340  # 340 m/sec
    PULSE_TRIGGER_INTERVAL = 0.06  # 60 msec
    TIMEOUT = 2 * 180 * 0.01 / SPEED_OF_SOUND  # 0.0106 sec

    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, GPIO.LOW)

    def wait_for_echo(self, wait_value, wait_time):
        timeout = False
        start_time = time.time()
        current_time = start_time
        while GPIO.input(self.echo) != wait_value:
            current_time = time.time()
            timeout = (current_time - start_time) > wait_time
            if timeout is True:
                break
        return current_time, not timeout

    def read(self):
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)
        GPIO.output(self.trig, GPIO.LOW)
        time.sleep(self.PULSE_TRIGGER_INTERVAL)
        GPIO.output(self.trig, GPIO.HIGH)
        time.sleep(self.PULSE_TRIGGER)
        GPIO.output(self.trig, GPIO.LOW)
        start_time, echo_result = self.wait_for_echo(GPIO.HIGH, self.TIMEOUT)
        if echo_result:
            end_time, echo_result = self.wait_for_echo(GPIO.LOW, self.TIMEOUT)
            if echo_result:
                return True, (end_time - start_time) * (self.SPEED_OF_SOUND * 1000 / 2)
            else:
                print("wait_for_echo(GPIO.HIGH) error")
        else:
            print("wait_for_echo(GPIO.LOW) error")
        return False, 0
