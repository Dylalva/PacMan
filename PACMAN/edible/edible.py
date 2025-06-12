class Edible:
    def __init__(self, points, position):
        self.points = points
        self.position = position

    def eat(self, pacman):
        pass

    def draw(self, screen):
        pass

    def get_points(self):
        return self.points

    def save_state(self):
       pass

    def load_state(self, state):
        pass

    def type(self):
       pass