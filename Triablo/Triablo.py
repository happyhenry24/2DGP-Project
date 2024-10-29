import pico2d
import map_drawer
import character_controller as cc
import monster_controller as mc
import hud

pico2d.open_canvas(800, 600)

map_drawer.load_tiles()

cc.load_character_sprites()
mc.load_spike_fiend_images()

class Camera:
    def __init__(self, width, height):
        self.x, self.y = 0, 0
        self.width, self.height = width, height

    def update(self, target_x, target_y):
        self.x = target_x - self.width // 2
        self.y = target_y - self.height // 2

character = cc.Character()
camera = Camera(800, 600)

mc.generate_monsters(3600, 3600)

game_hud = hud.create_hud(800, 600)

running = True
while running:
    running = cc.handle_character_events(character, camera, mc.monsters)
    character.update()
    mc.update_monsters(character.x, character.y, character)
    camera.update(character.x, character.y)

    pico2d.clear_canvas()
    map_drawer.draw_map(camera.x, camera.y)

    character.draw(camera.x, camera.y, cc.walk_sprites, cc.idle_sprites, cc.attack_sprites)

    mc.draw_monsters(character.y, camera.x, camera.y)

    game_hud.draw()

    pico2d.update_canvas()
    pico2d.delay(0.01)

pico2d.close_canvas()
