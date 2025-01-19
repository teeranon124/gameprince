import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from random import choice, randint
from kivy.graphics import Color, Rectangle

class Door(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_on_door = False
        self.door_timer = None

    def check_collision(self, prince_rect):
        door_rect = self.pos[0], self.pos[1], self.size[0], self.size[1]
        if self.collides(prince_rect, door_rect):
            if not self.is_on_door :
                self.is_on_door = True
                self.door_timer = Clock.schedule_once(self.next_stage, 3)
        else:
            if self.is_on_door:
                self.is_on_door = False
                if self.door_timer:
                    self.door_timer.cancel()

    @staticmethod
    def collides(rect1, rect2):
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        return not (x1 > x2 + w2 or x1 + w1 < x2 or y1 > y2 + h2 or y1 + h1 < y2)

    def next_stage(self, dt):
        current_screen = self.parent.parent.manager.current 

        if current_screen == "game":  
            self.parent.parent.manager.current = "stage_two"  
        elif current_screen == "stage_two":  
            self.parent.parent.manager.current = "stage_three" 

class Prince(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._on_keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_key_down)
        self._keyboard.bind(on_key_up=self._on_key_up)
        self.pressed_keys = set()
        self.hp = 100
        self.dm = 20

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
            self.hero = Rectangle(pos=self.hero_pos, size=(100, 100))
            
            Color(0.7, 0.7, 0.7, 1)  
            self.hp_bg = Rectangle(pos=(self.hero_pos[0], self.hero_pos[1] + 110), 
                                 size=(100, 10))
            
            Color(0, 0, 1, 1)  
            self.hp_bar = Rectangle(pos=(self.hero_pos[0], self.hero_pos[1] + 110), 
                                  size=(100 * (self.hp/100), 10))

        Clock.schedule_interval(self.update_animation, 0.1)
        Clock.schedule_interval(self.move_step, 0)
        Clock.schedule_interval(self.update_hp_bar, 1/60)

    def update_hp_bar(self, dt):
        self.hp_bg.pos = (self.hero_pos[0], self.hero_pos[1] + 110)
        self.hp_bar.pos = (self.hero_pos[0], self.hero_pos[1] + 110)
        self.hp_bar.size = (100 * (self.hp/100), 10)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            App.get_running_app().root.current = "game_over"  # เปลี่ยนเป็นแบบนี้
        print(f"Prince HP: {self.hp}")



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

    def _on_key_up(self, keyboard, keycode):
        text = keycode[1]
        if text in self.pressed_keys:
            self.pressed_keys.remove(text)

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
                direction = self.current_animation.split('_')[1]
                self.change_animation(f'attack_{direction}')

        if not is_moving and not self.is_attacking:
            self.current_frame = 0

        self.hero_pos = [cur_x, cur_y]
        self.hero.pos = self.hero_pos
        
        door = self.parent.ids.door
        prince_rect = self.hero_pos[0], self.hero_pos[1], self.hero.size[0], self.hero.size[1]
        door.check_collision(prince_rect) 

        for i, j in self.parent.ids.items():
            if "monster" in i and j.parent:
                j.check_collision(prince_rect)
                j.check_attack_collision(prince_rect, self.is_attacking)
                j.attack_prince(prince_rect, self)

class Monster(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # สุ่มตำแหน่งเริ่มต้นจากซ้ายหรือขวาของจอ
        screen_width = Window.width
        screen_height = Window.height
        side = choice(['left', 'right'])
        y_pos = randint(50, screen_height - 50)
        self.pos = (0, y_pos) if side == 'left' else (screen_width, y_pos)
        self.direction = [-1, 1][side == 'left']  # ซ้าย -1, ขวา +1
        self.speed = randint(150, 250)  # กำหนดความเร็วสุ่ม
        self.vertical_speed = randint(-100, 100)  # ความเร็วแนวตั้ง

        self.hp = 200
        self.dm = 10
        self.is_hit = False
        self.can_attack = True
        
        # สร้าง sprite และ health bar
        with self.canvas:
            Color(0.7, 0.7, 0.7, 1)
            self.hp_bg = Rectangle(pos=(self.pos[0], self.pos[1] + 60), size=(80, 8))
            Color(1, 0, 0, 1)
            self.hp_bar = Rectangle(pos=(self.pos[0], self.pos[1] + 60), size=(80 * (self.hp / 200), 8))

        # Schedule updates
        Clock.schedule_interval(self.update_position, 1 / 60)
        Clock.schedule_interval(self.update_hp_bar, 1 / 60)

    def update_position(self, dt):
        screen_width = Window.width
        screen_height = Window.height

        # อัปเดตตำแหน่ง
        new_x = self.pos[0] + self.direction * self.speed * dt
        new_y = self.pos[1] + self.vertical_speed * dt

        # ชนขอบหน้าจอแล้วเปลี่ยนทิศทาง
        if new_x <= 0 or new_x >= screen_width - self.size[0]:
            self.direction *= -1  # กลับทิศทาง
        if new_y <= 0 or new_y >= screen_height - self.size[1]:
            self.vertical_speed *= -1  # กลับทิศทางแนวตั้ง

        self.pos = (new_x, new_y)

    def update_hp_bar(self, dt):
        self.hp_bg.pos = (self.pos[0], self.pos[1] + 60)
        self.hp_bar.pos = (self.pos[0], self.pos[1] + 60)
        self.hp_bar.size = (80 * (self.hp / 200), 8)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            print("Monster defeated!")
            if self.parent:
                self.parent.remove_widget(self)


    def check_attack_collision(self, prince_rect, is_attacking):
        monster_rect = self.pos[0], self.pos[1], self.size[0], self.size[1]
        if is_attacking and Door.collides(prince_rect, monster_rect):
            if not self.is_hit:
                self.hp -= 20
                print(f"Monster HP: {self.hp}")
                self.is_hit = True
                if self.hp <= 0:
                    print("Monster defeated!")
                    if self.parent:
                        Clock.unschedule(self.reset_attack)
                        Clock.unschedule(self.update_position)
                        Clock.unschedule(self.update_hp_bar)
                        self.parent.remove_widget(self)
        else:
            self.is_hit = False

    def reset_attack(self, dt):
        self.can_attack = True

    def check_collision(self, prince_rect):
        monster_rect = self.pos[0], self.pos[1], self.size[0], self.size[1]
        if Door.collides(prince_rect, monster_rect):
            if not self.is_on_monster:
                self.is_on_monster = True
                print("Monster collision detected!")
        else:
            self.is_on_monster = False

 

    def attack_prince(self, prince_rect, prince_obj):
        monster_rect = self.pos[0], self.pos[1], self.size[0], self.size[1]
        if Door.collides(prince_rect, monster_rect) and self.can_attack:
            prince_obj.take_damage(self.dm)
            self.can_attack = False  
            print("Monster attacks Prince!")

class GameOver(Screen):
    pass


class MenuScreen(Screen):
    pass

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer = 120  # เวลาจับเวลา (30 วินาที)
        self.timer_event = None

    def on_enter(self, *args):
        self.timer = 120  # ตั้งค่าเวลาสำหรับด่านแรก
        self.start_timer()
        self.add_widget(Prince())
        # เพิ่ม Monster ลงในด่าน

    def start_timer(self):
        if self.timer_event:
            self.timer_event.cancel()  # ยกเลิกตัวจับเวลาที่อาจทำงานอยู่
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        self.timer -= 1
        self.check = False
        print(f"Time left: {self.timer}s")  # แสดงเวลาที่เหลือใน Console
        for widget in self.walk():
            if isinstance(widget, Monster):
                print(widget)
                self.check = True
        if not self.check :
            self.manager.current = "menu"

        if self.timer <= 0:
            self.timer_event.cancel()
            self.end_game(False)  # เวลาหมดถือว่าแพ้เกม

    def check_monsters_remaining(self):
        monsters = [child for child in self.children if isinstance(child, Monster)]
        if not monsters:  # ไม่มี Monster เหลือ
            self.timer_event.cancel()
            self.end_game(True)  # ผ่านด่านสำเร็จ

    def end_game(self, success):
        if success:
            self.manager.current = "menu"
        else:
            print("Time's up! Game Over!")
            self.manager.current = "game_over"
    



class GameScreenTwo(Screen):
    def on_enter(self, *args):
        self.add_widget(Prince())

class GameScreenThree(Screen):
    def on_enter(self, *args):
        self.add_widget(Prince())

class GameApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))
        sm.add_widget(GameScreen(name="game"))
        sm.add_widget(GameOver(name = "game_over"))
        sm.add_widget(GameScreenTwo(name="stage_two"))
        sm.add_widget(GameScreenThree(name="stage_three"))
        return sm
    

if __name__ == '__main__':
    GameApp().run()