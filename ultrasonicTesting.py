from hcsr04sensor import sensor
import time

TRIG = 13
ECHO = 6

v = sensor.Measurement(TRIG, ECHO)

def read() :
    return v.distance_metric(v.raw_distance())


while True :
    print(read())
    time.sleep(1)
