import pickle
import random
import pygame
import numpy as np
from PACMAN.Enemy.Ghost import Ghost, MODE_FRIGHTENED
from PACMAN.Enemy.Q_Learning import QLearning
from PACMAN.Interface.constants import *

IMAGE_IDLE = "../../../resource/Ghost/Inky.png"
IMAGE_DOWN = "../../../resource/Ghost/InkyDown.png"
IMAGE_UP = "../../../resource/Ghost/InkyUp.png"
IMAGE_RIGHT = "../../../resource/Ghost/InkyRight.png"
IMAGE_LEFT = "../../../resource/Ghost/InkyLeft.png"


class Inky(Ghost):
    def __init__(self, home_corner, scatter_corner, graph, target, blinky, state_size=100, action_size=4, level = 0):
        super().__init__(home_corner, scatter_corner, graph, target)
        self.blinky = blinky
        self.qlearning = QLearning(state_size, action_size)  # Inicializar QLearning
        self.load_image()
        self.load_q_table(level)

    def chase(self):
        self.target_position = self.calculate_next_position()
        self.follow_target(self.target_position)

    def calculate_target(self):
        blinky_position = self.blinky.get_position()
        pacman_position = self.target.get_current_node()
        dir_pac_man = self.target.get_direction()

        # Seleccionar una acción basada en la tabla Q para maximizar la recompensa
        state = self.get_state(blinky_position, pacman_position)
        action = self.qlearning.choose_action(state)

        # Calcular la nueva posición de destino basada en la acción y las posiciones de Blinky y Pac-Man
        target_position = self.calculate_q_target(blinky_position, pacman_position, action)
        reward = self.get_reward(target_position, pacman_position)

        # Actualizar la tabla Q
        next_state = self.get_state(blinky_position, target_position)
        self.qlearning.update_q_table(state, action, reward, next_state)

        return target_position

    def calculate_q_target(self, blinky_position, pacman_position, action):
        dx, dy = [(-1, 0), (1, 0), (0, -1), (0, 1)][action]
        target_x = blinky_position.coordinate[0] + dx * (pacman_position.coordinate[0] - blinky_position.coordinate[0])
        target_y = blinky_position.coordinate[1] + dy * (pacman_position.coordinate[1] - blinky_position.coordinate[1])
        # Linea hecha con ChatGPT
        closest_node = min(self.graph.get_nodes(),
                           key=lambda node: (node.coordinate[0] - target_x) ** 2 + (node.coordinate[1] - target_y) ** 2)
        return closest_node

    def get_state(self, blinky_position, pacman_position):
        return (blinky_position.coordinate, pacman_position.coordinate)

    def get_reward(self, target_position, pacman_position):
        # np.linalg.norm calcula la norma euclidiana
        distance = np.linalg.norm(np.array(target_position.coordinate) - np.array(pacman_position.coordinate))
        return 1.0 / (distance + 1e-5)  # Para evitar divisiones por cero

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

    # Métodos para guardar y cargar la tabla Q
    def save_q_table(self, level):
        filename = f'../../../resource/qtable/q{level}_table_inky.pkl'
        try:
            with open(filename, 'wb') as fw:
                pickle.dump(self.qlearning.q_table, fw)
        except Exception as e:
            pass

    def load_q_table(self, level):
        filename = f'../../../resource/qtable/q{level}_table_inky.pkl'
        try:
            with open(filename, 'rb') as fr:
                self.qlearning.q_table = pickle.load(fr)
        except Exception as e:
            pass

    def save_state(self):
        state = super().save_state()
        state.update({
            'type': self.type()
        })
        return state

    def type(self):
        return 'Inky'

    def load_state(self, state, maze, pacman):
        super().load_state(state, maze, pacman)



    def print_q_table(self):
        print("Tabla Q de Inky:")
        for state, actions in self.qlearning.q_table.items():
            print(f"Estado: {state} -> Acciones: {actions}")
