import pico2d
import map_drawer
import character_controller as cc
import monster_controller as mc

pico2d.open_canvas(800, 600)

# 지도 타일 로드
map_drawer.load_tiles()

# 스프라이트 로드
cc.load_character_sprites()
mc.load_spike_fiend_images()


# 카메라 클래스 정의
class Camera:
    def __init__(self, width, height):
        self.x, self.y = 0, 0
        self.width, self.height = width, height

    def update(self, target_x, target_y):
        self.x = target_x - self.width // 2
        self.y = target_y - self.height // 2


# 캐릭터와 카메라 생성
character = cc.Character()
camera = Camera(800, 600)

# 몬스터 생성
mc.generate_monsters(3600, 3600)

running = True
while running:
    # 이벤트 처리
    running = cc.handle_character_events(character, camera, mc.monsters)
    character.update()
    mc.update_monsters(character.x, character.y)
    camera.update(character.x, character.y)

    pico2d.clear_canvas()
    map_drawer.draw_map(camera.x, camera.y)

    # 캐릭터 그리기
    character.draw(camera.x, camera.y, cc.walk_sprites, cc.idle_sprites, cc.attack_sprites)

    # 몬스터 그리기
    mc.draw_monsters(character.y, camera.x, camera.y)

    pico2d.update_canvas()
    pico2d.delay(0.01)

pico2d.close_canvas()
