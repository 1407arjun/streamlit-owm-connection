import streamlit as st
from connection import OpenWeatherMapConnection

st.set_page_config(
    page_title='OpenWeatherMap API Explorer',
    page_icon='🌤️'
)

latitude = st.number_input("Enter the latitude", key='lat', min_value=-90.00, max_value=90.00, value=0.00)
longitude = st.number_input("Enter the longitude", key='lon', min_value=-180.00, max_value=179.99, value=0.00)

conn = st.experimental_connection('owm', type=OpenWeatherMapConnection)

st.json(conn.current(latitude, longitude))