from src.config.api_configs import SESSIONS_API
from urllib.request import urlopen
import json
from typing import List, Dict, Optional
from urllib.parse import urlencode
from enum import Enum
from src.models.session import Session
from src.config.session_config import SessionName, SessionType, CircuteShortName


class Sessions:

    def __init__(self, session_key:str = None, date_start:str = None, date_end:str = None, circuit_short_name:CircuteShortName = None, session_type:SessionType = None, session_name:SessionName = None ):
        self.session_key = session_key
        self.date_start = date_start
        self.date_end = date_end
        self.circuit_short_name = circuit_short_name
        self.session_type = session_type
        self.session_name = session_name

    def __forumulate_filter(self)->Dict:
        """
        Construct Fileter.
        :rtype: Dict
        """

        filter = {}

        if self.session_key:
            filter['session_key'] = self.session_key
        
        if self.date_start:
            filter['date_start>'] = self.date_start

        if self.date_end:
            filter['date_end<'] = self.date_end
        
        if self.circuit_short_name:
            filter['circuit_short_name'] = self.circuit_short_name.value

        if self.session_type:
            filter['session_type'] = self.session_type.value

        if self.session_name:
            filter['session_name'] = self.session_name.value

        
        return filter
        

    def __get_sessions_data(self)->Optional[List[Dict]]:
        """
        get session data from session api.

        :return: Sessions Data 
        """
        query_string = urlencode(self.__forumulate_filter())
        print(query_string)
        if query_string:
            url = f"{SESSIONS_API}?{query_string}"
        else:
            url = SESSIONS_API
        response = response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
        

        return data
    
    def data(self):

        sessions = self.__get_sessions_data()

        records = []
        for session in sessions:
            try:
                records.append(Session(**session))
            except Exception as err:
                print(err)
                continue
    
        return records

        




if __name__ == "__main__":
    date_start="2025-01-01"
    date_end="2025-12-31"
    # circuit_short_name=CircuteShortName.AUSTIN, session_type=SessionType.RACE, session_name=SessionName.RACE
    sessions = Sessions(date_start=date_start, date_end=date_end)
    print(sessions.fetch_data())