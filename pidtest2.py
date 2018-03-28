import encoder
import wpilib
import motors

total_l, total_r = 0, 0

lol2 = []

def inp(l, r):
    def fun():
        global total_l, total_r
        total_l += l.get_steps()
        total_r += r.get_steps()
        if total_r == 0 or total_l == 0:
            i = 1
        else:
            i = total_r / total_l
        if i > 10:
            return 10
        lol2.append(i)
        return i
    return fun

speed = 100

lol = []

def out(i):
    lol.append(i)
    motors.leftSet(int(speed * (1-i)) if i > 0 else speed)
    motors.rightSet(int(speed * (1+i)) if i < 0 else speed)
    

def create():
    l, r = encoder.createLeftRight()
    kp = 5
    ki = 1
    kd = 1
    kf = 1
    source = inp(l, r)
    output = out
    ctrlr = wpilib.PIDController(kp, ki, kd, kf, source, output)
    ctrlr.setInputRange(0, 10)
    ctrlr.setOutputRange(-1.0, 1.0)
    ctrlr.setAbsoluteTolerance(0.1)
    ctrlr.setContinuous()
    return ctrlr


def stop(c):
    c.disable()
    motors.bothSet(0)
    print(total_l, total_r)

def start(c):
    global total_l, total_r
    total_l = 0
    total_r = 0
    c.origSource()
    c.setSetpoint(1)
    c.enable()

def f(c):
    while not c.onTarget():
        pass

if __name__ == '__main__':
    create()
