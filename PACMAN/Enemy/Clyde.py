#Librerias/modulos utilizados
import pygame.draw
from numpy import random

from PACMAN.Interface.Map import Node, Graph
from PACMAN.Interface.constants import *
from PACMAN.Enemy.Ghost import Ghost, MODE_FRIGHTENED
import PACMAN.Utils.AlgorithmicSearch as AlgorithmicSearch

"""
Se comporta de manera errática, a veces persiguiendo a
Pacman y otras veces alejándose
"""
#================================================================================
IMAGE_IDLE = "../../../resource/Ghost/Clyde.png"
IMAGE_DOWN = "../../../resource/Ghost/ClydeDown.png"
IMAGE_UP = "../../../resource/Ghost/ClydeUp.png"
IMAGE_RIGHT = "../../../resource/Ghost/ClydeRight.png"
IMAGE_LEFT = "../../../resource/Ghost/ClydeLeft.png"
class Clyde(Ghost):
    def __init__(self, home_corner, scatter_corner, graph, target):
        super().__init__(home_corner, scatter_corner, graph, target)
        self.target_position = None
        self.load_image()

    # Metodo de persecución, se comporta de acuerdo al tipo de fantasma
    def chase(self):
        self.target_position = self.calculate_next_position()
        self.follow_target(self.target_position)  # Seguir el camino hacia Pac-Man

    def load_image(self):
        self.images = {
            LEFT: pygame.transform.scale(pygame.image.load(IMAGE_LEFT), G_SIZE),
            RIGHT: pygame.transform.scale(pygame.image.load(IMAGE_RIGHT), G_SIZE),
            UP: pygame.transform.scale(pygame.image.load(IMAGE_UP), G_SIZE),
            DOWN: pygame.transform.scale(pygame.image.load(IMAGE_DOWN), G_SIZE),
            STOP: pygame.transform.scale(pygame.image.load(IMAGE_IDLE), G_SIZE)
        }

    def draw(self, screen):
        position_coordinates = self.position_frame
        if not self.isAlive:
            screen.blit(self.image_eyes, (position_coordinates[0] - 17, position_coordinates[1] - 19))
        elif self.mode == MODE_FRIGHTENED:
            screen.blit(self.image_frightened, (position_coordinates[0] - 17, position_coordinates[1] - 19))
        else:
            screen.blit(self.images[self.direction], (position_coordinates[0] - 17, position_coordinates[1] - 19))

    def calculate_target(self):
        pacman_position: Node = self.target.get_next_position()
        nodes = self.graph.get_nodes()

        # Si pacman esta cerca de la esquina o si pacman esta muy cerca del fantasma
        if AlgorithmicSearch.heuristic(self.scatter_corner, pacman_position) < 255:
            return pacman_position

        # Si pacman no esta cerca de la esquina de Clyde no tiene un patron definido
        return random.choice(nodes)

    def save_state(self):
        state = super().save_state()
        state.update({
            'type': self.type()
        })
        return state

    def load_state(self, state, maze, pacman):
        super().load_state(state, maze, pacman)


    def type(self):
        return 'Clyde'

    def save_q_table(self, level):
        return