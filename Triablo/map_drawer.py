import pico2d

def load_tiles():
    global ground_stone1
    ground_stone1 = pico2d.load_image('C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/environment/ground_stone1.png')

def draw_map(camera_x, camera_y, screen_width, screen_height):
    extra_space = 256
    tile_size = 256
    for x in range(int(-camera_x) % tile_size - extra_space, screen_width + tile_size + extra_space, tile_size):
        for y in range(int(-camera_y) % tile_size - extra_space, screen_height + tile_size + extra_space, tile_size):
            ground_stone1.draw(x - int(camera_x % tile_size), y - int(camera_y % tile_size))
