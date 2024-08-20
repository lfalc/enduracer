import streamlit as st
import pandas as pd
import external as ex
import globals
import time
import datetime
from streamlit_autorefresh import st_autorefresh

globals.init_globals()

hide_table_row_index = """
    <style>
    thead tr th:first-child {display:none}
    tbody th {display:none}
    </style>
"""


if 'start_of_race' not in st.session_state:
    st.session_state.start_of_race = ex.load_start_time()


# Automatische Aktualisierung alle 5 Sekunden (5000 Millisekunden)
st_autorefresh(interval=5000, key="dataframerefresh")

st.title("Schwetzendorf 2024")

# Button zum Starten des Rennens
if st.button("Start Race", help="Click to set the starting time of the race"):
    if st.session_state.start_of_race == 0:
        st.session_state.start_of_race = ex.get_current_time_from_server()
        ex.save_start_time(st.session_state.start_of_race)


normal_time = datetime.datetime.fromtimestamp(st.session_state.start_of_race)

# Button zum Zurücksetzen der Startzeit
if st.button("Reset Start Time", help="Click to reset the start time"):
    if 'start_of_race' in st.session_state:
        st.session_state.start_of_race = 0
        
# Überprüfen, ob die Startzeit gesetzt wurde
if 'start_of_race' in st.session_state:
    st.write(f"Start time recorded: {normal_time.strftime('%H:%M:%S %d-%m-%Y')}")
else:
    st.write("Race has not started yet.")

csv_file = "server_data.csv"

# Tabelle erstellen und anzeigen
table = ex.build_table(csv_file)

# DataFrame erstellen
df = pd.DataFrame(table[1:], columns=table[0])

# Formatieren der numerischen Spalten als Strings
df["Ranking"] = df["Ranking"].astype(str)
df["Laps"] = df["Laps"].astype(str)

st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.table(pd.DataFrame(table[1:], columns=table[0]))

