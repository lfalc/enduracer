import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import globals

# Holt die Namen der Fahrer aus den globalen Daten
driver_names = [globals.drivers[i].name for i in range(len(globals.drivers))]
selected_driver = st.selectbox("Select a driver", driver_names)

# Filtert den ausgewählten Fahrer aus den globalen Daten
driver = [d for d in globals.drivers if d.name == selected_driver]

# Überprüfen, ob der Fahrer gefunden wurde und ob Daten vorhanden sind
if driver:
    driver = driver[0]
    lap_times_seconds = driver.lap_times

    if lap_times_seconds:
        # Konvertiere die Rundenzeiten von Sekunden in Minuten
        lap_times_minutes = [time / 60 for time in lap_times_seconds]

        # Erstellen eines DataFrames für die Visualisierung
        df = pd.DataFrame({
            "Lap": np.arange(1, len(lap_times_minutes) + 1),
            "Lap time in minutes": lap_times_minutes,
        })

        # Definieren der y-Skala mit benutzerdefiniertem Bereich
        y_scale = alt.Scale(
            domain=(min(lap_times_minutes)-0.1, max(lap_times_minutes)+0.1)
        )

        # Erstellen des Diagramms
        chart_data = alt.Chart(df).mark_line().encode(
            y=alt.Y("Lap time in minutes", scale=y_scale, title="Lap time (minutes)"),
            x=alt.X("Lap", title="Lap")
        )

        # Anzeigen des Diagramms in Streamlit
        st.altair_chart(chart_data, use_container_width=True)
    else:
        st.write("Keine Rundenzeiten für den ausgewählten Fahrer verfügbar.")
else:
    st.write("Fahrer nicht gefunden.")
