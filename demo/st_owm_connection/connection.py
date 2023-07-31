import requests
from requests.sessions import Session
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

from typing import Any, Union, Optional, overload
from datetime import timedelta

BASE_URL = "https://api.openweathermap.org/data/2.5"

class OpenWeatherMapConnection(ExperimentalBaseConnection[Session]):
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
        
        self.session = requests.Session()
        return self.session
    
    def reset(self):
        self.session.close()
        self.session = requests.Session()
    
    def get_appid(self) -> str:
        return self.__appid
    
    @overload
    def current(self, query: str, ttl: Optional[Union[float, int, timedelta]] = None):
        pass

    @overload
    def current(self, lat: float, lon: float, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
       pass 
        
    def current(self, q: str | float, lon: float | None = None, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {q}...")
        def query(q: str):
            r = self.session.get(f"{BASE_URL}/weather?q={q}&appid={self.get_appid()}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner="Loading current weather...")
        def latlon(lat: float, lon: float):
            r = self.session.get(f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={self.get_appid()}")
            return r.json()
        
        if isinstance(q, str):
            return query(q)
        else:
            return latlon(q, lon)

    @overload
    def forecast(self, query: str, ttl: Optional[Union[float, int, timedelta]] = None):
        pass

    @overload
    def forecast(self, lat: float, lon: float, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
       pass 
        
    def forecast(self, q: str | float, lon: float | None = None, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
        @cache_data(ttl=ttl, show_spinner=f"Loading weather forecast for {q}...")
        def query(q: str):
            r = self.session.get(f"{BASE_URL}/forecast?q={q}&appid={self.get_appid()}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner="Loading weather forecast...")
        def latlon(lat: float, lon: float):
            r = self.session.get(f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={self.get_appid()}")
            return r.json()
        
        if isinstance(q, str):
            return query(q)
        else:
            return latlon(q, lon)