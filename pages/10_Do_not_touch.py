import streamlit as st
import external as ex
import datetime


st.title("Control Panel")


# Button zum Starten des Rennens
if st.button("Start Race", help="Click to set the starting time of the race"):
    if st.session_state.start_of_race == 0:
        st.session_state.start_of_race = ex.get_current_time_from_server()
        ex.save_start_time(st.session_state.start_of_race)

# Button zum Zurücksetzen der Startzeit
if st.button("Reset Start Time", help="Click to reset the start time"):
    if 'start_of_race' in st.session_state:
        st.session_state.start_of_race = 0
        #ex.save_start_time(0)  # Auch im externen Speicher zurücksetzen


normal_time = datetime.datetime.fromtimestamp(st.session_state.start_of_race)

# Überprüfen, ob die Startzeit gesetzt wurde
if 'start_of_race' in st.session_state:
    st.write(f"Start time recorded: {normal_time.strftime('%H:%M:%S %d-%m-%Y')}")
else:
    st.write("Race has not started yet.")



# # Button zum Navigieren zurück zur Hauptseite
# if st.button("Go to Main Page"):
#     st.write("Navigate to the main page by entering the URL: `/`")
