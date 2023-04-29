class Driver:
    def __init__(self, name):
        self.name = name
        self.ranking = 0
        self.lap_clocktimes = [0]
        self.lap_times = [0]
        self.average_lap_time = 0

def init_globals():
    global drivers
    drivers = []