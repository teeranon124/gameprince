from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.graphics import Rectangle
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.core.window import Window

class prince(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.pressed_keys = set()
        Clock.schedule_interval(self.move_step, 0)
        with self.canvas:
            self.hero = Rectangle(source='hero.png', pos=(0, 0), size=(100,
            100))
    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None
    def _on_key_down(self, keyboard, keycode, text, modifiers):
        print('down', text)
        self.pressed_keys.add(text)
    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        print('up', text)
        if text in self.pressed_keys:
            self.pressed_keys.remove(text)
    def move_step(self, dt):
        cur_x = self.hero.pos[0]
        cur_y = self.hero.pos[1]
        step = 100*dt
        if 'w' in self.pressed_keys:
            cur_y += step
        if 's' in self.pressed_keys:
            cur_y -= step
        if 'a' in self.pressed_keys:
            cur_x -= step
        if 'd' in self.pressed_keys:
            cur_x += step
        self.hero.pos = (cur_x, cur_y)
class MyApp(App):
    def build(self):
        return prince()
if __name__ == '__main__':
    app = MyApp()
    app.run()