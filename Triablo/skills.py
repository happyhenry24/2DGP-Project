import pico2d
import math
import time

active_fire_paths = []


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

class FirePath:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.start_time = time.time()
        self.duration = 5
        self.create_frames = [
            pico2d.load_image(f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Fire_Arrow/tile{i:03}.png')
            for i in range(13)
        ]
        self.loop_frames = [
            pico2d.load_image(f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Fire_Arrow/tile{i:03}.png')
            for i in range(13, 26)
        ]
        self.destroy_frames = self.create_frames[::-1]
        self.frame_index = 0
        self.state = 'create'

    def update(self):
        elapsed = time.time() - self.start_time
        if elapsed > self.duration:
            self.state = 'destroy'
        elif elapsed > len(self.create_frames) * 0.1:
            self.state = 'loop'

        if self.state == 'create':
            self.frame_index = min(len(self.create_frames) - 1, int(elapsed / 0.1))
        elif self.state == 'loop':
            self.frame_index = int(elapsed / 0.1) % len(self.loop_frames)
        elif self.state == 'destroy':
            self.frame_index = min(len(self.destroy_frames) - 1, int(elapsed / 0.1))

    def draw(self, camera_x, camera_y):
        if self.state == 'create':
            frame = self.create_frames[self.frame_index]
        elif self.state == 'loop':
            frame = self.loop_frames[self.frame_index]
        elif self.state == 'destroy':
            frame = self.destroy_frames[self.frame_index]
        frame.draw(self.x - camera_x, self.y - camera_y)

    def is_active(self):
        return self.state != 'destroy' or self.frame_index < len(self.destroy_frames)


class FireArrow(Arrow):
    def __init__(self, x, y, target_x, target_y, image_path):
        super().__init__(x, y, target_x, target_y, image_path=image_path)

    def update(self, screen_width, screen_height, camera_x, camera_y):
        super().update(screen_width, screen_height, camera_x, camera_y)
        if self.is_active:
            if len(active_fire_paths) == 0 or \
               math.sqrt((self.x - active_fire_paths[-1].x) ** 2 + (self.y - active_fire_paths[-1].y) ** 2) >= 15:
                active_fire_paths.append(FirePath(self.x, self.y))

    def draw(self, camera_x, camera_y):
        super().draw(camera_x, camera_y)

def update_fire_paths(screen_width, screen_height, camera_x, camera_y, monsters):
    global active_fire_paths
    for fire_path in active_fire_paths:
        fire_path.update()

        for monster in monsters:
            if not monster.is_dead:
                distance_squared = (monster.x - fire_path.x) ** 2 + (monster.y - fire_path.y) ** 2
                if distance_squared <= (15 ** 2):
                    if not hasattr(monster, "last_damage_time") or time.time() - monster.last_damage_time >= 0.5:
                        monster.receive_damage(2)
                        monster.last_damage_time = time.time()
    active_fire_paths = [path for path in active_fire_paths if path.is_active()]


def draw_fire_paths(camera_x, camera_y):
    for fire_path in active_fire_paths:
        fire_path.draw(camera_x, camera_y)

class MultipleArrow:
    def __init__(self, x, y, base_angle, damage=2, image_path=None):
        self.arrows = []
        self.base_angle = base_angle
        self.create_arrows(x, y, damage, image_path)

    def create_arrows(self, x, y, damage, image_path):
        angles = [self.base_angle + offset for offset in [0, 10, 20, 30, -10, -20, -30]]
        for angle in angles:
            arrow = Arrow(
                x=x,
                y=y,
                target_x=x + math.cos(math.radians(angle)) * 100,
                target_y=y + math.sin(math.radians(angle)) * 100,
                damage=damage,
                image_path=image_path
            )
            self.arrows.append(arrow)

    def get_arrows(self):
        return self.arrows

class Explosion:
    def __init__(self, x, y, damage=10):
        self.x, self.y = x, y
        self.damage = damage
        self.frames = [
            pico2d.load_image(f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Explosion/tile{i:03}.png')
            for i in range(15)
        ]
        self.current_frame = 0
        self.active = True
        self.start_time = time.time()
        self.collision_detected = False

    def update(self, monsters):
        if not self.active:
            return
        elapsed_time = time.time() - self.start_time
        self.current_frame = int(elapsed_time * 15)
        if self.current_frame >= len(self.frames):
            self.active = False
        for monster in monsters:
            if not monster.is_dead:
                distance_squared = (monster.x - self.x) ** 2 + (monster.y - self.y) ** 2
                if distance_squared <= (150 ** 2):
                    monster.receive_damage(self.damage)

    def draw(self, camera_x, camera_y):
        if self.active:
            self.frames[self.current_frame].draw(self.x - camera_x, self.y - camera_y + 100)


class ExplodingArrow(Arrow):
    def __init__(self, x, y, target_x, target_y, image_path=None):
        super().__init__(x, y, target_x, target_y, damage=10, image_path=image_path)
        self.explosion_triggered = False

    def update(self, screen_width, screen_height, camera_x, camera_y, explosions, monsters):
        if not self.explosion_triggered:
            super().update(screen_width, screen_height, camera_x, camera_y)
            for monster in monsters:
                if math.sqrt((self.x - monster.x) ** 2 + (self.y - monster.y) ** 2) <= 30:
                    self.is_active = False
                    self.explosion_triggered = True
                    explosions.append(Explosion(self.x, self.y))
                    break

    def draw(self, camera_x, camera_y):
        if not self.explosion_triggered:
            super().draw(camera_x, camera_y)


class SkillsManager:
    def __init__(self):
        self.current_mode = None

    def handle_input(self, events):
        for event in events:
            if event.type == pico2d.SDL_KEYDOWN:
                if event.key == pico2d.SDLK_q:
                    self.switch_mode('Magic_Arrow')
                elif event.key == pico2d.SDLK_w:
                    self.switch_mode('Fire_Arrow')
                elif event.key == pico2d.SDLK_e:
                    self.switch_mode('Multiple_Arrow')
                elif event.key == pico2d.SDLK_r:
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
                return [MagicArrow(x, y, target_x, target_y)]
            else:
                return []
        elif self.current_mode == "Fire_Arrow":
            mana_cost = 10
            if character.mana >= mana_cost:
                character.mana = max(0, character.mana - mana_cost)
                return [
                    FireArrow(
                        x, y, target_x, target_y,
                        image_path='C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Arrow/tile004.png'
                    )
                ]
            else:
                return []
        if self.current_mode == "Multiple_Arrow":
            mana_cost = 7
            if character.mana >= mana_cost:
                character.mana = max(0, character.mana - mana_cost)
                base_angle = math.degrees(math.atan2(target_y - y, target_x - x))
                multi_arrow = MultipleArrow(
                    x, y, base_angle, damage=2,
                    image_path='C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Arrow/tile004.png'
                )
                return multi_arrow.get_arrows()
            else:
                return []
        if self.current_mode == "Exploding_Arrow":
            mana_cost = 10
            if character.mana >= mana_cost:
                character.mana = max(0, character.mana - mana_cost)
                return [
                    ExplodingArrow(
                        x, y, target_x, target_y,
                        image_path='C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Arrow/tile004.png'
                    )
                ]
            else:
                return []

        return [
            Arrow(
                x, y, target_x, target_y,
                image_path='C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Arrow/tile004.png'
            )
        ]


    def get_current_mode(self):
        return self.current_mode or "None"
