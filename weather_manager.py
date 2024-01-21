from kivy.event import EventDispatcher
from main import Call_City#, cities_temperature, cities_weather
from main import Hourly_weather_location
from main import Daily_forecast

class WeatherManager(EventDispatcher):
    def __init__(self,**kwargs):
        super(WeatherManager, self).__init__(**kwargs)
        self.cities_lat = None
        self.cities_lon = None
        self.temperature = None
        self.feels_like = None
        self.pressure = None
        self.humidity = None
        self.weather_description =  None
        self.time_zone = 0
        self.city = "Warsaw"
        self.unit = "Metric"
        self.daily = [0] * 7
        self.daily_desc = [''] * 7
        self.hourly = [0] * 7
        self.hourly_desc = [''] * 7
        self.sunrise = 0
        self.sunset = 0
        self.register_event_type('on_change')
        
        self.update_weather()
        
        
    def on_change(self, *args):
        print("Weather changed")
        
        
    def updateSettings(self, city, unit):
        self.city = city
        self.unit = unit
        self.update_weather()
        self.dispatch('on_change',None)

    def update_weather(self):
        self.cities_lat, self.cities_lon, self.temperature, self.feels_like, self.pressure, self.humidity, self.weather_description, self.city, self.time_zone, self.sunrise, self.sunset = Call_City(self.city,self.unit) 
        self.update_hourly()
        self.update_weekly()

    def update_hourly(self):
        self.hourly[0], self.hourly[1], self.hourly[2], self.hourly[3], self.hourly[4], self.hourly[5], self.hourly[6], self.hourly_desc[0], self.hourly_desc[1], self.hourly_desc[2], self.hourly_desc[3], self.hourly_desc[4], self.hourly_desc[5], self.hourly_desc[6] = Hourly_weather_location(self.cities_lat, self.cities_lon, self.unit)

    def update_weekly(self):
        self.daily[0], self.daily[1], self.daily[2], self.daily[3], self.daily[4], self.daily[5], self.daily[6], self.daily_desc[0], self.daily_desc[1], self.daily_desc[2], self.daily_desc[3], self.daily_desc[4], self.daily_desc[5], self.daily_desc[6] = Daily_forecast(self.cities_lat, self.cities_lon, self.unit)

    def error_callback(self, req, result):
        self.city_name = 'City Not Found'
        self.temperature = '--'
        self.weather_description = 'N/A'

manager = WeatherManager()

