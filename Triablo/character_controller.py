import time
import math
import pico2d

direction_angle_mapping = {
    'E': '0.0', 'NE': '45.0', 'N': '90.0', 'NNE': '67.5', 'NEE': '22.5',
    'NW': '135.0', 'NNW': '112.5', 'NWW': '157.5', 'S': '270.0',
    'SE': '315.0', 'SEE': '337.5', 'SSE': '292.5', 'SSW': '247.5',
    'SW': '225.0', 'SWW': '202.5', 'W': '180.0'
}

class Character:
    def __init__(self):
        self.x, self.y = 3200, 3200
        self.target_x, self.target_y = self.x, self.y
        self.frame = 0
        self.direction = 'E'
        self.speed = 5
        self.is_moving = False
        self.frame_delay = 0
        self.frame_speed = 5
        self.mouse_down_time = 0
        self.mouse_held = False
        self.is_following_mouse = False

        self.highlight = pico2d.load_image('C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/user interface/highlight/highlight_yellow.png')

    def update(self):
        if self.is_moving:
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
            self.frame = 0

    def draw(self, camera_x, camera_y, walk_sprites, idle_sprites):

        self.highlight.draw(self.x - camera_x, self.y - camera_y)

        if self.is_moving:
            walk_sprites[self.direction][self.frame].draw(self.x - camera_x, self.y - camera_y)
        else:
            idle_sprites[self.direction].draw(self.x - camera_x, self.y - camera_y)

    def move_to(self, x, y):
        self.target_x, self.target_y = x, y
        self.is_moving = True
        self.direction = self.calculate_direction(x, y)

    def calculate_direction(self, target_x, target_y):
        angle = math.degrees(math.atan2(target_y - self.y, target_x - self.x))
        if angle < 0:
            angle += 360

        if 337.5 <= angle < 360 or 0 <= angle < 22.5:
            return 'E'
        elif 22.5 <= angle < 45.0:
            return 'NEE'
        elif 45.0 <= angle < 67.5:
            return 'NE'
        elif 67.5 <= angle < 90.0:
            return 'N'
        elif 90.0 <= angle < 112.5:
            return 'NNE'
        elif 112.5 <= angle < 135.0:
            return 'NNW'
        elif 135.0 <= angle < 157.5:
            return 'NW'
        elif 157.5 <= angle < 180.0:
            return 'NWW'
        elif 180.0 <= angle < 202.5:
            return 'W'
        elif 202.5 <= angle < 225.0:
            return 'SWW'
        elif 225.0 <= angle < 247.5:
            return 'SW'
        elif 247.5 <= angle < 270.0:
            return 'SSW'
        elif 270.0 <= angle < 292.5:
            return 'S'
        elif 292.5 <= angle < 315.0:
            return 'SSE'
        elif 315.0 <= angle < 337.5:
            return 'SE'
        else:
            return 'E'

    def stop(self):
        self.is_moving = False
        self.is_following_mouse = False

class Camera:
    def __init__(self, width, height):
        self.x, self.y = 0, 0
        self.width, self.height = width, height

    def update(self, target_x, target_y):
        self.x = target_x - self.width // 2
        self.y = target_y - self.height // 2

def handle_character_events(character, camera):
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT:
            return False
        elif event.type == pico2d.SDL_MOUSEBUTTONDOWN and event.button == pico2d.SDL_BUTTON_RIGHT:
            character.mouse_down_time = time.time()
            character.mouse_held = True
        elif event.type == pico2d.SDL_MOUSEBUTTONUP and event.button == pico2d.SDL_BUTTON_RIGHT:
            character.mouse_held = False
            elapsed_time = time.time() - character.mouse_down_time
            if elapsed_time < 0.2:
                character.move_to(event.x + camera.x, 600 - event.y + camera.y)
            else:
                character.stop()
        elif character.mouse_held and time.time() - character.mouse_down_time >= 0.2:
            character.is_following_mouse = True
            character.move_to(event.x + camera.x, 600 - event.y + camera.y)
    return True
