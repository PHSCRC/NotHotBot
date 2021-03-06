import curses
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import atexit
import ultrasonic as u
import time

mh = Adafruit_MotorHAT(addr=0x60)

ul = []
last = None

U = ord('u')
W = ord('w')
A = ord('a')
S = ord('s')
D = ord('d')
Q = ord('q')
E = ord('e')
Z = ord('z')
X = ord('x')
C = ord('c')
F = ord('f')
G = ord('g')
V = ord('v')
B = ord('b')
ONE = ord('1')
TWO = ord('2')
THREE = ord('3')
FOUR = ord('4')
FIVE = ord('5')

def print(*args):
    pass

right = mh.getMotor(1)
left = mh.getMotor(2)
speed = 100

def turnOffMotors():
    # pass
    left.run(Adafruit_MotorHAT.RELEASE)
    right.run(Adafruit_MotorHAT.RELEASE)

def forward(speed):
    print('forward')
    left.run(Adafruit_MotorHAT.FORWARD)
    right.run(Adafruit_MotorHAT.FORWARD)
    left.setSpeed(speed)
    right.setSpeed(speed)

def backward(speed):
    print('backward')
    left.run(Adafruit_MotorHAT.BACKWARD)
    right.run(Adafruit_MotorHAT.BACKWARD)
    left.setSpeed(speed)
    right.setSpeed(speed)

def turnleft(speed):
    print('left')
    speed = 75
    left.run(Adafruit_MotorHAT.BACKWARD)
    right.run(Adafruit_MotorHAT.FORWARD)
    left.setSpeed(speed)
    right.setSpeed(speed)

def turnright(speed):
    print('right')
    speed = 75
    left.run(Adafruit_MotorHAT.FORWARD)
    right.run(Adafruit_MotorHAT.BACKWARD)
    left.setSpeed(speed)
    right.setSpeed(speed)

def forright(speed):
    s2 = int(0.75 * speed)
    left.run(Adafruit_MotorHAT.FORWARD)
    right.run(Adafruit_MotorHAT.FORWARD)
    left.setSpeed(speed)
    right.setSpeed(s2)

def forleft(speed):
    s2 = int(0.75 * speed)
    left.run(Adafruit_MotorHAT.FORWARD)
    right.run(Adafruit_MotorHAT.FORWARD)
    left.setSpeed(s2)
    right.setSpeed(speed)

def for2right(speed):
    s2 = int(0.25 * speed)
    left.run(Adafruit_MotorHAT.FORWARD)
    right.run(Adafruit_MotorHAT.FORWARD)
    left.setSpeed(speed)
    right.setSpeed(s2)

def for2left(speed):
    s2 = int(0.25 * speed)
    left.run(Adafruit_MotorHAT.FORWARD)
    right.run(Adafruit_MotorHAT.FORWARD)
    left.setSpeed(s2)
    right.setSpeed(speed)


def smallLeft():
    turnleft(51)
    time.sleep(.1)
    turnOffMotors()

def smallForward():
    forward(51)
    time.sleep(.1)
    turnOffMotors()

def smallRight():
    turnright(51)
    time.sleep(.1)
    turnOffMotors()


def ultra(scr):
    global last
    fit = lambda x: '{:1.3f}'.format(x)
    x = str(list(map(fit, u.all())))
    if '3.000' in x or '0.000' in x:
        ul.append(last + ' l')
        ul.append(x)
    last = x
    scr.addstr(4, 10, x)
    scr.refresh()


def stop():
    print('stop')
    left.run(Adafruit_MotorHAT.BACKWARD)
    right.run(Adafruit_MotorHAT.FORWARD)
    left.setSpeed(0)
    right.setSpeed(0)

def main():
    atexit.register(curses.endwin)
    scr = curses.initscr()
    curses.cbreak()
    curses.setsyx(-1, -1)
    # scr.keypad(1)
    scr.addstr(0, 10, 'debug_control.py: the ultimate boxbot controller')
    scr.addstr(2, 10, 'Press Q to exit.')
    scr.refresh()
    speed = 100

    while True:
        key = scr.getch()

        if key == Q:
            turnOffMotors()
            with open('ultra_out.txt', 'w') as f:
                for i in ul:
                    f.write(i)
                    f.write('\n')
            break
        elif key == W:
            forward(speed)
        elif key == S:
            backward(speed)
        elif key == V:
            turnleft(speed)
        elif key == B:
            turnright(speed)
        elif key == Z:
            smallLeft()
        elif key == X:
            smallForward()
        elif key == C:
            smallRight()
        elif key == F:
            forleft(speed)
        elif key == G:
            forright(speed)
        elif key == A:
            for2left(speed)
        elif key == D:
            for2right(speed)
        elif key == E:
            stop()
        elif key == ONE:
            speed = 51
        elif key == TWO:
            speed = 51*2
        elif key == THREE:
            speed = 51*3
        elif key == FOUR:
            speed = 51*4
        elif key == U:
            ultra(scr)
        else:
            print("not a valid key")

    curses.endwin()

if __name__ == '__main__':
    main()

