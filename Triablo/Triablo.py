import pico2d
import map_drawer
import character_controller as cc
import monster_controller as mc
import hud
import skills

pico2d.open_canvas(800, 600)

map_drawer.load_tiles()
cc.load_character_sprites()
mc.load_spike_fiend_images()

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
mc.generate_monsters(3600, 3600)

game_hud = hud.HUD(800, 600)

explosions = []

running = True
while running:
    events = pico2d.get_events()

    mouse_events = [e for e in events if
                    e.type in (pico2d.SDL_MOUSEBUTTONDOWN, pico2d.SDL_MOUSEBUTTONUP, pico2d.SDL_MOUSEMOTION)]
    keyboard_events = [e for e in events if e.type in (pico2d.SDL_KEYDOWN, pico2d.SDL_KEYUP)]

    for event in keyboard_events:
        character.handle_event(event, camera, game_hud)

    for event in mouse_events:
        character.handle_event(event, camera, game_hud)

    skills_manager.handle_input(keyboard_events)

    for event in events:
        if event.type == pico2d.SDL_QUIT:
            running = False
        elif event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            running = False

    if not character.is_dead:
        character.update(camera.x, camera.y, explosions)

    mc.update_monsters(character.x, character.y, character)
    skills.update_fire_paths(800, 600, camera.x, camera.y, mc.monsters)

    for explosion in explosions:
        explosion.update(mc.monsters)

    explosions = [e for e in explosions if e.active]

    camera.update(character.x, character.y)

    pico2d.clear_canvas()
    map_drawer.draw_map(camera.x, camera.y)
    skills.draw_fire_paths(camera.x, camera.y)
    mc.draw_monsters(character.y, camera.x, camera.y)

    for explosion in explosions:
        explosion.draw(camera.x, camera.y)

    if character.is_dead:
        character.draw_death_message()
    else:
        character.draw(camera.x, camera.y, cc.walk_sprites, cc.idle_sprites, cc.attack_sprites)

    game_hud.draw(character.hp, character.mana, skills_manager.get_current_mode())
    pico2d.update_canvas()
    pico2d.delay(0.01)

pico2d.close_canvas()
