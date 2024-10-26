import pico2d
import random
import math
import time
import character_controller as cc  # 캐릭터는 16방향, 몬스터는 8방향 사용

# 기본 애니메이션 스프라이트 저장 변수
spike_fiend_idle_sprites = {}
spike_fiend_walk_sprites = {}
spike_fiend_hit_sprites = {}

# 몬스터는 8방향을 사용합니다.
direction_order_8 = ['S', 'SW', 'W', 'NW', 'N', 'NE', 'E', 'SE']
direction_angle_mapping_8 = {
    'S': 270.0, 'SW': 225.0, 'W': 180.0, 'NW': 135.0, 'N': 90.0,
    'NE': 45.0, 'E': 0.0, 'SE': 315.0
}

def load_spike_fiend_images():
    global spike_fiend_idle_sprites, spike_fiend_walk_sprites, spike_fiend_hit_sprites

    # Idle 스프라이트 로딩 (8방향 * 8프레임)
    spike_fiend_idle_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_ASpike_Fiend_Idle/tile{frame_idx:03}.png')
            for frame_idx in range(8 * idx, 8 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_order_8)
    }

    # Walk 스프라이트 로딩 (8방향 * 9프레임)
    spike_fiend_walk_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_ASpike_Fiend_Walk/tile{frame_idx:03}.png')
            for frame_idx in range(9 * idx, 9 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_order_8)
    }

    # 맞는 애니메이션 스프라이트 로딩 (8방향 * 6프레임)
    spike_fiend_hit_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_ASpike_Fiend_Get_hit/tile{frame:03}.png')
            for frame in range(6 * idx, 6 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_order_8)
    }

class Monster:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.spawn_x, self.spawn_y = x, y
        self.direction = random.choice(direction_order_8)
        self.frame = 0
        self.speed = 2
        self.distance = 0
        self.patrol_distance = random.randint(50, 200)
        self.patrol_delay = random.uniform(2, 5)
        self.timer = time.time()
        self.walk_sprites = spike_fiend_walk_sprites
        self.idle_sprites = spike_fiend_idle_sprites
        self.hit_sprites = spike_fiend_hit_sprites
        self.is_idle = False
        self.returning_to_spawn = False
        self.chase_distance = 200
        self.is_hit = False
        self.hit_frame = 0
        self.hit_animation_done = False
        self.has_entered_range = False  # 추적 범위에 들어온 적이 있는지 확인
        self.chasing_on_attack = False  # 공격을 받아 추적 상태인지 여부를 관리

    def update(self, player_x, player_y):
        if self.is_hit:
            if self.hit_frame >= len(self.hit_sprites[self.direction]):
                self.is_hit = False
                self.hit_animation_done = True
                self.hit_frame = 0
            else:
                self.hit_frame += 0.2
            return

        distance_to_player = math.sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)

        if distance_to_player <= self.chase_distance:
            # 범위 안에 플레이어가 들어오면 추적 시작
            self.has_entered_range = True
            self.chase_player(player_x, player_y)
        elif self.chasing_on_attack:
            # 공격받아 추적 중인데, 추적 범위에 한번이라도 들어왔고 현재는 나가있을 경우 패트롤로 돌아감
            if self.has_entered_range and distance_to_player > self.chase_distance:
                self.chasing_on_attack = False
                self.returning_to_spawn = True
            else:
                self.chase_player(player_x, player_y)
        elif self.returning_to_spawn:
            # 반환 중
            self.move_to_spawn()
        else:
            # 패트롤 상태
            self.patrol()

    def patrol(self):
        current_time = time.time()
        if not self.is_idle:
            dx = math.cos(math.radians(direction_angle_mapping_8[self.direction])) * self.speed
            dy = math.sin(math.radians(direction_angle_mapping_8[self.direction])) * self.speed
            self.x += dx
            self.y += dy
            self.distance += self.speed
            self.update_frame()

            if self.distance >= self.patrol_distance:
                self.is_idle = True
                self.timer = current_time
                self.patrol_delay = random.uniform(2, 5)
        else:
            if current_time - self.timer > self.patrol_delay:
                self.is_idle = False
                self.distance = 0
                self.direction = self.get_opposite_direction(self.direction)

    def chase_player(self, player_x, player_y):
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
            self.has_entered_range = False  # 패트롤 복귀 시 범위 기록 초기화
        else:
            angle = math.degrees(math.atan2(dy, dx)) % 360
            self.direction = self.get_direction_by_angle(angle)
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            self.update_frame()

    def get_direction_by_angle(self, angle):
        for direction, dir_angle in direction_angle_mapping_8.items():
            if abs(angle - dir_angle) < 22.5 or abs(angle - dir_angle) > 337.5:
                return direction
        return 'S'

    def get_opposite_direction(self, direction):
        opposite_map = {
            'E': 'W', 'W': 'E', 'N': 'S', 'S': 'N',
            'NE': 'SW', 'SW': 'NE', 'NW': 'SE', 'SE': 'NW'
        }
        return opposite_map.get(direction, 'E')

    def update_frame(self):
        max_frames = len(self.walk_sprites[self.direction]) if not self.is_idle else len(self.idle_sprites[self.direction])
        self.frame = (self.frame + 1) % max_frames

    def draw(self, camera_x, camera_y):
        if self.is_hit and not self.hit_animation_done:
            frames = self.hit_sprites[self.direction]
            hit_index = min(int(self.hit_frame), len(frames) - 1)
            frames[hit_index].draw(self.x - camera_x, self.y - camera_y)
        else:
            sprite_list = self.walk_sprites if not self.is_idle else self.idle_sprites
            if self.direction in sprite_list:
                frames = sprite_list[self.direction]
                if 0 <= self.frame < len(frames):
                    frames[self.frame].draw(self.x - camera_x, self.y - camera_y)
                else:
                    self.frame = 0

    def hit(self):
        self.is_hit = True
        self.hit_animation_done = False
        self.hit_frame = 0
        self.chasing_on_attack = True



monsters = []

def generate_monsters(center_x, center_y):
    global monsters
    for _ in range(10):
        rand_x = random.randint(center_x - 200, center_x + 200)
        rand_y = random.randint(center_y - 200, center_y + 200)
        monsters.append(Monster(rand_x, rand_y))

def draw_monsters(player_y, camera_x, camera_y):
    for monster in monsters:
        if monster.y > player_y:
            monster.draw(camera_x, camera_y)
    for monster in monsters:
        if monster.y <= player_y:
            monster.draw(camera_x, camera_y)

def update_monsters(player_x, player_y):
    for monster in monsters:
        monster.update(player_x, player_y)
