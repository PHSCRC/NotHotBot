import RPi.GPIO as GPIO
import time
import sys
GPIO.setmode(GPIO.BCM)

TRIG = int(sys.argv[1])
ECHO = int(sys.argv[2])

print 'Measuring...'

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print 'Sensor Is Settling...'
time.sleep(2)

GPIO.output(TRIG, True)
time.sleep(0.00001)
GPIO.output(TRIG, False)

while GPIO.input(ECHO) == 0:
    pulse_start = time.time()

while GPIO.input(ECHO) == 1:
    pulse_end = time.time()
pulse_duration = pulse_end - pulse_start
distance = pulse_duration * 17150
distance = round(distance, 2)
print 'Distance:',distance,'cm'
