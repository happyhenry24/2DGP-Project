import pico2d

pico2d.open_canvas(800, 600)

background = pico2d.load_image('Lords Of Pain - Old School Isometric Assets/environment/ground_stone1.png')
character = pico2d.load_image('Lords Of Pain - Old School Isometric Assets/playable character/knight/knight_armed_idle/S/knight_armed_idle_S_270.0_0.png')

def draw():
    pico2d.clear_canvas()
    background.draw(400, 300)
    character.draw(400, 300)
    pico2d.update_canvas()

running = True
while running:
    events = pico2d.get_events()
    for event in events:
        if event.type == pico2d.SDL_QUIT or (event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE):
            running = False
    draw()
    pico2d.delay(0.01)

pico2d.close_canvas()
