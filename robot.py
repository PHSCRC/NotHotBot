from ultrasonicClass import Sensors
import Adafruit_TCS34725
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import RPi.GPIO as GPIO
import serial

class Robot():

    FRONT = 0
    LEFT = 1
    RIGHT = 2
    FRONT_RIGHT = 3
    FRONT_LEFT = 4
    REAR_RIGHT = 5
    REAR_LEFT = 6
    LUX_CUTOFF = 50 #completely random
    FLAME_LED = 18
    START_LED = 23
    SERIAL_PORT = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)

    def __init__(self, left, right, versa):
        self.left = left
        self.right = right
        self.versa = versa
        self.sen = Sensors()
        self.tcs = Adafruit_TCS34725.TCS34725()
        self.tcs.set_interrupt(False)
        GPIO.setmode(GPIO.BCM)
        setupLeds()

    def setupLeds():
        GPIO.setup(FLAME_LED, GPIO.OUT)
        GPIO.setup(START_LED, GPIO.OUT)

    def cleanupLeds():
        GPIO.cleanup(FLAME_LED)
        GPIO.cleannup(START_LED)

    def goStraight(self, distance):
        pass

    def goStraight(self):
        pass

    def stop(self):
        pass

    def turnLeft90(self):
        turnLeft(90)

    def turnRight90(self):
        turnRight(90)

    def turnLeft(self, angle):
        pass

    def turnRight(self, angle):
        pass

    def versa(self, boolean):
        self.versa.setSpeed(255 if boolean else 0)
        self.versa.run(Adafruit_MotorHAT.FORWARD if boolean else Adafruit_MotorHAT.RELEASE)

    def readFlameSensor(self):
        curr = SERIAL_PORT.readline().decode().strip()
        return int(curr)

    def waitForSoudStart(self):
        while True:
            curr = SERIAL_PORT.readline().decode().strip()
            if curr == 'sound':
                return
            delay(50)

    def startLed(self, boolean):
        GPIO.output(START_LED, boolean)

    def flameLed(self, boolean):
        GPIO.output(FLAME_LED, boolean)

    def readRoomLine(self):
        r, g, b, c = self.tcs.get_raw_data()
        print(Adafruit_TCS34725.calculate_lux(r, g, b))
        return Adafruit_TCS34725.calculate_lux(r, g, b)>LUX_CUTOFF

    def readFront(self):
        return self.sen.readSingleMetric(FRONT)

    def readLeft(self):
        return self.sen.readSingleMetric(LEFT)

    def readRight(self):
        return self.sen.readSingleMetric(RIGHT)

    def readFrontLeft(self):
        return self.sen.readSingleMetric(FRONT_LEFT)

    def readFrontRight(self):
        return self.sen.readSingleMetric(FRONT_RIGHT)

    def readRearRight(self):
        return self.sen.readSingleMetric(REAR_RIGHT)

    def raedRearLeft(self):
        return self.sen.readSingleMetric(REAR_LEFT)

    def readAllUltras(self):
        return self.sen.readAllMetric()
