from gpiozero import DistanceSensor

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

def _makeSensor(trig, echo):
    return DistanceSensor(trigger=trig, echo=echo, max_distance=3, queue_len=3)

def enableAll():
    for k, v in _sensor_defs.items():
        _sensors[k] = _makeSensor(*v)

def disableAll():
    for k, v in _sensor_defs.items():
        _sensors[k] = None

def _makeEnable(sensorName):
    def f():
        _sensors[sensorName] = _makeSensor(*_sensor_defs[sensorName])
    return f

en_front = _makeEnable('FRONT')
en_front_right = _makeEnable('FRONT_RIGHT')
en_front_left = _makeEnable('FRONT_LEFT')
en_right = _makeEnable('RIGHT')
en_left = _makeEnable('LEFT')
en_back = _makeEnable('BACK')

def _makeDisable(sensorName):
    def f():
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

_sensor_arr = [_sensors['FRONT'], _sensors['FRONT_RIGHT'], _sensors['RIGHT'], _sensors['BACK'], _sensors['LEFT'], _sensors['FRONT_LEFT']]

def all():
    _sensor_arr = [_sensors['FRONT'], _sensors['FRONT_RIGHT'], _sensors['RIGHT'], _sensors['BACK'], _sensors['LEFT'], _sensors['FRONT_LEFT']]
    return list(map(lambda x: x.distance, _sensor_arr))

def steph():
    _sensor_arr = [_sensors['FRONT'], _sensors['FRONT_RIGHT'], _sensors['RIGHT'], _sensors['BACK'], _sensors['LEFT'], _sensors['FRONT_LEFT']]
    l = list(map(lambda x: int(x * 100 + 15), all()))
    l.insert(3, 0)
    l.insert(5, 0)
    return l


enableAll() #REMOVE PROBABLY IDK
