from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout 
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from weather_manager import manager
from header_widget import HeaderWidget

        
class WeatherApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        header = HeaderWidget(size_hint_y = 0.2)
        layout.add_widget(header)
        body = RelativeLayout()
        layout.add_widget(body)
        return layout 
 
    def on_start(self):
        self.root_window.bind(on_resize=self._update_rect,
                              on_show=self._update_rect)
        with self.root.canvas.before:
            Color(0, 0.5, 0.5, 1)  
            self.rect = Rectangle(size=self.root.size, pos=self.root.pos)

    def _update_rect(self, instance, width, height):
        self.rect.size = instance.size
    
if __name__ == '__main__':
    WeatherApp().run()
