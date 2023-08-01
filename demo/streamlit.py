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

st.subheader('Get the current weather')
units_list = ["standard", "metric", "imperial"]
st.selectbox("Select a unit for all data", units_list, index=units_list.index(conn.units), key='units',
             help=None, on_change=lambda: conn.set_units(st.session_state.units), label_visibility="visible")

col1, col2 = st.columns(2)

with col1:
    with st.form("weather_by_city"):
        st.markdown("**Search by city**")
        q = st.text_input("Enter the city", value="", key='q', type="default",
                          help=None, placeholder="City name, State code, Country code", label_visibility="visible")

        submitted = st.form_submit_button("Get weather for city")
        if submitted:
            st.json(conn.current(q=q))

    with st.form("weather_by_city_id"):
        st.markdown("**Search by city ID**")
        id = st.number_input("Enter the city ID", key='id',
                             min_value=0, label_visibility="visible")

        submitted = st.form_submit_button("Get weather for city ID")
        if submitted:
            st.json(conn.current(id=id))

with col2:
    with st.form("weather_by_latlon"):
        st.markdown("**Search by coordinates**")
        latitude, longitude = st.columns(2)
        with latitude:
            lat = st.number_input("Enter the latitude", key='lat', min_value=-
                                  90.00, max_value=90.00, value=0.00, label_visibility="visible")
        with longitude:
            lon = st.number_input("Enter the longitude", key='lon', min_value=-
                                  180.00, max_value=179.99, value=0.00, label_visibility="visible")

        submitted = st.form_submit_button("Get weather for coordinates")
        if submitted:
            st.json(conn.current(lat=lat, lon=lon))

    with st.form("weather_by_zipcode"):
        st.markdown("**Search by zipcode**")
        zip = st.text_input("Enter the zipcode", value="", key='zip', type="default",
                            help=None, placeholder="Zipcode, Country code", label_visibility="visible")

        submitted = st.form_submit_button("Get weather for zipcode")
        if submitted:
            st.json(conn.current(zip=zip))
