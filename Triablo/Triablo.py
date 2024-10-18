import pico2d
import map_drawer
import character_controller as cc

pico2d.open_canvas(800, 600)

map_drawer.load_tiles()

walk_sprites = {
    direction: [
        pico2d.load_image(f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/playable character/knight/knight_armed_walk/{direction}/knight_armed_walk_{direction}_{cc.direction_angle_mapping[direction]}_{i}.png')
        for i in range(8)
    ]
    for direction in cc.direction_angle_mapping
}

idle_sprites = {
    direction: pico2d.load_image(f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/playable character/knight/knight_armed_idle/{direction}/knight_armed_idle_{direction}_{cc.direction_angle_mapping[direction]}_0.png')
    for direction in cc.direction_angle_mapping
}

character = cc.Character()
camera = cc.Camera(800, 600)

running = True
while running:
    running = cc.handle_character_events(character, camera)
    character.update()
    camera.update(character.x, character.y)

    pico2d.clear_canvas()
    map_drawer.draw_map(camera.x, camera.y)
    character.draw(camera.x, camera.y, walk_sprites, idle_sprites)
    pico2d.update_canvas()
    pico2d.delay(0.01)

pico2d.close_canvas()
