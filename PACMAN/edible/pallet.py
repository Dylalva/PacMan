import pygame
from PACMAN.Interface.constants import *
from PACMAN.edible.edible import *
from PACMAN.Interface.GameController.sound_manager import *


class Pallet(Edible):
    def __init__(self, position):
        super().__init__(10, position)
        self.color = WHITE
        self.radius = 2

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def eat(self, pacman: PACMAN):
        pacman.score += self.points
        Sound_Manager().eat_pallet()

    def type(self):
        return 'Pallet'

    #Metodo para serizalizar un pallet
    def save_state(self):
        return {
            'type': self.type(),
            'position': self.position,
            'color': self.color,
            'radius': self.radius,
            'points': self.points
        }

    #Metodo para desserealizar un pallet
    def load_state(self, state):
        self.position = state['position']
        self.color = state['color']
        self.radius = state['radius']
        self.points = state['points']