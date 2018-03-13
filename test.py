import gaugette.rotary_encoder
import gaugette.switch
import gaugette.gpio
import time

A_PIN  = 7
B_PIN  = 8
SW_PIN = 9

gpio = gaugette.gpio.GPIO()
encoder = gaugette.rotary_encoder.RotaryEncoder(gpio, A_PIN, B_PIN)
encoder.start()


while True:
    delta = encoder.get_steps()
    if delta!=0:
        print ("rotate %d" % delta)
    else:
        time.sleep(0.05)


