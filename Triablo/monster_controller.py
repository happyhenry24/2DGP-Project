import pico2d
import random
import math
import time
import hud

from skills import FireArrow
from ASpike_Fiend import get_spike_fiend_data, get_hell_bovine_data

direction_order_8 = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']
direction_angle_mapping_8 = {
    'S': (247.5, 292.5), 'SW': (225.0, 247.5), 'W': (157.5, 202.5), 'NW': (112.5, 157.5),
    'N': (67.5, 112.5), 'NE': (22.5, 67.5), 'E': (337.5, 22.5), 'SE': (292.5, 337.5)
}

def load_monster_images(monster_data):
    sprites = {}
    image_paths = monster_data["image_paths"]
    frame_counts = monster_data["frame_counts"]

    for action, path in image_paths.items():
        sprites[action] = {
            direction: [
                pico2d.load_image(f'{path}tile{frame_idx:03}.png')
                for frame_idx in range(frame_counts[action] * idx, frame_counts[action] * (idx + 1))
            ]
            for idx, direction in enumerate(direction_order_8)
        }

    return sprites

class Monster:
    def __init__(self, x, y, monster_data):
        self.x, self.y = x, y
        self.spawn_x, self.spawn_y = x, y
        self.hp = monster_data["hp"]
        self.max_hp = monster_data["hp"]
        self.attack_damage = monster_data["attack_damage"]
        self.chase_distance = monster_data["chase_distance"]
        self.attack_distance = monster_data["attack_distance"]
        self.sprites = load_monster_images(monster_data)
        self.direction = random.choice(direction_order_8)
        self.frame = 0
        self.walk_frame_delay = 0
        self.walk_frame_speed = 5
        self.speed = 2
        self.distance = 0
        self.patrol_distance = random.randint(50, 200)
        self.patrol_delay = random.uniform(2, 5)
        self.timer = time.time()
        self.is_idle = False
        self.returning_to_spawn = False
        self.is_hit = False
        self.hit_frame = 0
        self.is_attacking = False
        self.attack_frame = 0
        self.has_entered_range = False
        self.chasing_on_attack = False
        self.is_dead = False
        self.death_frame = 0
        self.last_damage_time = 0
        self.hp_bar = hud.MonsterHPBar(self)

    def start_attack(self, player_x, player_y):
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_frame = 0
            self.has_dealt_damage = False
            dx, dy = player_x - self.x, player_y - self.y
            angle = math.degrees(math.atan2(dy, dx)) % 360
            self.direction = self.get_direction_by_angle(angle)

    def receive_damage(self, damage):
        if not self.is_dead:
            self.hp -= damage
            if self.hp <= 0:
                self.hp = 0
                self.is_dead = True
                self.death_frame = 0
            else:
                self.is_hit = True
                self.hit_frame = 0
                self.chasing_on_attack = True
            self.hp_bar.update_hp(self.hp)

    def update(self, player_x, player_y, character, loot_indicators):
        if self.is_dead:
            self.death_frame += 0.2
            if self.death_frame >= len(self.sprites['death'][self.direction]):
                self.drop_loot(character, loot_indicators)
                monsters.remove(self)
            return

        if self.is_hit:
            if self.hit_frame >= len(self.sprites['hit'][self.direction]):
                self.is_hit = False
                self.hit_frame = 0
            else:
                self.hit_frame += 0.2
            return

        distance_to_player = math.sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)

        if distance_to_player <= self.attack_distance:
            self.start_attack(player_x, player_y)
            if self.is_attacking:
                if not self.has_dealt_damage:
                    character.take_damage(self.attack_damage)
                    self.has_dealt_damage = True
                self.attack_frame += 0.2
        elif distance_to_player <= self.chase_distance:
            self.has_entered_range = True
            self.chase_player(player_x, player_y)
        elif self.chasing_on_attack:
            if self.has_entered_range and distance_to_player > self.chase_distance:
                self.chasing_on_attack = False
                self.returning_to_spawn = True
            else:
                self.chase_player(player_x, player_y)
        elif self.returning_to_spawn:
            self.move_to_spawn()
        else:
            self.patrol()

    def drop_loot(self, character, loot_indicators):
        if not self.is_dead:
            return
        missing_potions = [
            potion for potion in ["HP_Potion_Small", "HP_Potion_Big", "Mana_Potion_Small", "Mana_Potion_Big"]
            if character.potions.get(potion, 0) == 0
        ]
        if missing_potions and random.random() < 0.1:
            loot_indicator = {
                'image': pico2d.load_image(
                    'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/user interface/loot-indicator/loot_indicator_yellow.png'),
                'x': self.x,
                'y': self.y
            }
            loot_indicators.append(loot_indicator)

    def patrol(self):
        if not self.is_idle:
            dx = math.cos(math.radians(direction_angle_mapping_8[self.direction][0])) * self.speed
            dy = math.sin(math.radians(direction_angle_mapping_8[self.direction][0])) * self.speed
            self.x += dx
            self.y += dy
            self.distance += self.speed
            self.update_frame()

            if self.distance >= self.patrol_distance:
                self.is_idle = True
                self.timer = time.time()
                self.patrol_delay = random.uniform(2, 5)
        else:
            if time.time() - self.timer > self.patrol_delay:
                self.is_idle = False
                self.distance = 0
                self.direction = self.get_opposite_direction(self.direction)

    def chase_player(self, player_x, player_y):
        self.is_attacking = False
        self.returning_to_spawn = False
        self.is_idle = False
        dx, dy = player_x - self.x, player_y - self.y
        angle = math.degrees(math.atan2(dy, dx)) % 360
        self.direction = self.get_direction_by_angle(angle)
        distance = math.sqrt(dx ** 2 + dy ** 2)
        self.x += (dx / distance) * self.speed
        self.y += (dy / distance) * self.speed
        self.update_frame()

    def move_to_spawn(self):
        dx, dy = self.spawn_x - self.x, self.spawn_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < self.speed:
            self.x, self.y = self.spawn_x, self.spawn_y
            self.returning_to_spawn = False
            self.direction = random.choice(direction_order_8)
            self.patrol_distance = random.randint(50, 200)
            self.patrol_delay = random.uniform(2, 5)
            self.is_idle = False
            self.distance = 0
            self.has_entered_range = False
        else:
            angle = math.degrees(math.atan2(dy, dx)) % 360
            self.direction = self.get_direction_by_angle(angle)
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            self.update_frame()

    def get_direction_by_angle(self, angle):
        for direction, (min_angle, max_angle) in direction_angle_mapping_8.items():
            if min_angle <= angle < max_angle or (min_angle > max_angle and (angle >= min_angle or angle < max_angle)):
                return direction
        return 'S'

    def get_opposite_direction(self, direction):
        opposite_map = {
            'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N',
            'NE': 'SW', 'SW': 'NE', 'NW': 'SE', 'SE': 'NW'
        }
        return opposite_map.get(direction, 'E')

    def update_frame(self):
        max_frames = len(self.sprites['walk'][self.direction]) if not self.is_idle else len(
            self.sprites['idle'][self.direction])
        self.walk_frame_delay += 1
        if self.walk_frame_delay >= self.walk_frame_speed:
            self.frame = (self.frame + 1) % max_frames
            self.walk_frame_delay = 0

    def draw(self, camera_x, camera_y):
        if self.is_dead:
            death_index = min(int(self.death_frame), len(self.sprites['death'][self.direction]) - 1)
            self.sprites['death'][self.direction][death_index].draw(self.x - camera_x, self.y - camera_y)
        elif self.is_hit:
            hit_index = min(int(self.hit_frame), len(self.sprites['hit'][self.direction]) - 1)
            self.sprites['hit'][self.direction][hit_index].draw(self.x - camera_x, self.y - camera_y)
        elif self.is_attacking:
            attack_index = min(int(self.attack_frame), len(self.sprites['attack'][self.direction]) - 1)
            self.sprites['attack'][self.direction][attack_index].draw(self.x - camera_x, self.y - camera_y)
            self.attack_frame += 0.2
            if self.attack_frame >= len(self.sprites['attack'][self.direction]):
                self.is_attacking = False
                self.attack_frame = 0
        else:
            sprite_list = self.sprites['walk'] if not self.is_idle else self.sprites['idle']
            frames = sprite_list[self.direction]
            if 0 <= self.frame < len(frames):
                frames[self.frame].draw(self.x - camera_x, self.y - camera_y)
            else:
                self.frame = 0

        self.hp_bar.draw(camera_x, camera_y)


def monster_hit(monster, damage):
    monster.receive_damage(damage)

monsters = []

def generate_monsters():
    global monsters

    monster_data_list = [get_spike_fiend_data(), get_hell_bovine_data()]

    for monster_data in monster_data_list:
        spawn_center_x = monster_data["spawn_center_x"]
        spawn_center_y = monster_data["spawn_center_y"]

        for _ in range(10 if monster_data["name"] == "Spike Fiend" else 5):
            rand_x = random.randint(spawn_center_x - 200, spawn_center_x + 200)
            rand_y = random.randint(spawn_center_y - 200, spawn_center_y + 200)
            monsters.append(Monster(rand_x, rand_y, monster_data))

def draw_monsters(player_y, camera_x, camera_y):
    for monster in monsters:
        if monster.y > player_y:
            monster.draw(camera_x, camera_y)
    for monster in monsters:
        if monster.y <= player_y:
            monster.draw(camera_x, camera_y)

def update_monsters(player_x, player_y, character, loot_indicators):
    for monster in monsters[:]:
        monster.update(player_x, player_y, character, loot_indicators)
    check_arrow_collision(character.arrows)

def check_arrow_collision(arrows):
    for arrow in arrows:
        for monster in monsters:
            if math.sqrt((monster.x - arrow.x) ** 2 + (monster.y - arrow.y) ** 2) <= 30:
                if isinstance(arrow, FireArrow):
                    if not hasattr(monster, "last_fire_arrow_damage_time") or time.time() - monster.last_fire_arrow_damage_time >= 0.5:
                        monster.receive_damage(arrow.damage)
                        monster.last_fire_arrow_damage_time = time.time()
                else:
                    monster.receive_damage(arrow.damage)
                    arrow.is_active = False
                break
