import wiringpi
import math, time

class HcSr04:
    PULSE_TRIGGER = 0.00001  # 10 μsec
    SPEED_OF_SOUND = 340  # 340 m/sec
    PULSE_TRIGGER_INTERVAL = 0.06  # 60 msec
    TIMEOUT = 2 * 180 * 0.01 / SPEED_OF_SOUND  # 0.0106 sec

    def __init__(self, trig, echo):
        self.trig = trig
        self.echo = echo
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(self.trig, wiringpi.OUTPUT)
        wiringpi.pinMode(self.echo, wiringpi.INPUT)
        wiringpi.digitalWrite(self.trig, wiringpi.LOW)
        time.sleep(1)

    def wait_for_echo(self, wait_value, wait_time):
        timeout = False
        start_time = time.time()
        current_time = start_time
        while wiringpi.digitalRead(self.echo) != wait_value:
            current_time = time.time()
            timeout = (current_time - start_time) > wait_time
            if timeout is True:
                break
        return current_time, not timeout

    def read(self):
        time.sleep(self.PULSE_TRIGGER_INTERVAL)
        wiringpi.digitalWrite(self.trig, wiringpi.HIGH)
        time.sleep(self.PULSE_TRIGGER)
        wiringpi.digitalWrite(self.trig, wiringpi.LOW)
        start_time, echo_result = self.wait_for_echo(wiringpi.HIGH, self.TIMEOUT)
        if echo_result:
            end_time, echo_result = self.wait_for_echo(wiringpi.LOW, self.TIMEOUT)
            if echo_result:
                return True, (end_time - start_time) * (self.SPEED_OF_SOUND * 1000 / 2)
            else:
                print("wait_for_echo(wiringpi.HIGH) error")
        else:
            print("wait_for_echo(wiringpi.LOW) error")
        return False, 0
