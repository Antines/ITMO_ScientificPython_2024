import openmeteo_requests
from datetime import datetime

class IncreaseSpeed():
    def __init__(self, current_speed: int, max_speed: int):
        self.current_speed = current_speed
        self.max_speed = max_speed

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_speed >= self.max_speed:
            raise StopIteration
        else:
            self.current_speed += 10
            return self.current_speed

class DecreaseSpeed():
    def __init__(self, current_speed: int, max_speed: int):
        self.current_speed = current_speed
        self.max_speed = max_speed

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_speed <= 0:
            raise StopIteration
        else:
            self.current_speed -= 10
            return self.current_speed

class Car():
    total_cars_on_road = 0

    def __init__(self, max_speed: int, current_speed=0, state="on road"):
        self.max_speed = max_speed
        self.current_speed = current_speed
        self.state = state
        Car.total_cars_on_road += 1

    def accelerate(self, upper_border=None):
        if self.state == "on road":
            if upper_border is not None and upper_border <= self.max_speed:
                for speed in IncreaseSpeed(self.current_speed, self.max_speed):
                    if speed > upper_border:
                        break
                    self.current_speed = speed
                    print(f"Accelerating: Current speed is {self.current_speed} km/h")
            else:
                self.current_speed = min(self.current_speed + 10, self.max_speed)
                print(f"Accelerating: Current speed is {self.current_speed} km/h")

    def brake(self, lower_border=None):
        if self.state == "on road":
            if lower_border is not None and lower_border <= self.max_speed:
                for speed in DecreaseSpeed(self.current_speed):
                    if speed < lower_border:
                        break
                    self.current_speed = speed
                    print(f"Braking: Current speed is {self.current_speed} km/h")
            else:
                self.current_speed = max(self.current_speed - 10, 0)
                print(f"Braking: Current speed is {self.current_speed} km/h")

    def parking(self):
        if Car.total_cars_on_road > 0:
            Car.total_cars_on_road -= 1
            print("Car is parked")
        else:
            print("Car is not on the road")

    @classmethod
    def total_cars(cls):
        return cls.total_cars_on_road

    @staticmethod
    def show_weather():
        openmeteo = openmeteo_requests.Client()
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 59.9386,  # for St.Petersburg
            "longitude": 30.3141,  # for St.Petersburg
            "current": ["temperature_2m", "apparent_temperature", "rain", "wind_speed_10m"],
            "wind_speed_unit": "ms",
            "timezone": "Europe/Moscow"
        }

        response = openmeteo.weather_api(url, params=params)[0]

        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_rain = current.Variables(2).Value()
        current_wind_speed_10m = current.Variables(3).Value()

        current_time = datetime.fromtimestamp(current.Time() + response.UtcOffsetSeconds())
        timezone_abbr = response.TimezoneAbbreviation().decode()

        print(f"Current time: {current_time} {timezone_abbr}")
        print(f"Current temperature: {round(current_temperature_2m, 0)} C")
        print(f"Current apparent_temperature: {round(current_apparent_temperature, 0)} C")
        print(f"Current rain: {current_rain} mm")
        print(f"Current wind_speed: {round(current_wind_speed_10m, 1)} m/s")

car1 = Car(90)
car2 = Car(90)
car3 = Car(90)
car1.accelerate(60)
car1.brake()
car1.parking()
print(Car.total_cars_on_road)
Car.show_weather()