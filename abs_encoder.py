import os
import functools
import atexit
import time

_path_req = 'lmao_encoder_req'
_path_resp = 'lmao_encoder_resp'
total_l = 0
total_r = 0


if not os.path.exists(_path_req) or not os.path.exists(_path_resp):
    raise RuntimeError("Encoder daemon is not running")
_req = open(_path_req, 'w')
print('acquired req')
_resp = open(_path_resp, 'r')
print('acquired resp')
def _cleanup():
    _req.close()
    _resp.close()
atexit.register(_cleanup)


def right():
    global total_r
    _req.write('right\n')
    _req.flush()
    res = _resp.readline().strip()
    while res == '':
        res = _resp.readline().strip()
        time.sleep(0.001)
    result = int(res)
    total_r += result
    print('right:', result)
    return result

def left():
    global total_l
    _req.write('left\n')
    _req.flush()
    res = _resp.readline().strip()
    while res == '':
        res = _resp.readline().strip()
        time.sleep(0.001)
    result = int(res)
    total_l += result
    print('left:', result)
    return result

def end():
    _req.write('end\n')
    _req.flush()

def clearLeft():
    global total_l
    total_l = 0

def clearRight():
    global total_r
    total_r = 0

def clearBoth():
    clearLeft()
    clearRight()

def totalLeft():
    return total_l

def totalRight():
    return total_r

def totalBoth():
    return total_l, total_r
