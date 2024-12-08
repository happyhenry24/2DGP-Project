import pico2d

class MapDrawer:
    def __init__(self):
        self.floor_image = pico2d.load_image(
            'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Map/Floor.png')
        self.front_image = pico2d.load_image(
            'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/Othersprite/Map/Front.png')

        self.collision_points = self.load_collision_points(
            'C:/Users/Creator/Documents/2DGP/2DGP-Project/Triablo/collider_coordinates.txt'
        )

    def load_collision_points(self, file_path):
        points = set()
        with open(file_path, "r") as f:
            for line in f:
                x, y = map(int, line.strip().split(","))
                points.add((x, y))
        return points

    def is_collision(self, x, y):
        return (int(x), int(y)) in self.collision_points

    def draw(self, camera_x, camera_y):
        self.floor_image.draw(1500 - camera_x, 1000 - camera_y)
        self.front_image.draw(1500 - camera_x, 1000 - camera_y)
