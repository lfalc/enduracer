import streamlit as st
import csv
import pandas as pd
import os
import requests
import json
import globals


def read_from_csv(csv_file: str, drivers: list = []):
    driver_dict = {}

    # create driver objects and driver dictionary
    with open(csv_file, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
        for row in data:
            if row[0] not in driver_dict:
                driver_dict.update({row[0]: len(globals.drivers)})
                driver = globals.Driver(name=row[0])
                globals.drivers.append(driver)  # add the driver object to the list

    # read lap clocktimes and calculate relative timestamps
    with open("database_dummy.csv", newline="") as f:
        for row in data:
            lap_clocktime = float(row[1]) - start_of_race
            globals.drivers[driver_dict.get(row[0])].lap_clocktimes.append(
                lap_clocktime
            )

    # calculate average lap time and ranking
    for driver in globals.drivers:
        for n in range(len(driver.lap_clocktimes) - 1):
            lap_time = driver.lap_clocktimes[n + 1] - driver.lap_clocktimes[n]
            driver.lap_times.append(lap_time)
        # remove empty lap time
        driver.lap_times.pop(0)

        driver.average_lap_time = sum(driver.lap_times) / len(driver.lap_times)
        driver.ranking = len(driver.lap_clocktimes)


def build_table(csv_file: str, drivers: list = []):
    globals.drivers.clear()

    read_from_csv(csv_file, globals.drivers)
    # sort by average lap time
    globals.drivers.sort(key=lambda x: x.average_lap_time, reverse=False)
    # define ranking
    for ranking in range(len(globals.drivers)):
        globals.drivers[ranking].ranking = ranking + 1

    # build table
    table = [["Ranking", "Name", "Laps", "Average Lap Time"]]
    for driver in globals.drivers:
        table.append(
            [
                driver.ranking,
                driver.name,
                len(driver.lap_clocktimes),
                driver.average_lap_time,
            ]
        )
    return table


# read .csv files in current directory, store in list
def get_files():
    files = []
    for file in os.listdir():
        if file.endswith(".csv"):
            files.append(file)
    return files


# get time from server (for ESP32)
def get_time():
    start_of_race = float(requests.get("http://localhost:5000/time").text)
    with open("variables.json", "w") as f:
        json.dump({"start_of_race": start_of_race}, f, indent=4)
