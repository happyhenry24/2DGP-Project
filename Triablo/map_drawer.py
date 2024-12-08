import pico2d

class MapDrawer:
    def __init__(self):
        self.floor_image = pico2d.load_image('C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Map/Floor.png')
        self.front_image = pico2d.load_image('C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Map/Front.png')

    def draw(self, camera_x, camera_y):
        self.floor_image.draw(1500 - camera_x, 1000 - camera_y)
        self.front_image.draw(1500 - camera_x, 1000 - camera_y)
