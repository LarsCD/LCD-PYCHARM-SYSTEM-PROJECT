import time
import datetime
import psutil

class Application():
    def __init__(self):

        # setup
        self.timestamp = datetime.datetime.now()
        self.update_speed = 1   # hz

        self.get_data = self.get_data()


    def get_data(self):
        battery = psutil.sensors_battery()
        print(battery)
