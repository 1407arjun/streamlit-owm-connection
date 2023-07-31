import streamlit as st
from st_owm_connection import OpenWeatherMapConnection

st.set_page_config(
    page_title='OpenWeatherMap API Explorer',
    page_icon='🌤️'
)

st.title("🌤️ OpenWeatherMap API Explorer")

# OpenWeatherMap API connection
conn = st.experimental_connection('owm', type=OpenWeatherMapConnection)

with st.form("weather"):
    st.subheader('Get the current weather')
    st.markdown("**Search by city**")
    query = st.text_input("Enter the city", value="", key='q', type="default", help=None, placeholder="City, Country", label_visibility="visible")

    st.divider()
    
    st.markdown("**Search by latitude and longitude**")
    latitude = st.number_input("Enter the latitude", key='lat', min_value=-90.00, max_value=90.00, value=0.00, label_visibility="visible")
    longitude = st.number_input("Enter the longitude", key='lon', min_value=-180.00, max_value=179.99, value=0.00, label_visibility="visible")

    submitted = st.form_submit_button("Submit")


# Get the connection session using conn.session attribute

st.json(conn.weather(latitude, longitude))