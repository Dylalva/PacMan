#Librerias/modulos utilizados
import pygame.draw
from PACMAN.Interface.Map import Node, Graph
from PACMAN.Interface.constants import *
from PACMAN.Enemy.Ghost import Ghost, MODE_CHASE, MODE_FRIGHTENED
import PACMAN.Utils.AlgorithmicSearch as AlgorithmicSearch
#=================================================================
IMAGE_IDLE = "../../../resource/Ghost/Blinky.png"
IMAGE_DOWN = "../../../resource/Ghost/BlinkyDown.png"
IMAGE_UP = "../../../resource/Ghost/BlinkyUp.png"
IMAGE_RIGHT = "../../../resource/Ghost/BlinkyRight.png"
IMAGE_LEFT = "../../../resource/Ghost/BlinkyLeft.png"

class Blinky(Ghost):
    def __init__(self, home_corner: Node, scatter_corner: Node, graph: Graph, target):
        super().__init__(home_corner, scatter_corner, graph, target)
        self.target_position = None
        self.load_image()

    # Metodo de persecución
    def chase(self):
        self.target_position = self.calculate_next_position()  # Obtener la posicion de Pac-Man
        self.follow_target(self.target_position)  # Seguir el camino hacia Pac-Man

    def create_path(self, pos):
        dic, _ = AlgorithmicSearch.a_star_search(self.position, pos)
        if not dic:  # Si no hay camino, salir
            return

        current = pos
        start = self.position
        self.path = []  # Reinicia la ruta para evitar residuos de rutas previas

        while current != start:
            if current in dic:
                self.path.append(current)  # Añade cada nodo a la ruta
                current = dic[current]  # Retrocede a través del diccionario
            else:
                break  # Romper si el camino no se puede construir
        self.path.reverse()  # Invertir la lista para obtener la ruta desde el inicio hasta el objetivo

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
        return self.target.get_next_position()

    def save_state(self):
        state = super().save_state()
        state.update({
           'type': self.type()
        })
        return state

    def type(self):
        return 'Blinky'

    def load_state(self, state, maze, pacman):
        super().load_state(state, maze, pacman)


    def save_q_table(self, level):
        return