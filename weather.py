from kivy.config import Config

Config.set('graphics', 'fullscreen', '1')
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from weather_manager import manager
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from DarkBlueBoxLayoutHeader import DarkBlueBoxLayout,GreyBoxLayout
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
import datetime

class WeatherApp(App):
    def build(self):
        #Fonts
        LabelBase.register(name='CustomFontB', fn_regular='static/OpenSans-SemiBold.ttf')
        LabelBase.register(name='CustomFontR', fn_regular='static/OpenSans-Regular.ttf')
        LabelBase.register(name='CustomFontI', fn_regular='static/OpenSans-Italic.ttf')
        
        # left tile
        self.layout = BoxLayout(orientation='horizontal', spacing=5, padding=5)
        settings_layout = self.create_settings_tile()
        self.settings_popupsettings_popup = Popup(title='Settings',
                      content=settings_layout,
                      size_hint=(None, None), size=(400, 400))
        #self.layout.add_widget(settings_layout)

        # central tiles
        ## upper
        middle_tiles_layout = BoxLayout(orientation='vertical', spacing=5)
        middle_tiles_layout.add_widget(self.create_city_and_temperature_tile())
        middle_tiles_layout.add_widget(self.create_hourly_forecast_tile())
        ## middle
        air_conditions_layout = BoxLayout(orientation='horizontal', spacing=5)
        air_conditions_layout.add_widget(self.create_left_air_conditions_tile())
        air_conditions_layout.add_widget(self.create_right_air_conditions_tile())
        ## bottom
        middle_tiles_layout.add_widget(air_conditions_layout)
        self.layout.add_widget(middle_tiles_layout)

        # right tile
        right_tile_layout = self.create_7_day_forecast_tile()
        self.layout.add_widget(right_tile_layout)

        manager.bind(on_change = self.updateTopView)
        manager.bind(on_change = self.updateMiddleView)
        manager.bind(on_change = self.updateBottomView)
        manager.bind(on_change = self.updateRightView)

        return self.layout

    def updateTopView(self,instance,value):
        self.city_label.text = self.get_cityLabel_text()
        self.temp_label.text = self.get_tempLabel_text()
        self.realfeel_label.text = self.get_realfeel_text()
        self.description_label.text = self.get_weatherDescription_text()
        self.image.source = self.get_img_source()

    def updateMiddleView(self, instance, value):
        for i, (label, time_label, image_for_daily) in enumerate(zip(self.hourly_labels, self.hourly_times, self.images_for_daily)):
            if (manager.cities_lat != '0'):
                label.text = self.get_hourly_array(i) + '°'
            else:
                label.text = ''
            time_label.text = f"{(int(self.current_datetime.hour) + int(self.get_time_difference()) + i) % 24}:00"
            image_for_daily.source = self.rawToPictureAddress(manager.hourly_desc[i])



    def updateBottomView(self,instance,value):
        self.humidity.text = self.get_humidity_text()
        self.pressure.text = self.get_pressure_text()
        self.daybreak.text = self.get_sunrise_text()

    def updateRightView(self,instance,value):
        for i, (label, image_for_weekly) in enumerate(zip(self.week_temp, self.week_desc)):
            if (manager.cities_lat != '0'):
                label.text = self.get_weekly_array(i) + '°'
            else:
                label.text = ''
            image_for_weekly.source = self.rawToPictureAddress(manager.daily_desc[i])

    def create_city_and_temperature_tile(self):
        btn = Button(text='',
                     font_size=80,
                     size_hint=(None, None),
                     size=(70, 70),
                     pos_hint={'right': 0.95, 'bottom': 1},
                     on_press=self.settings_popupsettings_popup.open,
                     border=(0, 0, 0, 0),
                     background_normal='images/Settings_icon.png')

        main = DarkBlueBoxLayout(orientation='horizontal', spacing=0)
        tile = DarkBlueBoxLayout(orientation='horizontal', spacing=0)
        mainInfo = DarkBlueBoxLayout(orientation='vertical', spacing=0,size_hint_x=2)

        self.city_label = Label(text=self.get_cityLabel_text(), font_name='CustomFontB', color='black', font_size=50, halign='left', valign='middle')
        self.temp_label = Label(text=self.get_tempLabel_text(), font_name='CustomFontB', color='black', font_size=150, halign='left', valign='middle')
        self.realfeel_label = Label(text=self.get_realfeel_text(), font_name='CustomFontI', color='black', font_size=20, halign='left', valign='middle')

        image_source = self.get_img_source()
        self.image = Image(source=image_source, size_hint=(None, 1), width=200)

        mainInfo.add_widget(self.city_label)
        mainInfo.add_widget(Label())
        mainInfo.add_widget(self.temp_label)
        mainInfo.add_widget(Label())
        mainInfo.add_widget(self.realfeel_label)

        self.description_label = Label(text=self.get_weatherDescription_text(), font_name='CustomFontB', color='black', font_size=30, halign='right', valign='middle')

        tile.add_widget(mainInfo)
        tile.add_widget(self.image)
        tile.add_widget(Label())

        box = BoxLayout(orientation='vertical')
        tile.add_widget(box)
        box.add_widget(btn)
        box.add_widget(self.description_label)


        main.add_widget(tile)

        return main
    
    def get_img_source(self):
        raw = f"{manager.weather_description}"
        return self.rawToPictureAddress(raw)
    
    def rawToPictureAddress(self, data):
        if 'thunderstorm' in data:
            result = "Thunderstorm"
        elif 'drizzle' in data:
            result = "Drizzle"
        elif 'snow' in data:
            result = "Snow"
        elif 'clear' in data:
            result = "Clear"
        elif 'clouds' in data:
            result = "Clouds"
        elif 'rain' in data:
            result = "Rain"
        else:
            result = "Atmosphere"
    
        picture = {
            "Thunderstorm": "weatherImages/Storm.png",
            "Drizzle": "weatherImages/Rain.png",
            "Rain": "weatherImages/Rain_new.png",
            "Snow": "weatherImages/Snowfall.png",
            "Atmosphere": "weatherImages/Foggy.png",
            "Clear": "weatherImages/Sun.png",
            "Clouds": "weatherImages/Cloud.png",
        }
        return picture.get(result, "weatherImages/Sun_cloud")

    def get_cityLabel_text(self):
        return f"{manager.city}"

    def get_tempLabel_text(self):
        unit = 'C' if manager.unit == 'Metric' else 'F'
        return f"{round(manager.temperature)}°{unit}"
    
    def get_realfeel_text(self):
        unit = 'C' if manager.unit == 'Metric' else 'F'
        return "Real Feel: " + f"{round(manager.feels_like)}°"
    
    def get_weatherDescription_text(self):
        raw = f"{manager.weather_description}               "
        return raw.capitalize()

    def get_hourly_array(self, int):
        return f"{round(manager.hourly[int])}"
    
    def get_weekly_array(self, int):
        return f"{round(manager.daily[int])}"

    def create_hourly_forecast_tile(self):
        tile = DarkBlueBoxLayout(orientation='vertical', spacing=5)

        tile.add_widget(Label(text="Today's Forecast", font_size=30, font_name='CustomFontB', color='black', halign='right', valign='middle'))
        tile.add_widget(Label())
        tile.add_widget(Label())

        forecast_container = BoxLayout(orientation='horizontal', spacing=5)
        self.populate_hourly_forecast(forecast_container)
        
        tile.add_widget(forecast_container)
        tile.add_widget(Label())
        return tile

    def create_left_air_conditions_tile(self):
        tile = DarkBlueBoxLayout(orientation='vertical', spacing=5)
        tile.add_widget(Label(text='Daybreak', font_size=25, font_name='CustomFontB', color='black', halign='right', valign='top'))
        hori = DarkBlueBoxLayout(orientation='horizontal', spacing=5)
        hori.add_widget(Label())
        images = Image(source="images/Sunrise_icon.png", size_hint=(None, None), size=(80, 80), pos_hint={'center_x': 0.5})
        hori.add_widget(images)
        hori.add_widget(Label())
        images = Image(source="images/Sunset_icon.png", size_hint=(None, None), size=(80, 80), pos_hint={'center_x': 0.5})
        hori.add_widget(images)
        hori.add_widget(Label())

        tile.add_widget(hori)
        self.daybreak = Label(text=self.get_sunrise_text(), font_size=20, color='black', halign='right', valign='middle')
        tile.add_widget(self.daybreak)

        return tile
    
    def get_sunrise_text(self):
        unix = manager.sunrise
        utc_datetime = datetime.datetime.utcfromtimestamp(unix)
        readable_time = utc_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')
        time_object = datetime.datetime.strptime(readable_time, '%Y-%m-%d %H:%M:%S UTC')
        hour_part = time_object.hour
        minute_part = time_object.minute

        unix1 = manager.sunset
        utc_datetime = datetime.datetime.utcfromtimestamp(unix1)
        readable_time1 = utc_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')
        time_object1 = datetime.datetime.strptime(readable_time1, '%Y-%m-%d %H:%M:%S UTC')
        hour_part1 = time_object1.hour
        minute_part1 = time_object1.minute

        return f"{(int(self.get_time_difference()) + int(hour_part)) % 24:02d}:{int(minute_part):02d}" + (" " * 37) + f"{(int(self.get_time_difference()) + int(hour_part1)) % 24:02d}:{int(minute_part1):02d}"

    
    def get_pressure_text(self):
        return 'Humidity:    ' + f"{manager.pressure}" + ' hPa'
    
    def get_humidity_text(self):
        return 'Pressure:             ' + f"{manager.humidity}" + ' %'

    def create_right_air_conditions_tile(self):
        tile = DarkBlueBoxLayout(orientation='vertical', spacing=5)
        layout = DarkBlueBoxLayout(orientation='horizontal', spacing=5)
        layout2 = DarkBlueBoxLayout(orientation='horizontal', spacing=5)
        
        image = Image(source='images/Air_Pressure.png', size_hint=(None, 1), width=50)
        image2 = Image(source='images/Humidity_icon.png', size_hint=(None, 1), width=50)
        self.humidity = Label(text=self.get_humidity_text(), font_name='CustomFontB', color='black', font_size=20, halign='left', valign='middle')
        self.pressure = Label(text=self.get_pressure_text(), font_name='CustomFontB', color='black', font_size=20, halign='left', valign='middle')
        
        layout.add_widget(Label())
        layout.add_widget(image2)
        layout.add_widget(Label())
        layout.add_widget(self.pressure)  
        layout.add_widget(Label())
        layout.add_widget(Label())
        layout.add_widget(Label())    

        tile.add_widget(layout)

        layout2.add_widget(Label())
        layout2.add_widget(image)
        layout2.add_widget(Label())
        layout2.add_widget(self.humidity)  
        layout2.add_widget(Label())
        layout2.add_widget(Label())
        layout2.add_widget(Label())

        tile.add_widget(layout2)

        return tile

    def populate_hourly_forecast(self, container):
        hori = DarkBlueBoxLayout(orientation='horizontal', spacing=5)
        self.current_datetime = datetime.datetime.now(datetime.timezone.utc)
        hourly_labels = []
        hourly_times = []
        images_for_daily = []

        for i in range(7):
            vert = DarkBlueBoxLayout(orientation='vertical', spacing=5)
            image = Image(source=self.rawToPictureAddress(manager.hourly_desc[i]), size_hint=(None, None), size=(80, 80), pos_hint={'center_x': 0.5})
            vert.add_widget(Label())

            hourly_time = Label(text=f"{(int(self.current_datetime.hour) + int(self.get_time_difference()) + i) % 24}" + ":00", color=(0, 0, 0, 0.7), font_size=16, font_name='CustomFontR')
            hourly_times.append(hourly_time)
            vert.add_widget(Label())
            vert.add_widget(hourly_time)
            
            vert.add_widget(Label())
            vert.add_widget(Label())
            images_for_daily.append(image)
            vert.add_widget(image)
            
            hourly_label = Label(text=self.get_hourly_array(i) + '°', color='black', font_size=20, font_name='CustomFontB')
            hourly_labels.append(hourly_label)
            vert.add_widget(Label())
            vert.add_widget(hourly_label)

            hori.add_widget(vert)

        container.add_widget(hori)
        
        self.hourly_labels = hourly_labels
        self.hourly_times = hourly_times
        self.images_for_daily = images_for_daily

            
    def get_time_difference(self):
        return manager.time_zone
        
    def create_7_day_forecast_tile(self):
        tile = DarkBlueBoxLayout(orientation='vertical', spacing=5, size_hint_x=0.3)
        tile.add_widget(Label(text='7-Day Forecast', font_size=30, color='black', font_name='CustomFontB', halign='right', valign='middle'))

        current_datetime = datetime.datetime.now()
        current_day_of_week = current_datetime.strftime("%A")
        days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        current_day_index = days_of_week.index(current_day_of_week)

        week_desc = []
        week_temp = []

        for i in range(7):
            tile.add_widget(Label(text=f"{days_of_week[current_day_index]:<15}", font_size=25, font_name='CustomFontB', color='black', halign='center', valign='center'))
            current_day_index = (current_day_index + 1) % 7
            label = BoxLayout(orientation='horizontal', spacing=5)
            
            label.add_widget(Label())

            week_image = Image(source=self.rawToPictureAddress(manager.daily_desc[i]), size_hint=(None, None), size=(60, 60))
            week_desc.append(week_image)
            label.add_widget(week_image)
            label.add_widget(Label())

            week_temps = Label(text=f"{self.get_weekly_array(i)}°", font_size=30, color='black',  font_name='CustomFontI', halign='right', valign='top')
            week_temp.append(week_temps)
            label.add_widget(week_temps)
            label.add_widget(Label())

            tile.add_widget(label)
        tile.add_widget(Label())

        self.week_desc = week_desc
        self.week_temp = week_temp

        return tile
    
    def create_settings_tile(self):
        tile = GreyBoxLayout(orientation='vertical', spacing=20, size_hint_x=1,padding=10)

        # city
        box = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text='City:',size_hint_x=0.3))

        self.search_bar = TextInput(font_size=20,
                                    multiline=False,
                                    size_hint=(1, 1),
                                    padding=(10, 10),
                                    hint_text='City',
                                    font_name='CustomFontB',
                                    halign='center',
                                    text=manager.city)
        self.search_bar.bind(on_text_validate=self.applySettings)

        box.add_widget(self.search_bar)
        tile.add_widget(box)

        # units
        box = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text='Unit:',size_hint_x=0.3))
        if manager.unit == 'Metric':
            unit_text = 'Celsius'
        else:
            unit_text = 'Fahrenheit'
        self.unit_spinner = Spinner(text=unit_text, values=(
            'Celsius', 'Fahrenheit'), size_hint=(1, 1))
        box.add_widget(self.unit_spinner)
        tile.add_widget(box)

        # apply button
        btn = Button(text='Apply',
            on_press=self.applySettings,
            background_color=(.0, 1, .0, 1))
        tile.add_widget(btn)

        return tile

    def applySettings(self, instance):
        if self.unit_spinner.text == 'Celsius':
            unit = 'Metric'
        else:
            unit = 'Imperial'

        manager.updateSettings(self.search_bar.text,unit)
        self.settings_popupsettings_popup.dismiss()


if __name__ == '__main__':
    WeatherApp().run()
