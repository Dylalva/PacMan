import pygame
from PACMAN.edible.edible import *
from PACMAN.Player.PacMan import *


class Power_pill(Edible):
    def __init__(self, position):
        super().__init__(50, position)
        self.radius = 6
        self.color = YELLOW

    def eat(self, pacman: PacMan):
        pacman.score += self.points
        pacman.set_mode(MODE_INVINCIBLE)
        Sound_Manager().eat_special_item()

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)
        pygame.draw.circle(screen, WHITE, self.position, self.radius//2)

    def save_state(self):
        return {
            'type': self.type(),
            'position': self.position,
            'color': self.color,
            'radius': self.radius,
            'points': self.points
        }

    def type(self):
        return 'PowerPill'

    def load_state(self, state):

        self.position = state['position']
        self.color = state['color']
        self.radius = state['radius']
        self.points = state['points']