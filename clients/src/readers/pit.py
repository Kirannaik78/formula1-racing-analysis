from urllib.request import urlopen
from urllib.parse import urlencode
from src.config.api_configs import PIT_API
import json
from src.models.pit import Pit



class Pit:

    def __init__(self, driver_number: int, session_key: int):
        self.driver_number = driver_number
        self.session_key = session_key
        

    def __get_filters(self):

        filters = {}

        if self.driver_number:
            filters['driver_number'] = self.driver_number

        if self.session_key:
            filters['session_key'] = self.session_key

        return urlencode(filters)
    
    def __fetch_data(self):

        url = f"{PIT_API}?{self.__get_filters()}"

        response = urlopen(url)

        data = json.loads(response.read().decode('utf-8'))
        print(data)
        return data
    
    def get_models(self):
        
        pits= self.__fetch_data()

        records = []
        for pit in pits:
            records.append(Pit(**pit))

        return records
    


if __name__ == "__main__":

    pit = Pit(driver_number=81, session_key=9158)

    print(pit.get_models())

