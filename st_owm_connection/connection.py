import requests
from requests.sessions import Session
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.caching import cache_data

class OpenWeatherMapConnection(ExperimentalBaseConnection[Session]):
    def _connect(self) -> Session:
        secrets = self._secrets.to_dict()
        self.appid = secrets.pop("appid", None)
        self._session = requests.Session()
        return self.session
    
    @property
    def session(self) -> Session:
        return self._session