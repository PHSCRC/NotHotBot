import time
import atexit

class Motor (object) :
#charlie
	def __init__ (self, motorNumber) :

		mh = Adafruit_MotorHAT(addr=0x60)
		    mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
		atexit.register(turnOffMotors)
