import pico2d
import math
import time

direction_angle_mapping = {
    'S': (247.5, 292.5), 'SSW': (225.0, 247.5), 'SW': (202.5, 225.0), 'SWW': (180.0, 202.5),
    'W': (157.5, 180.0), 'NWW': (135.0, 157.5), 'NW': (112.5, 135.0), 'NNW': (90.0, 112.5),
    'N': (67.5, 90.0), 'NNE': (45.0, 67.5), 'NE': (22.5, 45.0), 'NEE': (0.0, 22.5),
    'E': (337.5, 360.0), 'SEE': (315.0, 337.5), 'SE': (292.5, 315.0), 'SSE': (270.0, 292.5)
}

walk_sprites = {}
idle_sprites = {}
attack_sprites = {}
highlight = None
dead_sign = None

def load_character_sprites():
    global walk_sprites, idle_sprites, attack_sprites, highlight, dead_sign

    walk_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Walk/tile{frame_idx:03}.png')
            for frame_idx in range(8 * idx, 8 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping)
    }

    idle_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Idle/tile{frame_idx:03}.png')
            for frame_idx in range(8 * idx, 8 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping)
    }

    attack_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Attack/tile{frame_idx:03}.png')
            for frame_idx in range(14 * idx, 14 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping)
    }

    highlight = pico2d.load_image(
        'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/user interface/highlight/highlight_yellow.png')

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
        global highlight
        self.highlight = highlight

    def take_damage(self, damage):
        if not self.is_dead:
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                self.is_dead = True
                print("당신은 죽었습니다.")

    def respawn(self):
        self.x, self.y = self.spawn_x, self.spawn_y
        self.hp = 62
        self.is_dead = False

    def update(self):
        if not self.is_dead:
            if self.is_attacking:
                self.attack_frame += self.attack_frame_speed
                if self.attack_frame >= 14:
                    self.is_attacking = False
                    self.attack_cooldown = False
                    self.attack_frame = 0
            elif self.is_moving:
                dx, dy = self.target_x - self.x, self.target_y - self.y
                distance = math.sqrt(dx ** 2 + dy ** 2)
                if distance < self.speed:
                    self.x, self.y = self.target_x, self.target_y
                    self.is_moving = False
                else:
                    self.x += (dx / distance) * self.speed
                    self.y += (dy / distance) * self.speed

                self.frame_delay = (self.frame_delay + 1) % self.frame_speed
                if self.frame_delay == 0:
                    self.frame = (self.frame + 1) % 8
            else:
                self.frame_delay = (self.frame_delay + 1) % self.frame_speed
                if self.frame_delay == 0:
                    self.frame = (self.frame + 1) % 8

    def draw(self, camera_x, camera_y, walk_sprites, idle_sprites, attack_sprites):
        if not self.is_dead:
            self.highlight.draw(self.x - camera_x, self.y - camera_y)

            if self.is_attacking:
                attack_sprites[self.direction][int(self.attack_frame)].draw(self.x - camera_x, self.y - camera_y)
            elif self.is_moving:
                walk_sprites[self.direction][self.frame].draw(self.x - camera_x, self.y - camera_y)
            else:
                idle_sprites[self.direction][self.frame].draw(self.x - camera_x, self.y - camera_y)

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
        if not self.is_dead and not self.attack_cooldown:
            self.is_attacking = True
            self.attack_cooldown = True
            self.is_moving = False
            self.direction = self.calculate_direction(target_x, target_y)

    def calculate_direction(self, target_x, target_y):
        angle = math.degrees(math.atan2(target_y - self.y, target_x - self.x))
        if angle < 0:
            angle += 360
        for direction, (min_angle, max_angle) in direction_angle_mapping.items():
            if min_angle <= angle < max_angle:
                return direction
        return 'S'

    def stop(self):
        self.is_moving = False
        self.is_following_mouse = False

    def handle_event(self, event):
        if self.is_dead:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_RETURN:
                    self.respawn()
                    return True
                elif event.key == pico2d.SDLK_ESCAPE:
                    return False
            return True
        return True

def handle_character_events(character, camera, monsters):
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            return False
        elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return False
        elif character.is_dead:
            return character.handle_event(event)
        elif event.type == pico2d.SDL_MOUSEBUTTONDOWN and event.button == pico2d.SDL_BUTTON_RIGHT:
            character.mouse_down_time = time.time()
            character.mouse_held = True
        elif event.type == pico2d.SDL_MOUSEBUTTONUP and event.button == pico2d.SDL_BUTTON_RIGHT:
            character.mouse_held = False
            elapsed_time = time.time() - character.mouse_down_time
            mouse_x, mouse_y = event.x + camera.x, 600 - event.y + camera.y

            if elapsed_time < 0.2:
                for monster in monsters:
                    distance = math.sqrt((monster.x - mouse_x) ** 2 + (monster.y - mouse_y) ** 2)
                    if distance <= 50:
                        monster.hit()
                        break
                if not character.is_attacking:
                    character.attack(mouse_x, mouse_y)
            else:
                character.stop()
        elif character.mouse_held and time.time() - character.mouse_down_time >= 0.2:
            character.is_following_mouse = True
            character.move_to(event.x + camera.x, 600 - event.y + camera.y)
    return True
