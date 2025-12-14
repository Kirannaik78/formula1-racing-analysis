from urllib.request import urlopen
from urllib.parse import urlencode
from src.config.api_configs import CAR_API
import json
from src.models.car import Car

class Cars:

    def __init__(self, driver_number: int, session_key: int):
        self.driver_number = driver_number
        self.session_key = session_key

    
    def __get_filter_string(self)->str:
        """
        Contructs filter string for car.
        """

        if not self.session_key:
            raise ValueError(f"Mission Session Key: {self.session_key}")

        filters = {
            "driver_number": self.driver_number,
            "session_key": self.session_key
        }

        return urlencode(filters)
    

    def __fetch_data(self):
        """
        Fetch Car data.
        """

        query_string = self.__get_filter_string()

        url = f"{CAR_API}?{query_string}"

        response = urlopen(url)

        data = json.loads(response.read().decode('utf-8'))

        return data
    
    def get_car_models(self):

        cars = self.__fetch_data()

        records = []
        for car in cars:
            records.append(Car(**car))
        
        return records
    

if __name__ == "__main__":

    car = Cars(driver_number=55, session_key=9159)
    print(car.get_car_models())

        