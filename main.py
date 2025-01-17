import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

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
        self.is_on_door = False  # ตรวจสอบสถานะว่าตัวละครอยู่บนประตูหรือไม่
        self.door_timer = None  # ใช้สำหรับจับเวลา  

        with self.canvas:
            self.hero = Rectangle(pos=self.hero_pos, size=(100, 100))

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
        self.hero_pos = [cur_x, cur_y]
        self.hero.pos = self.hero_pos

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
        self.check_collision_with_door()
    
    def check_collision_with_door(self):
        door = self.parent.ids.door  # เข้าถึงวัตถุประตูจาก kv
        prince_rect = self.hero_pos[0], self.hero_pos[1], self.hero.size[0], self.hero.size[1]
        door_rect = door.pos[0], door.pos[1], door.size[0], door.size[1]

        if self.collides(prince_rect, door_rect):
            if not self.is_on_door:
                self.is_on_door = True
                self.door_timer = Clock.schedule_once(self.enter_next_level, 3)  # เริ่มจับเวลา 3 วินาที
        else:
            if self.is_on_door:
                self.is_on_door = False
                if self.door_timer:
                    self.door_timer.cancel()  # ยกเลิก timer หากออกจากประตู
    @staticmethod
    def collides(rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return not (x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2)

    def enter_next_level(self, dt):
        self.parent.manager.current = "next_level"  # เปลี่ยนเป็นหน้าจอถัดไป

class Door(Widget):
    pass


class MenuScreen(Screen):
    pass


class GameScreen(Screen):
    def on_enter(self, *args):
        self.add_widget(Prince())  


class GameScreenTwo(Screen):
    def on_enter(self, *args):
        self.add_widget(Prince()) 


class GameApp(App):
    def build(self):
        Builder.load_file("game.kv") 
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameScreenTwo(name="next_level"))  # เพิ่มหน้าจอใหม่
        return sm


if __name__ == '__main__':
    GameApp().run()



