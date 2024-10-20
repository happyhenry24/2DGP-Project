import pico2d
import map_drawer
import character_controller as cc
import monster_controller as mc

pico2d.open_canvas(800, 600)

map_drawer.load_tiles()
mc.load_skeleton_images()
mc.load_slime_images()
mc.generate_monsters(3200, 3200)

walk_sprites = {
    direction: [
        pico2d.load_image(
            f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/playable character/knight/knight_armed_walk/{direction}/knight_armed_walk_{direction}_{cc.direction_angle_mapping[direction]}_{i}.png')
        for i in range(8)
    ]
    for direction in cc.direction_angle_mapping
}

idle_sprites = {
    direction: pico2d.load_image(
        f'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/playable character/knight/knight_armed_idle/{direction}/knight_armed_idle_{direction}_{cc.direction_angle_mapping[direction]}_0.png')
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

    mc.draw_monsters(character.y, camera.x, camera.y)
    character.draw(camera.x, camera.y, walk_sprites, idle_sprites)

    mc.update_monsters()

    pico2d.update_canvas()
    pico2d.delay(0.01)

pico2d.close_canvas()
