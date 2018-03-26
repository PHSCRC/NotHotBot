from ultrasonicClass import Sensors
import time

sensors = Sensors()

while True :
    print(sensors.readAllMetric())
    time.sleep(0.1)
