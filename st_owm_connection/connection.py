import requests
from requests.sessions import Session
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

from typing import Any, Union, Optional, overload
from datetime import timedelta

BASE_URL = "https://api.openweathermap.org/data/2.5"

class OpenWeatherMapConnection(ExperimentalBaseConnection[Session]):
    def _connect(self, **kwargs) -> Session:
        self.appid = None
        if 'appid' in kwargs:
            self.appid = kwargs.pop('appid')
        
        if self.appid is None:
            secrets = self._secrets.to_dict()

            if secrets.get("appid") == None:
                raise ValueError("AppID/API Key not provided in secrets")
            else:
                self.appid = secrets.pop("appid", None)
        
        self.session = requests.Session()
        return self.session
    
    def session(self) -> Session:
        return self.session
    
    @overload
    def current(self, name: str, ttl: Optional[Union[float, int, timedelta]] = None):
        pass

    def current(self, lat: float, lon: float, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
        @cache_data(ttl=ttl, show_spinner="Loading city weather...")
        def weather_by_city(lat: float, lon: float):
            r = self.session.get(f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={self.appid}")
            return r.json()
        return weather_by_city(lat, lon)