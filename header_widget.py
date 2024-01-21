from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout 
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from weather_manager import manager


class HeaderWidget(RelativeLayout):
    def __init__(self, **args):
        super(HeaderWidget, self).__init__(**args)
        btn = Button(text ='BTN',
            font_size = 40,
            size_hint = (None,None),
            size = (50,80),
            pos_hint = {'right': 0.95, 'bottom': 1},
            on_press=self.showSettings, 
            background_color =(.0, .0, .0, .0)) 
        self.add_widget(btn)
        
        self.cityLabel = Label(text=self.get_cityLabel_text(), pos_hint = {'left' : 0,'top' : 1},
            size_hint_y = 0.5,size_hint_x = None,font_size = 50)
        self.cityLabel.bind(texture_size=self.cityLabel.setter('size'))
        self.tempLabel = Label(text=self.get_tempLabel_text(), pos_hint = {'left' : 0,'top' : 0.5},
            size_hint_y = 0.5,size_hint_x = None,font_size = 50)
        self.tempLabel.bind(texture_size=self.tempLabel.setter('size'))
        self.descLabel = Label(text=self.get_descLabel_text(), pos_hint = {'x' : 0.3,'top' : 0.4},
            size_hint_y = 0.5,size_hint_x = None)
        self.descLabel.bind(texture_size=self.descLabel.setter('size'))
       
        self.settingsLayout = None
        manager.bind(on_change = self.updateView)
     
    def updateView(self,instance,value):
        self.cityLabel.text = self.get_cityLabel_text()
        self.tempLabel.text = self.get_tempLabel_text()
        self.descLabel.text = self.get_descLabel_text()
        
    def get_cityLabel_text(self):
        return f"{manager.city}"
    
    def get_tempLabel_text(self):
        unit = 'C' if manager.unit == 'Metric' else 'F'
        return f"{round(manager.temperature)}°{unit}"
    
    def get_descLabel_text(self):
        return f"{manager.weather_description}"    
       
    def showSettings(self, instance):
        if self.settingsLayout != None:
            return 
        self.settingsLayout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        grid = GridLayout(cols=4,
            rows = 2, 
            spacing = 10, 
            size_hint_x = 0.85, 
            size_hint_y = 0.3,
            pos_hint = {'left': 0, 'top': 1})
        grid.add_widget(Label(text='City:'))
        self.city_spinner = Spinner(text=manager.city, values=(
            'Lodz', 'Warsaw','Marrakesh'), size_hint=(1, 0.1))
        grid.add_widget(self.city_spinner)
        grid.add_widget(Label(text='Unit:'))
        self.unit_spinner = Spinner(text=manager.unit, values=(
            'Metric', 'Imperial'), size_hint=(1, 0.1))
        grid.add_widget(self.unit_spinner)
        btn = Button(text ='Apply',
            on_press=self.applySettings, 
            background_color =(.0, 1, .0, 1)) 
        grid.add_widget(btn)
        self.settingsLayout.add_widget(grid)
        self.add_widget(self.settingsLayout)
        self.settingsLayout.bind(size=self.updateRect, pos=self.updateRect)
        with self.settingsLayout.canvas.before:
            Color(0.5, 0.5, 0.5, 1) 
            self.rect = Rectangle(size=self.settingsLayout.size, pos=self.settingsLayout.pos)

    def updateRect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
                    
    def applySettings(self, instance):
        manager.updateSettings(self.city_spinner.text,self.unit_spinner.text)
        self.remove_widget(self.settingsLayout)
        self.settingsLayout = None