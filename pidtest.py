import encoder
import wpilib
import motors

total = 0

def inp(l, r):
    def fun():
        global total
        i = l.get_steps() + r.get_steps()
        total += i
        if i > 1000:
            return 1000
        if i < -1000:
            return -1000
        return i
    return fun

lol = []

def create():
    l, r = encoder.createLeftRight()
    kp = 5
    ki = 1
    kd = 1
    kf = 1
    source = inp(l, r)
    output = lambda x: motors.bothSetVar(x) or lol.append(x)
    ctrlr = wpilib.PIDController(kp, ki, kd, kf, source, output)
    ctrlr.setInputRange(-1000, 1000)
    ctrlr.setOutputRange(-1.0, 1.0)
    ctrlr.setAbsoluteTolerance(10)
    ctrlr.setContinuous()
    return ctrlr


def stop(c):
    print(total)
    c.disable()
    motors.bothSet(0)

def start(c):
    global total
    total = 0
    c.origSource()
    c.enable()

def f(c):
    while not c.onTarget():
        pass

if __name__ == '__main__':
    create()
