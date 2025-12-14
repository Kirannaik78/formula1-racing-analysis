from urllib.request import urlopen
from urllib.parse import urlencode
from src.config.api_configs import DRIVER_API
import json
from src.models.driver import Driver

class Drivers:

    def __init__(self, session_key: int):
        self.session_key = session_key

    def __get_filter_query(self)->str:
        """
        Filter Query.
        """

        filters = {
            "session_key": self.session_key
        }

        return urlencode(filters)



    
    
    def fetch_drivers(self):
        """
        Fetch Drivers Details for a give session.
        """
        url = f"{DRIVER_API}?{self.__get_filter_query()}"

        response = urlopen(url)
        data = json.loads(response.read().decode('utf-8'))

        return data
    
    def get_driver_models(self):

        drivers = self.fetch_drivers()

        driver_models = []

        for driver in drivers:
            driver_models.append(Driver(**driver))

        return driver_models

if __name__ == "__main__":
    drivers = Drivers(session_key=9975)
    print(drivers.get_driver_models())