import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import globals

# Holt die Namen und Nummern der Fahrer aus den globalen Daten
driver_names_with_numbers = [
    f"{globals.drivers[i].driver_id} - {globals.drivers[i].name}" for i in range(len(globals.drivers))
]
selected_driver = st.selectbox("Select a driver", driver_names_with_numbers)

# Extrahiert die Nummer des ausgewählten Fahrers
selected_driver_number = selected_driver.split(" - ")[0]

# Filtert den ausgewählten Fahrer aus den globalen Daten basierend auf der Nummer
driver = [d for d in globals.drivers if d.driver_id == selected_driver_number]

def format_time(seconds):
    """Format a float time in seconds to mm:ss."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

# Überprüfen, ob der Fahrer gefunden wurde und ob Daten vorhanden sind
if driver:
    driver = driver[0]
    lap_times_seconds = driver.lap_times

    if lap_times_seconds:
        # Konvertiere die Rundenzeiten von Sekunden in Minuten:Sekunden
        lap_times_formatted = [format_time(time) for time in lap_times_seconds]

        # Erstellen eines DataFrames für die Visualisierung
        df = pd.DataFrame({
            "Lap": np.arange(1, len(lap_times_seconds) + 1),
            "Lap time": lap_times_formatted,
            "Lap time (seconds)": lap_times_seconds,  # Rohdaten für die Sortierung
        })

        # Entfernen der Index-Spalte, wenn du sie nicht anzeigen möchtest
        df_display = df.reset_index(drop=True)

        # Erstellen des Diagramms
        chart_data = alt.Chart(df).mark_line().encode(
            x=alt.X("Lap:O", title="Lap", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Lap time (seconds):Q", title="Lap time (seconds)"),
            color=alt.value("blue")
        ).properties(
            title="Lap Times in seconds"
        )

        # Anzeigen des Diagramms in Streamlit
        st.altair_chart(chart_data, use_container_width=True)

        # Tabelle mit formatierten Zeiten anzeigen
        st.write("Lap times (formatted):")
        st.write(df[["Lap", "Lap time", "Lap time (seconds)"]])
    else:
        st.write("Keine Rundenzeiten für den ausgewählten Fahrer verfügbar.")
else:
    st.write("Fahrer nicht gefunden.")
