import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window

class Prince(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.pressed_keys = set()


        self.sprites_path = "images"
        self.animations = {
            'walk_left': self.load_sprites('LeftRun'),
            'walk_right': self.load_sprites('RightRun'),
            'walk_up': self.load_sprites('UpRun'),
            'walk_down': self.load_sprites('DownRun'),
            'attack_left': self.load_sprites('LeftAttack'),
            'attack_right': self.load_sprites('RightAttack'),
            'attack_up': self.load_sprites('UpAttack'),
            'attack_down': self.load_sprites('DownAttack'),
        }

        self.current_animation = 'walk_down'
        self.current_frame = 0
        self.is_attacking = False
        self.hero_pos = [0, 0]  

        with self.canvas:
            self.hero = Rectangle(pos=self.hero_pos, size=(50, 50))

        Clock.schedule_interval(self.update_animation, 0.1)
        Clock.schedule_interval(self.move_step, 0)

    def load_sprites(self, folder_name):
        path = os.path.join(self.sprites_path, folder_name)
        return [os.path.join(path, file) for file in sorted(os.listdir(path)) if file.endswith('.png')]

    def update_animation(self, dt):
        frames = self.animations[self.current_animation]
        if frames:
            frame_path = frames[self.current_frame]
            self.hero.texture = Rectangle(source=frame_path).texture
            self.current_frame += 1

            if self.current_frame >= len(frames):
                if self.is_attacking and "attack" in self.current_animation:
                    self.is_attacking = False 
                self.current_frame = 0

    def change_animation(self, animation):
        if self.current_animation != animation:
            self.current_animation = animation
            self.current_frame = 0 

    def _on_keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_key_down)
        self._keyboard.unbind(on_key_up=self._on_key_up)
        self._keyboard = None

    def _on_key_down(self, keyboard, keycode, text, modifiers):
        self.pressed_keys.add(text)
        print("keydown",text)

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.pressed_keys:
            self.pressed_keys.remove(text)
            print("keyup")

    def move_step(self, dt):
        cur_x, cur_y = self.hero_pos
        step = 100 * dt
        is_moving = False

        if 'w' in self.pressed_keys:
            cur_y += step
            is_moving = True
            if not self.is_attacking:
                self.change_animation('walk_up')
        elif 's' in self.pressed_keys:
            cur_y -= step
            is_moving = True
            if not self.is_attacking:
                self.change_animation('walk_down')
        elif 'a' in self.pressed_keys:
            cur_x -= step
            is_moving = True
            if not self.is_attacking:
                self.change_animation('walk_left')
        elif 'd' in self.pressed_keys:
            cur_x += step
            is_moving = True
            if not self.is_attacking:
                self.change_animation('walk_right')
        if 'g' in self.pressed_keys:
            if not self.is_attacking:  
                self.is_attacking = True
                direction = self.current_animation.split('_')[1]  # ทิศทางปัจจุบัน (left, right, up, down)
                self.change_animation(f'attack_{direction}')
        if not is_moving and not self.is_attacking:
            self.current_frame = 0

        self.hero_pos = [cur_x, cur_y]
        self.hero.pos = self.hero_pos


class MainWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Prince())


class MyApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    app = MyApp()
    app.run()



