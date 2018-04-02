from ultrasonicClass import Sensors
import Adafruit_TCS34725
import time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import RPi.GPIO as GPIO
import serial

class Robot():

    def __init__(self, left, right, versa):
        self.FRONT = 6
        self.LEFT = 1 #Good
        self.RIGHT = 5 #good
        self.FRONT_RIGHT = 3 #Good
        self.FRONT_LEFT = 4 #good
        self.REAR_RIGHT = 0 #good
        self.REAR_LEFT = 2
        self.LUX_CUTOFF = 250 #completely random
        self.FLAME_LED = 18
        self.START_LED = 23

        self.left = left
        self.right = right
        self._versa = versa
        self.sen = Sensors()
        self.tcs = Adafruit_TCS34725.TCS34725()
        self.tcs.set_interrupt(False)
        GPIO.setmode(GPIO.BCM)
        self.setupLeds()

        self.SERIAL_PORT = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)

    def setupLeds(self):
        GPIO.setup(self.FLAME_LED, GPIO.OUT)
        GPIO.setup(self.START_LED, GPIO.OUT)

    def cleanupLeds(self):
        GPIO.cleanup(self.FLAME_LED)
        GPIO.cleanup(self.START_LED)

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
        self._versa.setSpeed(255 if boolean else 0)
        self._versa.run(Adafruit_MotorHAT.FORWARD if boolean else Adafruit_MotorHAT.RELEASE)

    def readFlameSensor(self):
        curr = self.SERIAL_PORT.readline().decode().strip()
        
        try :
            int(curr)
        except ValueError :
            curr = -1 
        else :
            return int(curr)

    def waitForSoundStart(self):
        while True:
            curr = self.SERIAL_PORT.readline().decode().strip()
            print(curr)
            if curr == 'sound':
                return
            time.sleep(0.05)

    def startLed(self, boolean):
        GPIO.output(self.START_LED, boolean)

    def flameLed(self, boolean):
        GPIO.output(self.FLAME_LED, boolean)

    def readRoomLine(self):
        r, g, b, c = self.tcs.get_raw_data()
        print(Adafruit_TCS34725.calculate_lux(r, g, b))
        return Adafruit_TCS34725.calculate_lux(r, g, b)>self.LUX_CUTOFF

    def readFront(self):
        return self.sen.readSingleMetric(self.FRONT)

    def readLeft(self):
        return self.sen.readSingleMetric(self.LEFT)

    def readRight(self):
        return self.sen.readSingleMetric(self.RIGHT)

    def readFrontLeft(self):
        return self.sen.readSingleMetric(self.FRONT_LEFT)

    def readFrontRight(self):
        return self.sen.readSingleMetric(self.FRONT_RIGHT)

    def readRearRight(self):
        return self.sen.readSingleMetric(self.REAR_RIGHT)

    def readRearLeft(self):
        return self.sen.readSingleMetric(self.REAR_LEFT)

    def readAllUltras(self):
        return self.sen.readAllMetric()
