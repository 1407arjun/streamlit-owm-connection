import requests
from requests.sessions import Session
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

from typing import Any, Union, Optional, Literal, overload
from datetime import timedelta

BASE_URL = "https://api.openweathermap.org/data/2.5"
PRO_URL = "https://pro.openweathermap.org/data/2.5"

class OpenWeatherMapConnection(ExperimentalBaseConnection[Session]):
    __appid: str | None
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
    
    def reset(self):
        self.session.close()
        self.session = requests.Session()
    
    def __get_appid(self) -> str:
        return self.__appid
    
    def set_units(self, units: Literal["standard", "metric", "imperial"]):
        self.units = units

    def set_lang(self, lang: str):
        self.lang = lang
    
    # Call current weather data
    def current(self, q: str = None, lat: float = None, lon: float = None, id: int = None, zip: str = None, units: Literal["standard", "metric", "imperial"] = None, lang: str = None, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
        units = units if units else self.units
        lang = lang if lang else self.lang

        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {q}...")
        def query(q: str):
            r = self.session.get(f"{BASE_URL}/weather?q={q}&appid={self.__get_appid()}&units={units}&lang={lang}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {lat}, {lon}...")
        def latlon(lat: float, lon: float):
            r = self.session.get(f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={self.__get_appid()}&units={units}&lang={lang}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {zip}...")
        def cityid(id: str):
            r = self.session.get(f"{BASE_URL}/weather?id={id}&appid={self.__get_appid()}&units={units}&lang={lang}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {zip}...")
        def zipcode(zip: str):
            r = self.session.get(f"{BASE_URL}/weather?zip={zip}&appid={self.__get_appid()}&units={units}&lang={lang}")
            return r.json()

        if q is not None:
            return query(q=q)
        elif lat is not None and lon is not None:
            return latlon(lat=lat, lon=lon)
        elif id is not None:
            return cityid(id=id)
        elif zip is not None:
            return zipcode(zip=zip)
        else:
            return None
        
    def forecast(self, type: Literal["3hr", "daily", "hourly", "climate"] = "3hr", q: str = None, lat: float = None, lon: float = None, id: int = None, zip: str = None, cnt: int = None, units: Literal["standard", "metric", "imperial"] = None, lang: str = None, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
        units = units if units else self.units
        lang = lang if lang else self.lang
        count = "&cnt=" + cnt if cnt else ""

        type = "" if type == "3hr" else type
        ENDPOINT = PRO_URL if type in ["daily", "hourly", "climate"] else BASE_URL

        @cache_data(ttl=ttl, show_spinner=f"Loading {type} weather forecast for {q}...")
        def query(q: str):
            r = self.session.get(f"{ENDPOINT}/forecast/{type}?q={q}&appid={self.__get_appid()}&units={units}&lang={lang}{count}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner=f"Loading {type} weather forecast for {lat}, {lon}...")
        def latlon(lat: float, lon: float):
            r = self.session.get(f"{ENDPOINT}/forecast/{type}?lat={lat}&lon={lon}&appid={self.__get_appid()}&units={units}&lang={lang}{count}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner=f"Loading {type} weather forecast for {zip}...")
        def cityid(id: str):
            r = self.session.get(f"{ENDPOINT}/forecast/{type}?id={id}&appid={self.__get_appid()}&units={units}&lang={lang}{count}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner=f"Loading {type} weather forecast for {zip}...")
        def zipcode(zip: str):
            r = self.session.get(f"{ENDPOINT}/forecast/{type}?zip={zip}&appid={self.__get_appid()}&units={units}&lang={lang}{count}")
            return r.json()

        if q is not None:
            return query(q=q)
        elif lat is not None and lon is not None:
            return latlon(lat=lat, lon=lon)
        elif id is not None:
            return cityid(id=id)
        elif zip is not None:
            return zipcode(zip=zip)
        else:
            return None
        
    def get_icon_url(id: str):
        return f"https://openweathermap.org/img/wn/{id}@2x.png"