import pico2d
import math
import time

# 각 방향에 해당하는 각도 매핑
direction_angle_mapping = {
    'S': (247.5, 292.5), 'SSW': (225.0, 247.5), 'SW': (202.5, 225.0), 'SWW': (180.0, 202.5),
    'W': (157.5, 180.0), 'NWW': (135.0, 157.5), 'NW': (112.5, 135.0), 'NNW': (90.0, 112.5),
    'N': (67.5, 90.0), 'NNE': (45.0, 67.5), 'NE': (22.5, 45.0), 'NEE': (0.0, 22.5),
    'E': (337.5, 360.0), 'SEE': (315.0, 337.5), 'SE': (292.5, 315.0), 'SSE': (270.0, 292.5)
}

# 스프라이트 로딩용 함수 추가
walk_sprites = {}
idle_sprites = {}
attack_sprites = {}

def load_character_sprites():
    global walk_sprites, idle_sprites, attack_sprites

    # walk_sprites 로드 (16방향 8프레임)
    walk_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Walk/tile{frame_idx:03}.png')
            for frame_idx in range(8 * idx, 8 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping)
    }

    # idle_sprites 로드 (16방향 8프레임)
    idle_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Idle/tile{frame_idx:03}.png')
            for frame_idx in range(8 * idx, 8 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping)
    }

    # attack_sprites 로드 (16방향 14프레임)
    attack_sprites = {
        direction: [
            pico2d.load_image(
                f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/PC_Computer_Diablo2_Amazon_Light_Attack/tile{frame_idx:03}.png')
            for frame_idx in range(14 * idx, 14 * (idx + 1))
        ]
        for idx, direction in enumerate(direction_angle_mapping)
    }

class Character:
    def __init__(self):
        self.x, self.y = 3200, 3200
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
        self.is_attacking = False  # 공격 중인지 확인하는 변수
        self.attack_frame = 0
        self.attack_frame_speed = 1.0
        self.attack_cooldown = False  # 연타 방지용 변수

        self.highlight = pico2d.load_image(
            'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/user interface/highlight/highlight_yellow.png')

    def update(self):
        if self.is_attacking:
            # 공격 애니메이션 프레임을 느리게 증가
            self.attack_frame += self.attack_frame_speed
            if self.attack_frame >= 14:
                self.is_attacking = False
                self.attack_cooldown = False
                self.attack_frame = 0  # 공격 프레임 초기화
        elif self.is_moving:
            # 이동 중일 때 처리
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
            # 정지 상태에서도 Idle 애니메이션 재생
            self.frame_delay = (self.frame_delay + 1) % self.frame_speed
            if self.frame_delay == 0:
                self.frame = (self.frame + 1) % 8

    def draw(self, camera_x, camera_y, walk_sprites, idle_sprites, attack_sprites):
        self.highlight.draw(self.x - camera_x, self.y - camera_y)

        if self.is_attacking:
            # 공격 중일 때 공격 애니메이션 재생 (인덱스를 정수로 변환)
            attack_sprites[self.direction][int(self.attack_frame)].draw(self.x - camera_x, self.y - camera_y)
        elif self.is_moving:
            walk_sprites[self.direction][self.frame].draw(self.x - camera_x, self.y - camera_y)
        else:
            idle_sprites[self.direction][self.frame].draw(self.x - camera_x, self.y - camera_y)

    def move_to(self, x, y):
        if not self.is_attacking:  # 공격 중에는 이동하지 않도록
            self.target_x, self.target_y = x, y
            self.is_moving = True
            self.direction = self.calculate_direction(x, y)

    def attack(self, target_x, target_y):
        if not self.attack_cooldown:  # 공격 쿨다운 중이 아니면 공격 시작
            self.is_attacking = True
            self.attack_cooldown = True  # 연타 방지용 쿨다운 설정
            self.is_moving = False  # 공격 중에는 이동하지 않음
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

# 수정된 handle_character_events 함수
def handle_character_events(character, camera, monsters):
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
            mouse_x, mouse_y = event.x + camera.x, 600 - event.y + camera.y

            if elapsed_time < 0.2:
                # 몬스터에 대해 반경 50 내 클릭 시 맞는 애니메이션 재생
                for monster in monsters:
                    distance = math.sqrt((monster.x - mouse_x) ** 2 + (monster.y - mouse_y) ** 2)
                    if distance <= 50:
                        monster.hit()
                        break  # 한 번에 하나의 몬스터만 히트 처리
                # 캐릭터가 공격 상태가 아닌 경우에만 공격 수행
                if not character.is_attacking:
                    character.attack(mouse_x, mouse_y)
            else:
                character.stop()
        elif character.mouse_held and time.time() - character.mouse_down_time >= 0.2:
            character.is_following_mouse = True
            character.move_to(event.x + camera.x, 600 - event.y + camera.y)
    return True
