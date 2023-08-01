import requests
from requests.sessions import Session
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

from typing import Any, Union, Optional, Literal
from datetime import timedelta

BASE_URL = "https://api.openweathermap.org/data/2.5"
PRO_URL = "https://pro.openweathermap.org/data/2.5"


class OpenWeatherMapConnection(ExperimentalBaseConnection[Session]):
    __appid: Union[str, None]
    units: Literal["standard", "metric", "imperial"] = "standard"
    lang: str = "en"

    def _connect(self, **kwargs) -> Session:
        self.__appid = None
        if 'appid' in kwargs:
            self.__appid = kwargs.pop('appid')
        else:
            if self.__appid is None:
                secrets = self._secrets.to_dict()

                if secrets.get("appid") == None:
                    raise ValueError("AppID/API Key not provided in secrets")
                else:
                    self.__appid = secrets.pop("appid", None)

        if 'units' in kwargs:
            self.units = kwargs.pop('units')

        if 'lang' in kwargs:
            self.lang = kwargs.pop('lang')

        self.session = requests.Session()
        return self.session

    # Private method to get the AppID within the conncection class
    def __get_appid(self) -> str:
        return self.__appid

    # Reset and return a new connection with the same AppID
    def reset(self):
        self.session.close()
        self.session = requests.Session()

    # Setters for units and language preferences
    def set_units(self, units: Literal["standard", "metric", "imperial"]):
        self.units = units

    def set_lang(self, lang: str):
        self.lang = lang

    # Call current weather data
    def current(self, q: str = None, lat: float = None, lon: float = None, id: int = None, zip: str = None, units: Literal["standard", "metric", "imperial"] = None, lang: str = None, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
        units = units if units else self.units
        lang = lang if lang else self.lang

        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {q}...")
        def query(q: str, units: Literal["standard", "metric", "imperial"], lang: str):
            r = self.session.get(
                f"{BASE_URL}/weather?q={q}&appid={self.__get_appid()}&units={units}&lang={lang}")
            return r.json()

        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {lat}, {lon}...")
        def latlon(lat: float, lon: float, units: Literal["standard", "metric", "imperial"], lang: str):
            r = self.session.get(
                f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={self.__get_appid()}&units={units}&lang={lang}")
            return r.json()

        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {id}...")
        def cityid(id: str, units: Literal["standard", "metric", "imperial"], lang: str):
            r = self.session.get(
                f"{BASE_URL}/weather?id={id}&appid={self.__get_appid()}&units={units}&lang={lang}")
            return r.json()

        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {zip}...")
        def zipcode(zip: str, units: Literal["standard", "metric", "imperial"], lang: str):
            r = self.session.get(
                f"{BASE_URL}/weather?zip={zip}&appid={self.__get_appid()}&units={units}&lang={lang}")
            return r.json()

        if q is not None:
            return query(q, units, lang)
        elif lat is not None and lon is not None:
            return latlon(lat, lon, units, lang)
        elif id is not None:
            return cityid(id, units, lang)
        elif zip is not None:
            return zipcode(zip, units, lang)
        else:
            return None

    # Call 5 day / 3 hour, 16 day / daily, hourly forecast data or climate forecast for 30 days
    def forecast(self, type: Literal["3hr", "daily", "hourly", "climate"] = "3hr", q: str = None, lat: float = None, lon: float = None, id: int = None, zip: str = None, cnt: int = None, units: Literal["standard", "metric", "imperial"] = None, lang: str = None, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
        units = units if units else self.units
        lang = lang if lang else self.lang
        count = "&cnt=" + cnt if cnt else ""

        type = "" if type == "3hr" else type
        ENDPOINT = PRO_URL if type in [
            "daily", "hourly", "climate"] else BASE_URL

        @cache_data(ttl=ttl, show_spinner=f"Loading {type} weather forecast for {q}...")
        def query(q: str, count: str, units: Literal["standard", "metric", "imperial"], lang: str):
            r = self.session.get(
                f"{ENDPOINT}/forecast/{type}?q={q}&appid={self.__get_appid()}&units={units}&lang={lang}{count}")
            return r.json()

        @cache_data(ttl=ttl, show_spinner=f"Loading {type} weather forecast for {lat}, {lon}...")
        def latlon(lat: float, lon: float, count: str, units: Literal["standard", "metric", "imperial"], lang: str):
            r = self.session.get(
                f"{ENDPOINT}/forecast/{type}?lat={lat}&lon={lon}&appid={self.__get_appid()}&units={units}&lang={lang}{count}")
            return r.json()

        @cache_data(ttl=ttl, show_spinner=f"Loading {type} weather forecast for {id}...")
        def cityid(id: str, count: str, units: Literal["standard", "metric", "imperial"], lang: str):
            r = self.session.get(
                f"{ENDPOINT}/forecast/{type}?id={id}&appid={self.__get_appid()}&units={units}&lang={lang}{count}")
            return r.json()

        @cache_data(ttl=ttl, show_spinner=f"Loading {type} weather forecast for {zip}...")
        def zipcode(zip: str, count: str, units: Literal["standard", "metric", "imperial"], lang: str):
            r = self.session.get(
                f"{ENDPOINT}/forecast/{type}?zip={zip}&appid={self.__get_appid()}&units={units}&lang={lang}{count}")
            return r.json()

        if q is not None:
            return query(q, count, units, lang)
        elif lat is not None and lon is not None:
            return latlon(lat, lon, count, units, lang)
        elif id is not None:
            return cityid(id, count, units, lang)
        elif zip is not None:
            return zipcode(zip, count, units, lang)
        else:
            return None

    # Utility function to get the icon URL
    def get_icon_url(self, id: str) -> str:
        return f"https://openweathermap.org/img/wn/{id}@2x.png"
