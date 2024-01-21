from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout

class DarkBlueBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(DarkBlueBoxLayout, self).__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self._update_rect()

    def _update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.2, 0.8, 1, 1)  # Light blue background color
            Rectangle(pos=self.pos, size=self.size)

class GreyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(GreyBoxLayout, self).__init__(**kwargs)
        self.bind(size=self._update_rect, pos=self._update_rect)
        self._update_rect()

    def _update_rect(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0.5, 0.5, 0.5, 1)  # Light blue background color
            Rectangle(pos=self.pos, size=self.size)