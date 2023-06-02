import streamlit as st
import pandas as pd
import external as ex
# from streamlit_autorefresh import st_autorefresh
import globals
import datetime
import calendar
import time


globals.init_globals()
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

st.title("Kartoffelacker Cup 2023")

# count = sst_autorefresh(interval=3000)

button: bool = st.button(
    "Start Race",
    help="Click to set the starting time of the race",
    on_click=ex.get_time,
)

# start = time.localtime(ex.start_of_race)
# float_time = time.mktime(start)
# start_time = datetime.datetime.fromtimestamp(float_time)

# time_in = st.time_input("Set starting time of the race")

files: list = ex.get_files()
option = st.selectbox("Select a database", files)

table = ex.build_table(option)
st.markdown(hide_table_row_index, unsafe_allow_html=True)
st.table(pd.DataFrame(table[1:], columns=table[0]))
# print(globals.drivers[0].lap_times)
