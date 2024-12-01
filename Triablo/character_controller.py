import pico2d
import math
import time
import monster_controller as mc

from skills import MagicArrow


direction_angle_mapping = {
    'S': (258.75, 281.25), 'SSW': (236.25, 258.75), 'SW': (213.75, 236.25), 'WSW': (191.25, 213.75),
    'W': (168.75, 191.25), 'WNW': (146.25, 168.75), 'NW': (123.75, 146.25), 'NNW': (101.25, 123.75),
    'N': (78.75, 101.25), 'NNE': (56.25, 78.75), 'NE': (33.75, 56.25), 'ENE': (11.25, 33.75),
    'E': (348.75, 11.25), 'ESE': (326.25, 348.75), 'SE': (303.75, 326.25), 'SSE': (281.25, 303.75)
}


walk_sprites = {}
idle_sprites = {}
attack_sprites = {}
dead_sign = None

def load_character_sprites():
    global walk_sprites, idle_sprites, attack_sprites, dead_sign

    walk_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Walk/tile{frame_idx:03}.png')
            for frame_idx in range(8 * idx, 8 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping.keys())
    }

    idle_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Idle/tile{frame_idx:03}.png')
            for frame_idx in range(8 * idx, 8 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping.keys())
    }

    attack_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Attack/tile{frame_idx:03}.png')
            for frame_idx in range(14 * idx, 14 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping.keys())
    }

    dead_sign = pico2d.load_image('C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/DeadSign.png')

class Character:
    def __init__(self):
        self.x, self.y = 3200, 3200
        self.spawn_x, self.spawn_y = self.x, self.y
        self.hp = 62
        self.is_dead = False
        self.target_x, self.target_y = self.x, self.y
        self.frame = 0
        self.direction = 'S'
        self.speed = 5
        self.is_moving = False
        self.frame_delay = 0
        self.frame_speed = 5
        self.mouse_down_time = 0
        self.mouse_held = False
        self.is_following_mouse = False
        self.is_attacking = False
        self.attack_frame = 0
        self.attack_frame_speed = 1.0
        self.attack_cooldown = False
        self.arrows = []
        self.attack_cooldown_time = 0.5
        self.last_attack_time = 0
        self.mouse_held = False
        self.keyboard_active = False
        self.skills_manager = None
        self.mana = 62

    def take_damage(self, damage):
        if not self.is_dead:
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                self.is_dead = True

    def attack_monster(self, monster):
        damage = 2
        mc.monster_hit(monster, damage)

    def respawn(self):
        self.x, self.y = self.spawn_x, self.spawn_y
        self.hp = 62
        self.is_dead = False

    def update(self, camera_x, camera_y):
        if not self.is_dead:
            if self.is_attacking:
                self.attack_frame += self.attack_frame_speed
                if self.attack_frame >= len(attack_sprites[self.direction]):
                    self.is_attacking = False
                    self.attack_frame = 0
            elif self.is_moving:
                dx, dy = self.target_x - self.x, self.target_y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < self.speed:
                    self.x, self.y = self.target_x, self.target_y
                    if not self.mouse_held:
                        self.is_moving = False
                else:
                    self.x += (dx / distance) * self.speed
                    self.y += (dy / distance) * self.speed

                self.frame_delay = (self.frame_delay + 1) % self.frame_speed
                if self.frame_delay == 0:
                    self.frame = (self.frame + 1) % len(walk_sprites[self.direction])
            else:
                self.frame_delay = (self.frame_delay + 1) % self.frame_speed
                if self.frame_delay == 0:
                    self.frame = (self.frame + 1) % len(idle_sprites[self.direction])
        for arrow in self.arrows:
            arrow.update(800, 600, camera_x, camera_y)
        self.arrows = [arrow for arrow in self.arrows if arrow.is_active]

    def draw(self, camera_x, camera_y, walk_sprites, idle_sprites, attack_sprites):
        if not self.is_dead:
            if self.is_attacking:
                attack_sprites[self.direction][int(self.attack_frame)].draw(self.x - camera_x, self.y - camera_y)
            elif self.is_moving:
                walk_sprites[self.direction][self.frame].draw(self.x - camera_x, self.y - camera_y)
            else:
                idle_sprites[self.direction][self.frame].draw(self.x - camera_x, self.y - camera_y)
        for arrow in self.arrows:
            arrow.draw(camera_x, camera_y)

    def draw_death_message(self):
        if self.is_dead:
            global dead_sign
            screen_width, screen_height = 800, 600
            dead_sign.draw(screen_width // 2, screen_height // 2)

    def move_to(self, x, y):
        if not self.is_dead and not self.is_attacking:
            self.target_x, self.target_y = x, y
            self.is_moving = True
            self.direction = self.calculate_direction(x, y)

    def attack(self, target_x, target_y):
        current_time = time.time()
        if not self.is_dead and current_time - self.last_attack_time >= self.attack_cooldown_time:
            self.last_attack_time = current_time
            self.direction = self.calculate_direction(target_x, target_y)

            arrows = self.skills_manager.create_arrow(self.x, self.y, target_x, target_y, self)
            if arrows:
                self.arrows.extend(arrows)
                self.is_attacking = True

    def calculate_direction(self, target_x, target_y):
        angle = math.degrees(math.atan2(target_y - self.y, target_x - self.x))
        if angle < 0:
            angle += 360

        for direction, (min_angle, max_angle) in direction_angle_mapping.items():
            if min_angle <= max_angle:
                if min_angle <= angle < max_angle:
                    return direction
            else:
                if angle >= min_angle or angle < max_angle:
                    return direction
        return 'S'

    def stop(self):
        self.is_moving = False
        self.target_x = self.x
        self.target_y = self.y

    def handle_event(self, event, camera):
        if event.type == pico2d.SDL_MOUSEBUTTONDOWN:
            if event.button == pico2d.SDL_BUTTON_RIGHT:
                self.mouse_held = True
                mouse_x = (event.x if event.x is not None else 0) + camera.x
                mouse_y = (600 - (event.y if event.y is not None else 0)) + camera.y
                self.move_to(mouse_x, mouse_y)
            elif event.button == pico2d.SDL_BUTTON_LEFT:
                mouse_x = (event.x if event.x is not None else 0) + camera.x
                mouse_y = (600 - (event.y if event.y is not None else 0)) + camera.y
                self.attack(mouse_x, mouse_y)

        elif event.type == pico2d.SDL_MOUSEBUTTONUP and event.button == pico2d.SDL_BUTTON_RIGHT:
            self.mouse_held = False
            self.stop()

        if event.type == pico2d.SDL_MOUSEMOTION and self.mouse_held:
            mouse_x = event.x + camera.x
            mouse_y = 600 - event.y + camera.y
            self.move_to(mouse_x, mouse_y)
            self.is_moving = True


def handle_character_events(character, camera, monsters):
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            return False
        elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return False
        elif character.is_dead:
            return character.handle_event(event, camera)
        elif event.type == pico2d.SDL_MOUSEBUTTONDOWN:
            if event.button == pico2d.SDL_BUTTON_RIGHT:
                character.mouse_held = True
        elif event.type == pico2d.SDL_MOUSEBUTTONUP and event.button == pico2d.SDL_BUTTON_RIGHT:
            character.mouse_held = False
            character.stop()
        elif event.type == pico2d.SDL_MOUSEMOTION and character.mouse_held:
            mouse_x = (event.x if event.x is not None else 0) + camera.x
            mouse_y = (600 - (event.y if event.y is not None else 0)) + camera.y
            character.x += (mouse_x - character.x) * 0.1
            character.y += (mouse_y - character.y) * 0.1
            character.direction = character.calculate_direction(mouse_x, mouse_y)
    return True
