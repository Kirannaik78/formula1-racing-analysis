from src.config.api_configs import RACE_CONTROL_API
from urllib.request import urlopen
import json
from typing import List, Dict, Optional
from urllib.parse import urlencode
from enum import Enum
from src.models.session import Session


class RaceControl:
    def __init__(self, session_key:int):
        self.session_key=session_key

    def __filter_string(self):

        filters = {
            "session_key": self.session_key
        }
        
        return urlencode(filters)
    
    def __fetch_data(self):

        url = f"{RACE_CONTROL_API}?{self.__filter_string()}"

        response = urlopen(url)

        data = json.loads(response.read().decode('utf-8'))

        return data
    
    def get_models(self):

        data = self.__fetch_data()

        for ctn in data:
            print(ctn['flag'])
    

if __name__ == "__main__":
    ctn = RaceControl(session_key=9102)
    
    ctn.get_models()