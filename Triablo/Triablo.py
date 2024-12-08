import pico2d
import character_controller as cc
import monster_controller as mc
import hud
import skills
from map_drawer import MapDrawer

pico2d.open_canvas(800, 600)
pico2d.hide_cursor()

map_drawer = MapDrawer()
cc.load_character_sprites()

skills_manager = skills.SkillsManager()

class Camera:
    def __init__(self, width, height):
        self.x, self.y = 0, 0
        self.width, self.height = width, height

    def update(self, target_x, target_y):
        self.x = target_x - self.width // 2
        self.y = target_y - self.height // 2

character = cc.Character()
character.skills_manager = skills_manager

camera = Camera(800, 600)
mc.generate_monsters()

game_hud = hud.HUD(800, 600)

explosions = []
loot_indicators = []

running = True
while running:
    events = pico2d.get_events()

    mouse_events = [e for e in events if
                    e.type in (pico2d.SDL_MOUSEBUTTONDOWN, pico2d.SDL_MOUSEBUTTONUP, pico2d.SDL_MOUSEMOTION)]
    keyboard_events = [e for e in events if e.type in (pico2d.SDL_KEYDOWN, pico2d.SDL_KEYUP)]

    for event in keyboard_events:
        character.handle_event(event, camera, game_hud)

    for event in mouse_events:
        if event.type == pico2d.SDL_MOUSEMOTION:
            game_hud.mouse_x, game_hud.mouse_y = event.x, event.y
        elif event.type == pico2d.SDL_MOUSEBUTTONDOWN:
            if event.button == pico2d.SDL_BUTTON_RIGHT:
                game_hud.set_cursor_state("blue")
            elif event.button == pico2d.SDL_BUTTON_LEFT:
                game_hud.set_cursor_state("red")
        elif event.type == pico2d.SDL_MOUSEBUTTONUP:
            if event.button in (pico2d.SDL_BUTTON_RIGHT, pico2d.SDL_BUTTON_LEFT):
                game_hud.set_cursor_state("white")

        character.handle_event(event, camera, game_hud)

    skills_manager.handle_input(keyboard_events)

    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            running = False

    if not character.is_dead:
        character.update(camera.x, camera.y, explosions)

    mc.update_monsters(character.x, character.y, character, loot_indicators)

    character.check_loot_collision(loot_indicators, game_hud)

    skills.update_fire_paths(800, 600, camera.x, camera.y, mc.monsters)

    for explosion in explosions:
        explosion.update(mc.monsters)

    explosions = [e for e in explosions if e.active]

    camera.update(character.x, character.y)

    pico2d.clear_canvas()
    map_drawer.floor_image.draw(1500 - camera.x, 1000 - camera.y)
    skills.draw_fire_paths(camera.x, camera.y)
    mc.draw_monsters(character.y, camera.x, camera.y)

    for loot in loot_indicators:
        loot['image'].draw(loot['x'] - camera.x, loot['y'] - camera.y)

    for explosion in explosions:
        explosion.draw(camera.x, camera.y)

    if character.is_dead:
        character.draw_death_message()
    else:
        character.draw(camera.x, camera.y, cc.walk_sprites, cc.idle_sprites, cc.attack_sprites)

    map_drawer.front_image.draw(1500 - camera.x, 1000 - camera.y)
    game_hud.draw(character.hp, character.mana, skills_manager.get_current_mode())
    pico2d.update_canvas()
    pico2d.delay(0.01)

pico2d.close_canvas()
