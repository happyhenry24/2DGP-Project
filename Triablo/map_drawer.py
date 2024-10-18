import pico2d

def load_tiles():
    global ground_stone1, tiles_NE, tiles_NW, tiles_SE, tiles_SW
    ground_stone1 = pico2d.load_image(
        'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/environment/ground_stone1.png')
    tiles_NE = pico2d.load_image(
        'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/prop/tiles/NE/tiles_NE_45.0_0.png')
    tiles_NW = pico2d.load_image(
        'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/prop/tiles/NW/tiles_NW_135.0_0.png')
    tiles_SE = pico2d.load_image(
        'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/prop/tiles/SE/tiles_SE_315.0_0.png')
    tiles_SW = pico2d.load_image(
        'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Lords Of Pain - Old School Isometric Assets/prop/tiles/SW/tiles_SW_225.0_0.png')

tile_gap_x = 87
tile_gap_y = 61

tiles_NE_positions = [
    (3200 + tile_gap_x, 3200),
]

tiles_NW_positions = [
    (3200, 3200 - tile_gap_y),
]

tiles_SE_positions = [
    (3200, 3200 + tile_gap_y),
]

tiles_SW_positions = [
    (3200 - tile_gap_x, 3200)
]

def draw_map(camera_x, camera_y):
    for x, y in generate_tile_positions(256, 25, 25):
        ground_stone1.draw(x - camera_x, y - camera_y)

    for x, y in tiles_NE_positions:
        tiles_NE.draw(x - camera_x, y - camera_y)

    for x, y in tiles_NW_positions:
        tiles_NW.draw(x - camera_x, y - camera_y)

    for x, y in tiles_SE_positions:
        tiles_SE.draw(x - camera_x, y - camera_y)

    for x, y in tiles_SW_positions:
        tiles_SW.draw(x - camera_x, y - camera_y)

def generate_tile_positions(tile_size, grid_width, grid_height):
    positions = []
    for row in range(grid_height):
        for col in range(grid_width):
            x = col * tile_size
            y = row * tile_size
            positions.append((x, y))
    return positions
