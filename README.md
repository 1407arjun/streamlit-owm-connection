# Streamlit OpenWeatherMapConnection

Retrieve current weather and weather forecast for any location by connecting to the OpenWeatherMap API from your Streamlit app. Powered by `st.experimental_connection()` and [requests](https://pypi.org/project/requests/). Works with Streamlit >= 1.22 and Python >= 3.8.

Read more about Streamlit Connections in the [official docs](https://docs.streamlit.io/library/api-reference/connections).

## Installation
See the demo directory for a full example of fetching the current weather in different ways by using the city name, coordinates, city ID and zipcode which are supported by the OpenWeatherMap API.
```
pip install streamlit
pip install git+https://github.com/1407arjun/streamlit-owm-connection
```

## Initialization methods
Initialize the connection by either storing it by the name `appid` in the `secrets.toml` file (recommended) or by directly passing it as an argument to the connection. The AppID passed as an argument takes preference over the one stored in the secrets file. Throws a `ValueError` if no AppID is found.
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

During the initialization of the connection, you can also specify global preferences for units and output language, which would be applied to each request made by the connection, unless overridden in the [main methods](#main-methods) or changed by using the [setter methods](#setter-methods). The preferences that can be set are as follows:
- `units`: Units of measurement (standard/metric/imperial). Defaults to standard.
- `lang`: Output language. Defaults to English (en). View the supported languages and their codes [here](https://openweathermap.org/current#multi).

``` py
import streamlit as st
from st_owm_connection import OpenWeatherMapConnection

conn = st.experimental_connection('owm', type=OpenWeatherMapConnection, units="metric", lang="fr")
```

## Main methods

### current()
Returns the current weather at the given location. Refer to the [OpenWeatherMap API docs](https://openweathermap.org/current) for additional information related to response formats and other endpoint-related taxonomy.

> Requires a free OpenWeatherMap API Key.

It takes in any one of the following named arguments at a time:
- `q`: The name of the city or city, state code, country code.
- `lat` and `lon`: The latitude and longitude of the location as floating point numbers.
- `id`: The city ID, an integer value. Refer to the OpenWeatherMap API docs for a list of valid city IDs.
- `zip`: The zipcode, country code of the location.

> If none of the above arguments is provided, then the function returns `None`.

Apart from the above arguments, it also takes in the following optional arguments, which override the global preferences provided during the initialization for the current request:
- `units`: Units of measurement (standard/metric/imperial). Defaults to standard.
- `lang`: Output language. Defaults to English (en). View the supported languages and their codes [here](https://openweathermap.org/current#multi).
- `ttl`: Time after which the cached response is invalidated. Refer to the [official docs](https://docs.streamlit.io/library/api-reference/performance/st.cache_data).

Some example function calls:
``` py
import streamlit as st
from st_owm_connection import OpenWeatherMapConnection

conn = st.experimental_connection('owm', type=OpenWeatherMapConnection)

# Get weather by city name
print(conn.current(q="San Francisco"))

# Get weather by coordinates (latitude and longitude)
print(conn.current(lat=43.39, lon=10.54))

# Get weather by city ID
print(conn.current(id=833))

# Get weather by zipcode
print(conn.current(zip="94105,US"))
```

### forecast()
Returns the 3-hour/daily/hourly/30-day weather forecast for the given location. Refer to the corresponding OpenWeatherMap API docs pf [3-hour](https://openweathermap.org/forecast5), [daily](https://openweathermap.org/forecast16), [hourly](https://openweathermap.org/api/hourly-forecast) and [30-day](https://openweathermap.org/api/forecast30) forecasts for additional information related to response formats and other endpoint-related taxonomy.

> 3-hour forecast requires a free OpenWeatherMap API Key.
> Daily forecast requires at least a Startup plan OpenWeatherMap API Key.
> Hourly and 30-day forecast requires at least a Developer plan OpenWeatherMap API Key.

The `type` positional argument is mandatory and should be one of the following (defaults to 3-hour forecast):
- `3hr`: Call 5 day / 3 hour forecast data.
- `daily`: Call 16 day / daily forecast data.
- `hourly`: Call hourly forecast data.
- `climate`: Call weather forecast for 30 days.

Similar to the `current` function, It takes in any one of the following named arguments at a time:
- `q`: The name of the city or city, state code, country code.
- `lat` and `lon`: The latitude and longitude of the location as floating point numbers.
- `id`: The city ID, an integer value. Refer to the OpenWeatherMap API docs for a list of valid city IDs.
- `zip`: The zipcode, country code of the location.

> If none of the above arguments is provided, then the function returns `None`.

Apart from the above arguments, it also takes in the following optional arguments, which override the global preferences provided during the initialization for the current request:
- `cnt`: A number of timestamps, which will be returned in the API response.
- `units`: Units of measurement (standard/metric/imperial). Defaults to standard.
- `lang`: Output language. Defaults to English (en). View the supported languages and their codes [here](https://openweathermap.org/current#multi).
- `ttl`: Time after which the cached response is invalidated. Refer to the [official docs](https://docs.streamlit.io/library/api-reference/performance/st.cache_data).

Some example function calls:
``` py
import streamlit as st
from st_owm_connection import OpenWeatherMapConnection

conn = st.experimental_connection('owm', type=OpenWeatherMapConnection)

# Get 3-hour weather forecast by city name
print(conn.forecast("3hr", q="San Francisco"))

# Get daily weather forecast by coordinates (latitude and longitude)
print(conn.forecast("daily", lat=43.39, lon=10.54))

# Get hourly weather forecast by city ID
print(conn.forecast("hourly", id=833))

# Get 30-day weather forecast by zipcode
print(conn.forecast("climate", zip="94105,US"))
```

## Setter methods

### set_units(units: Literal["standard", "metric", "imperial"])
Updates the global units preference to the value passed to the function. Must be one from standard/metric/imperial.

