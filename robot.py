import ultrasonic as u
import Adafruit_TCS34725
from Adafruit_BNO055 import BNO055
import time
import motors
import abs_encoder as e
import wpilib
import RPi.GPIO as GPIO
import serial
import math

class Robot:
    def __init__(self):
        self.STEPS_PER_REV = 3200
        self.DISTANCE_PER_REV = 0.2827433388
        self.LUX_CUTOFF = 250 #completely random
        self.FLAME_LED = 18
        self.START_LED = 23
        self.ROTATION_KEY = 0.09

        self.bno = BNO055.BNO055()
        if not self.bno.begin():
            raise RuntimeError('Uh oh spaghetti-o\'s my bno055 is on the fritz')
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

    def readAngle(self):
        return self.bno.read_euler()[0]

    def straightForwardUntil(self, func, speed, pre1=None, pre2=None):
        u.stage()
        if pre1 is not None:
            pre1()
        total_l, total_r = 0, 0
        def inp():
            nonlocal total_l, total_r
            print(total_l, total_r)
            total_l += e.left()
            total_r += e.right()
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
        ctrlr.setSetpoint(1)
        inp()
        if pre2 is not None:
            pre2()
        motors.bothSet(speed)
        time.sleep(0.01)
        if func():
            motors.bothSet(0)
        ctrlr.enable()
        while not func():
            pass
        ctrlr.disable()
        motors.bothSet(0)
        u.unstage()

    def straightForwardForMeters(self, distance, speed):
        def pre():
            e.clearBoth()
        def condition():
            time.sleep(0.001)
            l, r = e.totalBoth()
            d = ((l + r) / 2) / self.STEPS_PER_REV * self.DISTANCE_PER_REV
            return d >= distance
        self.straightForwardUntil(condition, speed, pre2=pre)
        l, r = e.totalBoth()
        d = ((l + r) / 2) / self.STEPS_PER_REV * self.DISTANCE_PER_REV
        print(d)

    def rotateRightBy(self, angle, speed):
        u.stage()
        self.bno.begin()
        b = []
        def inp():
            r = [self.readAngle(), self.readAngle(), self.readAngle(), self.readAngle(), self.readAngle(),]
            res = sorted(r)[2]
            b.append(res)
            return res
        testval = inp()
        target = 90 - testval if testval < 15 else 90
        # target = (self.readAngle() + angle) % 360
        a = []
        def out(i):
            motors.leftSet(int(speed * i))
            motors.rightSet(-int(speed * i))
            a.append(i)

        kp = 0.0025
        ki = 0.001
        kd = 0.001
        kf = 0.001
        source = self.readAngle
        output = out
        ctrlr = wpilib.PIDController(kp, ki, kd, kf, source, output)
        ctrlr.setInputRange(0, 360)
        ctrlr.setOutputRange(-1.0, 1.0)
        ctrlr.setAbsoluteTolerance(1.0)
        ctrlr.setContinuous()
        ctrlr.setSetpoint(target)
        ctrlr.enable()
        while not ctrlr.onTarget():
            pass
        ctrlr.disable()
        motors.bothSet(0)
        u.unstage()
        print(a)
        print(b)

    def rotateRightUntil(self, func, speed, pre1=None, pre2=None):
        u.stage()
        if pre1 is not None:
            pre1()
        total_l, total_r = 0, 0
        def inp():
            nonlocal total_l, total_r
            print(total_l, total_r)
            total_l += e.left()
            total_r += e.right()
            if total_r == 0 or total_l == 0:
                i = 1
            else:
                ratio = -total_r / total_l
                adjust = abs(ratio - 1) / (total_l + -total_r)
                i = 1 + adjust if ratio > 1 else 1 - adjust
            if i > 10:
                return 10
            return i
        f = False
        def out(i):
            nonlocal f
            if f:
                print(i)
                motors.leftSet(int(speed * (1-i)) if i > 0 else speed)
                motors.rightSet(-(int(speed * (1+i)) if i < 0 else speed))
            else:
                f = True
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
        ctrlr.setSetpoint(1)
        inp()
        if pre2 is not None:
            pre2()
        motors.leftSet(speed)
        motors.rightSet(-speed)
        time.sleep(0.01)
        if func():
            motors.bothSet(0)
        ctrlr.enable()
        while not func():
            pass
        ctrlr.disable()
        motors.bothSet(0)
        u.unstage()

    def expRotateRightBy(self, angle, speed):
        steps = int((angle / 180 * math.pi * self.ROTATION_KEY) / self.DISTANCE_PER_REV * self.STEPS_PER_REV)
        def pre():
            e.clearBoth()
        def condition():
            time.sleep(0.001)
            l = e.totalLeft()
            return l >= steps
        self.rotateRightUntil(condition, speed, pre2=pre)

    def rotateLeftUntil(self, func, speed, pre1=None, pre2=None):
        u.stage()
        if pre1 is not None:
            pre1()
        total_l, total_r = 0, 0
        def inp():
            nonlocal total_l, total_r
            print(total_l, total_r)
            total_l += e.left()
            total_r += e.right()
            if total_r == 0 or total_l == 0:
                i = 1
            else:
                ratio = total_r / -total_l
                adjust = abs(ratio - 1) / (-total_l + total_r)
                i = 1 + adjust if ratio > 1 else 1 - adjust
            if i > 10:
                return 10
            return i
        f = False
        def out(i):
            nonlocal f
            if f:
                print(i)
                motors.leftSet(-(int(speed * (1-i)) if i > 0 else speed))
                motors.rightSet(int(speed * (1+i)) if i < 0 else speed)
            else:
                f = True
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
        ctrlr.setSetpoint(1)
        inp()
        if pre2 is not None:
            pre2()
        motors.leftSet(-speed)
        motors.rightSet(speed)
        time.sleep(0.01)
        if func():
            motors.bothSet(0)
        ctrlr.enable()
        while not func():
            pass
        ctrlr.disable()
        motors.bothSet(0)
        u.unstage()

    def expRotateLeftBy(self, angle, speed):
        steps = int((angle / 180 * math.pi * self.ROTATION_KEY) / self.DISTANCE_PER_REV * self.STEPS_PER_REV)
        def pre():
            e.clearBoth()
        def condition():
            time.sleep(0.001)
            r = e.totalRight()
            return r >= steps
        self.rotateLeftUntil(condition, speed, pre2=pre)
