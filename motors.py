from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit

_mh = Adafruit_MotorHAT(addr=0x60)

_LEFT_NUM = 2
_LEFT_FORWARD = Adafruit_MotorHAT.BACKWARD
_LEFT_BACKWARD = Adafruit_MotorHAT.FORWARD
_left = _mh.getMotor(_LEFT_NUM)

_RIGHT_NUM = 1
_RIGHT_FORWARD = Adafruit_MotorHAT.BACKWARD
_RIGHT_BACKWARD = Adafruit_MotorHAT.FORWARD
_right = _mh.getMotor(_RIGHT_NUM)

_RELEASE = Adafruit_MotorHAT.RELEASE
_MAX = 150

FORWARD = 1
BACKWARD = 2


atexit.register(lambda: _left.run(_RELEASE))
atexit.register(lambda: _right.run(_RELEASE))

def _filter(speed):
    return _MAX if speed > _MAX else speed

def _stopMotor(motor):
    motor.run(_RELEASE)
    motor.setSpeed(0)

def leftStop():
    _stopMotor(_left)

def rightStop():
    _stopMotor(_right)

def bothStop():
    leftStop()
    rightStop()



def leftSet(speed, direction=None):
    if direction is None:
        direction = FORWARD if speed > 0 else BACKWARD
        speed = abs(speed)
    _left.setSpeed(_filter(speed))
    _left.run(_LEFT_FORWARD if direction == FORWARD else _LEFT_BACKWARD)

def rightSet(speed, direction=None):
    if direction is None:
        direction = FORWARD if speed > 0 else BACKWARD
        speed = abs(speed)
    _right.setSpeed(_filter(speed))
    _right.run(_RIGHT_FORWARD if direction == FORWARD else _RIGHT_BACKWARD)

def leftSetVar(speed):
    direction = FORWARD if speed > 0 else BACKWARD
    speed = abs(int(speed * _MAX))
    _left.setSpeed(_filter(speed))
    _left.run(_LEFT_FORWARD if direction == FORWARD else _LEFT_BACKWARD)

def rightSetVar(speed):
    direction = FORWARD if speed > 0 else BACKWARD
    speed = abs(int(speed * _MAX))
    _right.setSpeed(_filter(speed))
    _right.run(_RIGHT_FORWARD if direction == FORWARD else _RIGHT_BACKWARD)

    
def bothSet(*args):
    leftSet(*args)
    rightSet(*args)



def init():
    bothStop()
