from gpiozero import DistanceSensor
from ul import HcSr04

_sensor_defs = {
    'FRONT': (5, 0),
    'FRONT_RIGHT': (24, 25),
    'FRONT_LEFT': (9, 10),
    'RIGHT': (1, 7),
    'LEFT': (20, 21),
    'BACK': (13, 6),
}

_sensors = {
    'FRONT': None,
    'FRONT_RIGHT': None,
    'FRONT_LEFT': None,
    'RIGHT': None,
    'LEFT': None,
    'BACK': None,
}

_tl_sensors = {k: HcSr04(v[0], v[1]) for k, v in _sensor_defs.items()}

def _makeSensor(trig, echo):
    return DistanceSensor(trigger=trig, echo=echo, max_distance=3, queue_len=3)

def enableAll():
    for k, v in _sensor_defs.items():
        _sensors[k] = _makeSensor(*v)

def disableAll():
    for k, v in _sensor_defs.items():
        _sensors[k]._read = lambda: 0.0
    # do the above first to give some delay
    for k, v in _sensor_defs.items():
        _sensors[k].close()
        _sensors[k] = None

def _enable(sensorName):
    if _sensors[sensorName] is not None:
        raise RuntimeError(sensorName + ' already enabled')
    _sensors[sensorName] = _makeSensor(*_sensor_defs[sensorName])

def _makeEnable(sensorName):
    def f():
        _enable(sensorName)
    return f

en_front = _makeEnable('FRONT')
en_front_right = _makeEnable('FRONT_RIGHT')
en_front_left = _makeEnable('FRONT_LEFT')
en_right = _makeEnable('RIGHT')
en_left = _makeEnable('LEFT')
en_back = _makeEnable('BACK')

def _makeDisable(sensorName):
    def f():
        _sensors[sensorName]._read = lambda: 0.0
        _sensors[sensorName].close()
        _sensors[sensorName] = None
    return f

dis_front = _makeDisable('FRONT')
dis_front_right = _makeDisable('FRONT_RIGHT')
dis_front_left = _makeDisable('FRONT_LEFT')
dis_right = _makeDisable('RIGHT')
dis_left = _makeDisable('LEFT')
dis_back = _makeDisable('BACK')

def _makeFunc(sensorName):
    def f():
        return _sensors[sensorName].distance
    return f

front = _makeFunc('FRONT')
front_right = _makeFunc('FRONT_RIGHT')
front_left = _makeFunc('FRONT_LEFT')
right = _makeFunc('RIGHT')
left = _makeFunc('LEFT')
back = _makeFunc('BACK')

def _makeTLFunc(sensorName):
    def f():
        return _tl_sensors[sensorName].read()[1] / 1000
    return f

tl_front = _makeTLFunc('FRONT')
tl_front_right = _makeTLFunc('FRONT_RIGHT')
tl_front_left = _makeTLFunc('FRONT_LEFT')
tl_right = _makeTLFunc('RIGHT')
tl_left = _makeTLFunc('LEFT')
tl_back = _makeTLFunc('BACK')

_tl_sensor_arr = [_tl_sensors['FRONT'], _tl_sensors['FRONT_RIGHT'], _tl_sensors['RIGHT'], _tl_sensors['BACK'], _tl_sensors['LEFT'], _tl_sensors['FRONT_LEFT']]

def tl_all():
    return list(map(lambda x: x.read()[1] / 1000, _tl_sensor_arr))

def all():
    _sensor_arr = [_sensors['FRONT'], _sensors['FRONT_RIGHT'], _sensors['RIGHT'], _sensors['BACK'], _sensors['LEFT'], _sensors['FRONT_LEFT']]
    return list(map(lambda x: x.distance, _sensor_arr))

def steph():
    _sensor_arr = [_sensors['FRONT'], _sensors['FRONT_RIGHT'], _sensors['RIGHT'], _sensors['BACK'], _sensors['LEFT'], _sensors['FRONT_LEFT']]
    l = list(map(lambda x: int(x * 100 + 15), all()))
    l.insert(3, 0)
    l.insert(5, 0)
    return l

_staged = None

# disable everything but keep track of what was enabled
def stage():
    global _staged
    _staged = {k: v is not None for k, v in _sensors.items()}
    disableAll()

# reenable what was previously enabled with stage
def unstage():
    if _staged is None:
        raise RuntimeError('nothing to unstage')
    for k, v in _staged.items():
        if v:
            _enable(k)

enableAll() #REMOVE PROBABLY IDK
