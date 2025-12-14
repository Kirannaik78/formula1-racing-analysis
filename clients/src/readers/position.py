from urllib.request import urlopen
from urllib.parse import urlencode
import json
from src.config.api_configs import POSITION_API
from src.models.position import Position


class Positions:
    def __init__(self, session_key: int):
        self.session_key = session_key

    def __filter_string(self):

        filters = {
            "session_key": self.session_key
        }

        return urlencode(filters)
    
    def __fetch_data(self):

        url = f"{POSITION_API}?{self.__filter_string()}"

        request = urlopen(url)

        data = json.loads(request.read().decode('utf-8'))
        print(data)
        return data 
    
    def get_models(self):

        positions = self.__fetch_data()

        records = []

        for position in positions:
            try:
                records.append(Position(**position))
            except Exception as err:
                print(err)
                continue

        return records
    

if __name__ == "__main__":
    position = Positions(session_key=9144)

    print(position.get_models())