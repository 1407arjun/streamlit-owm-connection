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
display = st.empty()


def set_weather_ui(weather, conn):
    global display
    with display:
        if 'cod' in weather:
            st.error(weather["message"], icon="🚨")
        else:
            icon, desc, name = st.columns(3)
            with icon:
                st.markdown(
                    f"![]({conn.get_icon_url(weather['weather'][0]['icon'])})")
            with desc:
                st.header(weather["weather"][0]["main"])
                st.subheader(weather["weather"][0]["description"])
            with name:
                st.header(weather["name"])


select_unit, select_lang = st.columns(2)
with select_unit:
    units_list = ["standard", "metric", "imperial"]
    st.selectbox("Select a unit for all data", units_list, index=units_list.index(conn.units), key='units',
                 help=None, on_change=lambda: conn.set_units(st.session_state.units), label_visibility="visible")
with select_lang:
    lang_list = ["en", "fr", "de", "hi", "es", "it"]
    st.selectbox("Select a language for all data", lang_list, index=lang_list.index(conn.lang), key='lang',
                 help=None, on_change=lambda: conn.set_lang(st.session_state.lang), label_visibility="visible")

col1, col2 = st.columns(2)

with col1:
    with st.form("weather_by_city"):
        st.markdown("**Search by city**")
        q = st.text_input("Enter the city", value="", key='q', type="default",
                          help=None, placeholder="City name, State code, Country code", label_visibility="visible")

        submitted = st.form_submit_button("Get weather for city")
        if submitted:
            set_weather_ui(conn.current(q=q), conn)

    with st.form("weather_by_city_id"):
        st.markdown("**Search by city ID**")
        id = st.number_input("Enter the city ID", key='id',
                             min_value=0, label_visibility="visible")

        submitted = st.form_submit_button("Get weather for city ID")
        if submitted:
            set_weather_ui(conn.current(id=id), conn)

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
            set_weather_ui(conn.current(lat=lat, lon=lon), conn)

    with st.form("weather_by_zipcode"):
        st.markdown("**Search by zipcode**")
        zip = st.text_input("Enter the zipcode", value="", key='zip', type="default",
                            help=None, placeholder="Zipcode, Country code", label_visibility="visible")

        submitted = st.form_submit_button("Get weather for zipcode")
        if submitted:
            set_weather_ui(conn.current(zip=zip), conn)
