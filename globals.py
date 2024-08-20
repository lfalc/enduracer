class Driver:
    def __init__(self, name, driver_id):
        self.name = name
        self.driver_id = driver_id
        self.ranking = 0
        self.lap_clocktimes = [0]
        self.lap_times = [0]
        self.average_lap_time = 0

    def format_time(self, seconds):
        """Format seconds to minutes and seconds."""
        minutes = int(seconds // 60)
        seconds = round(seconds % 60, 2)
        return f"{minutes}:{seconds:0.2f}"

def calculate_lap_times(driver):
    """Calculate lap times and average lap time."""
    lap_times = []
    for n in range(len(driver.lap_clocktimes) - 1):
        lap_time = driver.lap_clocktimes[n + 1] - driver.lap_clocktimes[n]
        lap_times.append(lap_time)
    driver.lap_times = lap_times
    driver.average_lap_time = sum(driver.lap_times) / len(driver.lap_times) if driver.lap_times else 0

def init_globals():
    global drivers
    drivers = []

