import requests
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

class OpenWeatherMapConnection():
    def _connect():
        return