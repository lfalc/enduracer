import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import globals


driver_names = [globals.drivers[i].name for i in range(len(globals.drivers))]
selected_driver = st.selectbox("Select a driver", driver_names)

driver = [driver for driver in globals.drivers if driver.name == selected_driver]
# fastest_time, fatest_lap = min(driver[0].lap_times), driver[0].lap_times.index(min(driver[0].lap_times))



df = pd.DataFrame(
    {
        "Lap": np.arange(1, len(driver[0].lap_times) + 1),
        "Lap time in seconds": driver[0].lap_times,
    }
)

# Define y-scale with custom domain and range
y_scale = alt.Scale(
    # Set the domain of the y-scale (minimum and maximum values)
    domain=(
        min(driver[0].lap_times)-1,
        max(driver[0].lap_times)+1,
    ),
)


chart_data = (
    alt.Chart(df)
    .mark_line()
    .encode(
        y=alt.Y("Lap time in seconds", scale=y_scale),
        x="Lap",
    )
)

st.altair_chart(chart_data, use_container_width=True)
