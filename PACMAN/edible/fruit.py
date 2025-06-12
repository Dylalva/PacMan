import pygame
from PACMAN.edible.edible import *
from PACMAN.Interface.GameController.sound_manager import *

CHERRY_PATH = "../../../resource/pacman/images1/cerezas.png"
SIZE = (32, 32)
TIME = 10


class Fruit(Edible):
    def __init__(self, position, points):
        super().__init__(points, position)
        self.image = pygame.transform.scale(pygame.image.load(CHERRY_PATH), SIZE)
        self.time = 10  # tiempo que durara la fruta

    def eat(self, pacman):
        pacman.score += self.points
        Sound_Manager().eat_special_item()

    def draw(self, screen):
        pos = (self.position[0]-10, self.position[1]-10)
        screen.blit(self.image, pos)

    def update(self):
        self.time -= 0.01

    def get_time(self):
        return self.time

    def type(self):
        return 'Fruit'

    def save_state(self):
        return {
            'type': self.type(),
            'position': self.position,
            'time': self.time,
            'points': self.points
        }


    def load_state(self, state):
        self.position = state['position']
        self.time = state['time']
        self.points = state['points']