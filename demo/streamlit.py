import streamlit as st
from st_owm_connection import OpenWeatherMapConnection

st.set_page_config(
    page_title='OpenWeatherMap API Explorer',
    page_icon='🌤️'
)

st.title("🌤️ OpenWeatherMap API Explorer")
"""
This weather app is a quick prototype of using `st.experimental_connection`
with the OpenWeatherMap API to retrieve the current weather data for a given 
location using its name, coordinates, IDs or zipcodes. It makes use of the **free
version of the OpenWeatherMap API**. View the full app code 
[here](https://github.com/1407arjun/streamlit-owm-connection/tree/main/demo).

Although this example demonstrates the use of the current weather endpoint using the `conn.current` method, 
the connection also provides the `conn.forecast` method to retrieve the 3 hour/daily/hourly/30 day forecasts
for a given location using its name, coordinates, IDs or zipcodes, by passing in the appropriate type of forecast
and free/pro API Keys for the required functionality. View the connection docs 
[here](https://github.com/1407arjun/streamlit-owm-connection/tree/main/README.md).
"""

# OpenWeatherMap API connection (AppID/API Key loaded from secrets)
conn = st.experimental_connection('owm', type=OpenWeatherMapConnection)

# Get the connection session using conn.session attribute
# Get the connection units using conn.units attribute (default to standard)
# Get the connection language using conn.lang attribute (default to en)

display = st.empty()
metrics = st.empty()

with display:
    st.subheader('Get the current weather')


def set_weather_ui(weather, conn):
    global display, metrics
    with display:
        if weather["cod"] != 200:
            with st.container():
                st.subheader('Get the current weather')
                st.info(weather["message"], icon="ℹ️")
        else:
            with st.container():
                st.subheader(
                    f"Current weather for {weather['name']}, {weather['sys'].get('country', '')}")
                icon, desc = st.columns((2, 10))
                with icon:
                    st.markdown(
                        f"![]({conn.get_icon_url(weather['weather'][0]['icon'])})")
                with desc:
                    st.markdown(f"### {weather['weather'][0]['main']}")
                    st.caption(f"{weather['weather'][0]['description']}")

    with metrics:
        if weather["cod"] != 200:
            st.write()
        else:
            temp, pressure, humidity = st.columns(3)
            with temp:
                if conn.units == "imperial":
                    unit = "°F"
                elif conn.units == "metric":
                    unit = "°C"
                else:
                    unit = "K"
                st.metric(label="Temperature",
                          value=f"{weather['main']['temp']} {unit}")
            with pressure:
                st.metric(label="Pressure",
                          value=f"{weather['main']['pressure']} hPa")
            with humidity:
                st.metric(label="Humidity",
                          value=f"{weather['main']['humidity']} %")


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
