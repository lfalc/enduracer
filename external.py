import streamlit as st
import csv
import time
import globals
import pandas as pd
import os
import json
import requests

SERVER_URL = "http://192.168.178.186:5000/time"  # Verwende die passende URL
START_TIME_FILE = "start_time.json"

def save_start_time(start_time: float):
    """Speichert die Startzeit in einer JSON-Datei."""
    with open(START_TIME_FILE, "w") as f:
        json.dump({"start_time": start_time}, f)

def load_start_time() -> float:
    """Lädt die Startzeit aus der JSON-Datei."""
    if os.path.exists(START_TIME_FILE):
        with open(START_TIME_FILE, "r") as f:
            data = json.load(f)
            return data.get("start_time", 0.0)
    return 0.0

def get_current_time_from_server() -> float:
    """Holt die aktuelle Zeit vom Server."""
    try:
        response = requests.get(SERVER_URL)
        response.raise_for_status()
        return float(response.text.strip())
    except requests.RequestException as e:
        st.error(f"Fehler beim Abrufen der Zeit vom Server: {e}")
        return time.time()

# def get_current_time() -> float:
#     """Gibt die aktuelle Zeit als Unix-Zeitstempel zurück."""
#     return time.time()



def read_from_csv(csv_file: str):
    driver_dict = {}

    # create driver objects and driver dictionary
    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            driver_id = row[0]
            name = row[1]
            timestamp = float(row[2])
            
            if driver_id not in driver_dict:
                driver_dict[driver_id] = len(globals.drivers)
                driver = globals.Driver(name=name, driver_id=driver_id)
                globals.drivers.append(driver)  # add the driver object to the list

    # read lap clocktimes and calculate relative timestamps
    for row in data:
        driver_id = row[0]
        timestamp = float(row[2])
        driver_index = driver_dict.get(driver_id)
        if driver_index is not None:
            lap_clocktime = timestamp - st.session_state.start_of_race
            globals.drivers[driver_index].lap_clocktimes.append(lap_clocktime)

    # calculate average lap time and ranking
    for driver in globals.drivers:
        for n in range(len(driver.lap_clocktimes) - 1):
            lap_time = driver.lap_clocktimes[n + 1] - driver.lap_clocktimes[n]
            driver.lap_times.append(lap_time)
        # remove empty lap time
        if driver.lap_times:
            driver.lap_times.pop(0)
        driver.average_lap_time = sum(driver.lap_times) / len(driver.lap_times) if driver.lap_times else 0
        driver.ranking = len(driver.lap_clocktimes)

def build_table(csv_file: str):
    globals.drivers.clear()
    read_from_csv(csv_file)
    
    # Sort drivers by the number of laps in descending order
    globals.drivers.sort(key=lambda x: (len(x.lap_clocktimes) - 1, -x.average_lap_time),reverse=True)
    
    # Define ranking based on the number of laps
    for ranking in range(len(globals.drivers)):
        globals.drivers[ranking].ranking = ranking + 1
    
    # Build table
    table = [["Ranking", "Nr.", "Name", "Laps", "Ø-Zeit"]]
    for driver in globals.drivers:
        table.append(
            [
                f"{driver.ranking}",
                driver.driver_id,
                driver.name,
                f"{len(driver.lap_clocktimes)-1}",
                driver.format_time(driver.average_lap_time) if driver.lap_times else 0,
            ]
        )
    return table
