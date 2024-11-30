import pico2d
import math

class Arrow:
    def __init__(self, x, y, target_x, target_y, damage=2, image_path=None):
        self.x, self.y = x, y
        self.speed = 10
        self.damage = damage
        self.angle = math.degrees(math.atan2(target_y - y, target_x - x))
        self.image = pico2d.load_image(image_path) if image_path else None
        self.is_active = True

    def update(self, screen_width, screen_height, camera_x, camera_y):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        if self.x < camera_x or self.y < camera_y or self.x > camera_x + screen_width or self.y > camera_y + screen_height:
            self.is_active = False

    def draw(self, camera_x, camera_y):
        if self.image and self.is_active:
            self.image.rotate_draw(math.radians(self.angle), self.x - camera_x, self.y - camera_y)

class MagicArrow(Arrow):
    def __init__(self, x, y, target_x, target_y):
        super().__init__(x, y, target_x, target_y, damage=10)
        self.images = [
            pico2d.load_image(f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Magic_Arrow/tile{i:03}.png')
            for i in range(16, 20)
        ]
        self.frame = 0

    def update(self, screen_width, screen_height, camera_x, camera_y):
        super().update(screen_width, screen_height, camera_x, camera_y)
        if self.is_active:
            self.frame = (self.frame + 1) % len(self.images)

    def draw(self, camera_x, camera_y):
        if self.images and self.is_active:
            self.images[self.frame].rotate_draw(math.radians(self.angle), self.x - camera_x, self.y - camera_y)



class SkillsManager:
    def __init__(self):
        self.current_mode = None

    def handle_input(self, events):
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_1:
                    self.switch_mode('Magic_Arrow')
                elif event.key == pico2d.SDLK_2:
                    self.switch_mode('Fire_Arrow')
                elif event.key == pico2d.SDLK_3:
                    self.switch_mode('Multiple_Arrow')
                elif event.key == pico2d.SDLK_4:
                    self.switch_mode('Exploding_Arrow')

    def switch_mode(self, new_mode):
        if self.current_mode != new_mode:
            self.current_mode = new_mode
        else:
            self.current_mode = None

    def create_arrow(self, x, y, target_x, target_y, character):
        if self.current_mode == "Magic_Arrow":
            mana_cost = 5
            if character.mana >= mana_cost:
                character.mana = max(0, character.mana - mana_cost)
                return MagicArrow(x, y, target_x, target_y)
            else:
                return None
        return Arrow(x, y, target_x, target_y,
                     image_path='C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Arrow/tile004.png')

    def get_current_mode(self):
        return self.current_mode or "None"
