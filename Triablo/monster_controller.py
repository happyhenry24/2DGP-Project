import random
import pico2d
import math
import time
import character_controller as cc

def load_skeleton_images():
    global skeleton_idle_sprites, skeleton_walk_sprites
    skeleton_idle_sprites = {
        direction: pico2d.load_image(
            f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/enemy/skeleton/skeleton_default_idle/{direction}/skeleton_default_idle_{direction}_{cc.direction_angle_mapping[direction]}_0.png')
        for direction in cc.direction_angle_mapping
    }
    skeleton_walk_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/enemy/skeleton/skeleton_default_walk/{direction}/skeleton_default_walk_{direction}_{cc.direction_angle_mapping[direction]}_{i}.png')
            for i in range(8)
        ]
        for direction in cc.direction_angle_mapping
    }

def load_slime_images():
    global slime_idle_sprites, slime_walk_sprites
    slime_idle_sprites = {
        direction: pico2d.load_image(
            f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/enemy/slime/slime_default_idle/{direction}/slime_default_idle_{direction}_{cc.direction_angle_mapping[direction]}_0.png')
        for direction in cc.direction_angle_mapping
    }
    slime_walk_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/enemy/slime/slime_default_walk/{direction}/slime_default_walk_{direction}_{cc.direction_angle_mapping[direction]}_{i}.png')
            for i in range(8)
        ]
        for direction in cc.direction_angle_mapping
    }

class Monster:
    def __init__(self, x, y, type):
        self.x, self.y = x, y
        self.direction = random.choice(list(cc.direction_angle_mapping.keys()))
        self.frame = 0
        self.speed = 2
        self.frame_delay = 0
        self.frame_speed = 5
        self.is_patrolling = True
        self.distance = 0
        self.max_distance = random.randint(50, 150)
        self.patrol_delay = 2
        self.timer = time.time()
        self.walk_sprites = skeleton_walk_sprites if type == 'skeleton' else slime_walk_sprites
        self.idle_sprites = skeleton_idle_sprites if type == 'skeleton' else slime_idle_sprites
        self.patrol_direction = 1
        self.type = type
        self.original_direction = self.direction
        self.is_idle = False

    def update(self):
        current_time = time.time()

        if self.is_idle:
            if current_time - self.timer > self.patrol_delay:
                self.is_idle = False
                self.distance = 0
                self.patrol_direction *= -1
                if self.patrol_direction == -1:
                    self.direction = self.get_opposite_direction(self.original_direction)
                else:
                    self.direction = self.original_direction
                self.timer = current_time
                self.frame = 0

        elif self.distance < self.max_distance:
            dx = math.cos(math.radians(float(cc.direction_angle_mapping[self.direction]))) * self.speed
            dy = math.sin(math.radians(float(cc.direction_angle_mapping[self.direction]))) * self.speed
            self.x += dx
            self.y += dy
            self.distance += self.speed

            self.frame_delay = (self.frame_delay + 1) % self.frame_speed
            if self.frame_delay == 0:
                self.frame = (self.frame + 1) % 8
        else:
            self.is_idle = True
            self.timer = current_time

    def get_opposite_direction(self, direction):
        opposite_map = {
            'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N',
            'NE': 'SW', 'SW': 'NE', 'NW': 'SE', 'SE': 'NW',
            'NNE': 'SSW', 'SSW': 'NNE', 'NEE': 'SWW', 'SWW': 'NEE',
            'NNW': 'SSE', 'SSE': 'NNW', 'NWW': 'SEE', 'SEE': 'NWW'
        }
        return opposite_map.get(direction, 'E')

    def draw(self, camera_x, camera_y):
        if self.is_patrolling:
            if self.is_idle:
                self.idle_sprites[self.direction].draw(self.x - camera_x, self.y - camera_y)
            else:
                self.walk_sprites[self.direction][self.frame].draw(self.x - camera_x, self.y - camera_y)

monster_positions = [
    (3400, 3400),
    (3500, 3500),
]

monsters = []

def generate_monsters(center_x, center_y):
    global monsters
    for _ in range(10):
        rand_x = random.randint(center_x - 200, center_x + 200)
        rand_y = random.randint(center_y - 200, center_y + 200)
        type = random.choice(['skeleton', 'slime'])
        monsters.append(Monster(rand_x, rand_y, type))

def draw_monsters(player_y, camera_x, camera_y):
    for monster in monsters:
        if monster.y > player_y:
            monster.draw(camera_x, camera_y)
    for monster in monsters:
        if monster.y <= player_y:
            monster.draw(camera_x, camera_y)

def update_monsters():
    for monster in monsters:
        monster.update()
