from hcsr04sensor import sensor

class Sensors (object) :

    def __init__ (self) :
        TRIG_ECHO = [[5, 0], [24, 25], [1, 7], [13, 6], [20, 21], [9, 10]]
        triggers = [26, 5, 9, 20, 12, 1, 8]
        echos = [0, 10, 21, 16, 7, 25]
        self.ultras = []
        for a in range(len(TRIG_ECHO)) :
            self.ultras.append(sensor.Measurement(TRIG_ECHO[a][0], TRIG_ECHO[a][1]))

    def readSingleMetric (self, id) :
        return self.ultras[id].distance_metric(self.ultras[id].raw_distance())

    def readAllMetric (self) :
        readings = []
        for sensor in self.ultras :
            try :
                readings.append(sensor.distance_metric(sensor.raw_distance(5, 0.3)))
            except SystemError :
                readings.append(sensor)
        return readings
