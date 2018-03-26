import asyncio

from hcsr04sensor import sensor

async def readSingleMetric (id) :
    reading = await self.ultras[id].distance_metric(self.ultras[id].raw_distance())
    return reading

class Sensors (object) :

    def __init__ (self) :
        TRIG_ECHO = [[13, 6], [26, 19], [20, 21], [12, 16], [5, 0], [9, 10], [1, 7], [8, 25]]
        triggers = [26, 13, 5, 9, 20, 12, 1, 8]
        echos = [19, 6, 0, 10, 21, 16, 7, 25]
        self.ultras = []
        for a in range(len(TRIG_ECHO)) :
            self.ultras.append(sensor.Measurement(TRIG_ECHO[a][0], TRIG_ECHO[a][1]))


    def readAllMetric (self) :
        """
        futures = []
        for x in range(len(self.ultras)) :
            future = readSingleMetric(x)
            futures.append(future)
        """

        futures = [readSingleMetric(x) for x in range(len(self.ultras))]


        #readings = [readSingleMetric(x) for x in range(len(self.ultras))]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(futures))

        return futures


"""
    def readSingleMetric (self, id) :
        return self.ultras[id].distance_metric(self.ultras[id].raw_distance())

    def readAllMetric (self) :
        readings = []
        for sensor in self.ultras :
            try :
                readings.append(sensor.distance_metric(sensor.raw_distance()))
            except SystemError :
                readings.append(sensor)
        return readings
"""
