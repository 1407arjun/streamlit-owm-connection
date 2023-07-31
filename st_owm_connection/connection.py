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
    def weather(self, query: str, type: Optional[str] = None, ttl: Optional[Union[float, int, timedelta]] = None):
        @cache_data(ttl=ttl, show_spinner=f"Loading current weather for {query}...")
        def current(query: str):
            r = self.session.get(f"{BASE_URL}/weather?q={query}&appid={self.get_appid()}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner=f"Loading weather forcast for {query}...")
        def forcast(query: str):
            r = self.session.get(f"{BASE_URL}/forecast?q={query}&appid={self.get_appid()}")
            return r.json()
        
        if type == "forcast":
            return forcast(query)
        else:
            return current(query)

    def weather(self, lat: float, lon: float, type: Optional[str] = None, ttl: Optional[Union[float, int, timedelta]] = None) -> Any:
        @cache_data(ttl=ttl, show_spinner="Loading current weather...")
        def current(lat: float, lon: float):
            r = self.session.get(f"{BASE_URL}/weather?lat={lat}&lon={lon}&appid={self.get_appid()}")
            return r.json()
        
        @cache_data(ttl=ttl, show_spinner="Loading weather forcast...")
        def forcast(lat: float, lon: float):
            r = self.session.get(f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={self.get_appid()}")
            return r.json()
        
        if type == "forcast":
            return forcast(lat, lon)
        else:
            return current(lat, lon)