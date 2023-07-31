import streamlit as st
from st_owm_connection import OpenWeatherMapConnection

st.set_page_config(
    page_title='OpenWeatherMap API Explorer',
    page_icon='🌤️',
    layout="wide"
)

st.title("🌤️ OpenWeatherMap API Explorer")

# OpenWeatherMap API connection
conn = st.experimental_connection('owm', type=OpenWeatherMapConnection)

# Get the connection session using conn.session attribute
# Get the connection units using conn.units attribute (default to standard)
# Get the connection language using conn.lang attribute (default to en)


col1, col2 = st.columns(2)

with col1:
    st.subheader('Get the current weather')
    with st.form("weather_by_city"):
        st.markdown("**Search by city**")
        query = st.text_input("Enter the city", value="", key='q', type="default",
                              help=None, placeholder="City, Country", label_visibility="visible")

        submitted = st.form_submit_button("Get weather for city")
        if submitted:
            with col2:
                st.json(conn.current(query))

    with st.form("weather_by_latlon"):
        st.markdown("**Search by coordinates**")
        lat, lon = st.columns(2)
        with lat:
            latitude = st.number_input("Enter the latitude", key='lat', min_value=-
                                       90.00, max_value=90.00, value=0.00, label_visibility="visible")
        with lon:
            longitude = st.number_input("Enter the longitude", key='lon', min_value=-
                                        180.00, max_value=179.99, value=0.00, label_visibility="visible")

        submitted = st.form_submit_button("Get weather for coordinates")
        if submitted:
            with col2:
                st.json(conn.current(latitude, longitude))
