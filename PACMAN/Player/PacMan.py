"""
Clase PacMan la cual seria con el objeto que el usuario jugara
"""
import time

import pygame.draw

from PACMAN.Interface.Map.Node import Node
from PACMAN.Interface.constants import *
from PACMAN.Interface.GameController.sound_manager import *

# Modos que puede tener Pac-Man
MODE_INVINCIBLE = "INVINCIBLE"  # Para cuando coma una pildora de poder(comer fantasmas)
MODE_VULNERABLE = "VULNERABLE"  # Para cuando no tenga poderes (Los fantasmas lo pueden comer)
# ================================================================================================


#  imagenes de la animacion del pac-man
IMAGE_0_r = "../../../resource/pacman/images1/pac-man-0-right.png"
IMAGE_1_r = "../../../resource/pacman/images1/pac-man-1-right.png"
IMAGE_0_l = "../../../resource/pacman/images1/pac-man-0-left.png"
IMAGE_1_l = "../../../resource/pacman/images1/pac-man-1-left.png"
IMAGE_0_u = "../../../resource/pacman/images1/pac-man-0-up.png"
IMAGE_1_u = "../../../resource/pacman/images1/pac-man-1-up.png"
IMAGE_0_d = "../../../resource/pacman/images1/pac-man-0-down.png"
IMAGE_1_d = "../../../resource/pacman/images1/pac-man-1-down.png"
HEART_PATH = "../../../resource/pacman/images1/heart.png"
size = (32, 32)


class PacMan:
    def __init__(self, home_scorner, graph):
        self.home_scorner = home_scorner  # Nodo de origen donde spawnea Pac-Man
        self.position = home_scorner.coordinate  # Su posicion inicial es el origen
        self.current_node = home_scorner
        self.target = home_scorner
        self.score = 0  # Puntuacion
        self.life = 3  # Vidas, por defecto 3
        self.mode = MODE_VULNERABLE  # El modo que se encuentra Pac-Man
        self.direction = STOP
        self.next_direction = STOP
        self.heart_image = None
        self.power_time = 0
        self.invincible_time = 7
        self.movement = {
            STOP: (0, 0),
            LEFT: (-1, 0),
            RIGHT: (1, 0),
            DOWN: (0, 1),
            UP: (0, -1)
        }
        self.images = {}
        self.observers = []
        self.frame = 0
        self.load_images()
        self.kill = 1

    def load_images(self):
        self.images = {
            LEFT: {
                0: pygame.transform.scale(pygame.image.load(IMAGE_0_l), C_SIZE),
                1: pygame.transform.scale(pygame.image.load(IMAGE_1_l), C_SIZE)
            },
            RIGHT: {
                0: pygame.transform.scale(pygame.image.load(IMAGE_0_r), C_SIZE),
                1: pygame.transform.scale(pygame.image.load(IMAGE_1_r), C_SIZE)
            },
            UP: {
                0: pygame.transform.scale(pygame.image.load(IMAGE_0_u), C_SIZE),
                1: pygame.transform.scale(pygame.image.load(IMAGE_1_u), C_SIZE)
            },
            DOWN: {
                0: pygame.transform.scale(pygame.image.load(IMAGE_0_d), C_SIZE),
                1: pygame.transform.scale(pygame.image.load(IMAGE_1_d), C_SIZE)
            },
            STOP: {
                0: pygame.transform.scale(pygame.image.load(IMAGE_0_r), size),
                1: pygame.transform.scale(pygame.image.load(IMAGE_1_r), size)
            }
        }
        self.heart_image = pygame.transform.scale(pygame.image.load(HEART_PATH), (90, 90))

    # def eat_pallet(self, pallets):
    #    try:
    #       pallets[self.position].eat(self)
    #      del pallets[self.position]
    # except:
    #    pass

    def eat_pallet(self, pallets):
        if self.position in pallets and pallets[self.position] is not None:
            pallets[self.position].eat(self)
            del pallets[self.position]

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify(self):
        for observer in self.observers:
            observer.notify()

    def restart(self):
        self.position = self.home_scorner.coordinate
        self.current_node = self.home_scorner
        self.score = 0
        self.life = 3
        self.direction = STOP
        self.next_direction = STOP

    def get_mode(self):
        return self.mode

    def get_power_time(self):
        return self.power_time

    def set_mode(self, mode):
        if mode == MODE_INVINCIBLE:
            self.power_time = self.invincible_time
        self.mode = mode
        self.notify()

    def get_heart_image(self):
        return self.heart_image

    def get_score(self):
        return self.score

    def get_life(self):
        return self.life

    def get_position(self):
        return self.position

    def get_direction(self):
        return self.direction

    def lose_life(self):
        self.life -= 1

    def get_current_node(self):
        return self.current_node

    def update(self):
        self.update_time()
        self.target = self.get_next_position()
        if self.position != self.target.coordinate:
            self.position = tuple(a + b for a, b in zip(self.position, self.movement[self.direction]))
            self.change_frame()
        else:
            self.current_node = self.target
            self.direction = self.next_direction
            if self.current_node.neighbors[PORTAL] is not None:
                self.current_node = self.current_node.neighbors[PORTAL][0]
                self.position = self.current_node.coordinate

    def change_frame(self):
        if self.direction == UP or self.direction == DOWN:
            if self.position[1] % 10 == 0:
                if self.frame == 0:
                    self.frame = 1
                else:
                    self.frame = 0
        else:
            if self.position[0] % 10 == 0:
                if self.frame == 0:
                    self.frame = 1
                else:
                    self.frame = 0

    def draw(self, screen):
        self.update()
        screen.blit(self.images[self.direction][self.frame], (self.position[0] - 16, self.position[1] - 16))

    def next_is_valid(self):
        if self.direction == STOP:
            return False
        if self.current_node.neighbors[self.direction] is not None:
            if self.current_node.neighbors[self.direction][0].get_name() == GATE:
                return False
            return True

        return False

    def get_next_position(self):
        if self.direction == STOP or not self.next_is_valid():
            return self.current_node
        if self.current_node.neighbors[self.direction] == self.current_node.neighbors[PORTAL]:
            return self.current_node
        return self.current_node.neighbors[self.direction][0]

    def back_home(self):
        self.position = self.home_scorner.coordinate
        self.current_node = self.home_scorner
        self.mode = MODE_VULNERABLE
        self.direction = STOP
        self.next_direction = STOP

    def set_direction(self, direction):
        if self.direction == direction:
            return
        if self.direction == opposite(direction) or self.direction == STOP:
            self.direction = direction
            self.next_direction = direction
        elif self.is_near() and self.target.neighbors[direction] is not None:
            self.next_direction = direction

    def is_near(self):
        if self.direction == UP:
            return self.position[1] - 30 <= self.target.coordinate[1]
        if self.direction == DOWN:
            return self.position[1] + 30 >= self.target.coordinate[1]
        if self.direction == RIGHT:
            return self.position[0] + 30 >= self.target.coordinate[0]
        if self.direction == LEFT:
            return self.position[0] - 30 <= self.target.coordinate[0]

        return False

    def update_time(self):
        if self.mode == MODE_INVINCIBLE:
            self.power_time -= 0.01
            if self.power_time <= 0:
                self.set_mode(MODE_VULNERABLE)
                self.kill = 1

    def ghost_kill(self):
        self.score += 200 * self.kill
        self.kill += 1

    def save_state(self):
        state = {
            'position': self.position,
            'current_node': self.current_node.coordinate,
            'target_node': self.target.coordinate,
            'score': self.score,
            'life': self.life,
            'mode': self.mode,
            'direction': self.direction,
            'next_direction': self.next_direction,
            'power_time': self.power_time,
            'invincible_time': self.invincible_time,
            'kill': self.kill,
            'frame': self.frame
        }
        return state

    def load_state(self, state, graph, home_scorner):
        self.home_scorner = home_scorner
        self.position = state['position']
        self.current_node = graph.get_node_from_coordinate(state['current_node'])
        self.target = graph.get_node_from_coordinate(state['target_node'])
        self.score = state['score']
        self.life = state['life']
        self.mode = state['mode']
        self.direction = state['direction']
        self.next_direction = state['next_direction']
        self.power_time = state['power_time']
        self.invincible_time = state['invincible_time']
        self.kill = state['kill']
        self.frame = state['frame']
