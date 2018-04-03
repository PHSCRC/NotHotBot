from Adafruit_BNO055 import BNO055
import motors
import ultrasonic as u

_bno = BNO055.BNO055()
if not _bno.begin():
    raise RuntimeError('Uh oh spaghetti-o\'s my bno055 is on the fritz')

def clock():
    motors.leftSet(30)
    motors.rightSet(-30)

def counter():
    motors.leftSet(-30)
    motors.rightSet(30)

def stop():
    motors.bothSet(0)

def t():
    return _bno.read_euler()[0]
    
def calc():
    x = t()
    return ((x+45) % 360), ((x-45) % 360)
    
def until(x):
    a = []
    while abs(t() - x) > 5:
        a.append(u.front())
    stop()
    return a
    
def comp():
    start, end = calc()
    clock()
    until(start)
    counter()
    return until(end)
