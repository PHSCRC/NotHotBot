import ultrasonic as u
import Adafruit_TCS34725
import time
import motors
import encoder
import wpilib
import RPi.GPIO as GPIO
import serial

class Robot:
    def __init__(self):
        self.LUX_CUTOFF = 250 #completely random
        self.FLAME_LED = 18
        self.START_LED = 23

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
        return u.front()

    def readLeft(self):
        return u.left()

    def readRight(self):
        return u.right()

    def readFrontLeft(self):
        return u.front_left()

    def readFrontRight(self):
        return u.front_right()

    def readRear(self):
        return u.rear()

    def readAllUltras(self):
        return u.all()

    def straightForwardUntil(self, func, speed):
        total_l, total_r = 0, 0
        l, r = encoder.getLeftRight()
        def inp():
            nonlocal total_l, total_r
            print(total_l, total_r)
            total_l += l.get_steps()
            total_r += r.get_steps()
            if total_r == 0 or total_l == 0:
                i = 1
            else:
                i = total_r / total_l
            if i > 10:
                return 10
            return i
        def out(i):
            motors.leftSet(int(speed * (1-i)) if i > 0 else speed)
            motors.rightSet(int(speed * (1+i)) if i < 0 else speed)
        kp = 5
        ki = 1
        kd = 1
        kf = 1
        source = inp
        output = out
        ctrlr = wpilib.PIDController(kp, ki, kd, kf, source, output)
        ctrlr.setInputRange(0, 10)
        ctrlr.setOutputRange(-1.0, 1.0)
        ctrlr.setAbsoluteTolerance(0.1)
        ctrlr.setContinuous()
        ctrlr.origSource()
        ctrlr.setSetpoint(1)
        motors.bothSet(speed)
        time.sleep(0.01)
        if func():
            motors.bothSet(0)
        ctrlr.enable()
        while not func():
            pass
        ctrlr.disable()
        motors.bothSet(0)
