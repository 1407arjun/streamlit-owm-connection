# Streamlit OpenWeatherMapConnection

Retrieve current weather and weather forecast for any location by connecting to the OpenWeatherMap API from your Streamlit app. Powered by `st.experimental_connection()` and [requests](https://pypi.org/project/requests/). Works with Streamlit >= 1.22 and Python >= 3.8.

Read more about Streamlit Connections in the [official docs](https://docs.streamlit.io/library/api-reference/connections).

## Quickstart
See the demo directory for a full example of fetching the current weather in different ways by using the city name, coordinates, city ID and zipcode which are supported by the OpenWeatherMap API.
```
pip install streamlit
pip install git+https://github.com/1407arjun/streamlit-owm-connection
```

Initialize the connection by either storing it by the name `appid` in the `secrets.toml` file (recommended) or by directly passing it as an argument to the connection. The AppID passed as an argument takes preference over the one stored in the secrets file.
``` py
import streamlit as st
from st_owm_connection import OpenWeatherMapConnection

# OpenWeatherMap API connection (AppID/API Key loaded from secrets.toml)
conn = st.experimental_connection('owm', type=OpenWeatherMapConnection)

# OR
# OpenWeatherMap API connection (AppID/API Key passed as argument)
conn = st.experimental_connection('owm', type=OpenWeatherMapConnection, appid="<your-api-key>")
```
``` toml
# .streamlit/secrets.toml

[connections.owm]
appid = "<your-api-key>"
```

## Main methods

### current()
Returns the current weather at the given location. Refer to the OpenWeatherMap API docs for 

It takes in any one of the following named arguments at a time:
- `q`: The name of the city or city, state code, country code.
- `lat` and `lon`: The latitude and longitude of the location as floating point numbers.
- `id`: The city ID.
- `zip`: The zipcode, country code of the location.

Apart from the above arguments, it also takes in the following optional arguments:
- `units`: Units of measurement (standard/metric/imperial). Defaults to standard.
- `lang`: Output language. Defaults to English (en).
- `ttl`: Time after which the cached response is invalidated. Refer to the [official docs](https://docs.streamlit.io/library/api-reference/performance/st.cache_data).
