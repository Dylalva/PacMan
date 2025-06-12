import pickle

import pygame
import numpy as np
from PACMAN.Enemy.Ghost import Ghost, MODE_FRIGHTENED
from PACMAN.Enemy.Q_Learning import QLearning
from PACMAN.Interface.constants import *

IMAGE_IDLE = "../../../resource/Ghost/Pinky.png"
IMAGE_DOWN = "../../../resource/Ghost/PinkyDown.png"
IMAGE_UP = "../../../resource/Ghost/PinkyUp.png"
IMAGE_RIGHT = "../../../resource/Ghost/PinkyRight.png"
IMAGE_LEFT = "../../../resource/Ghost/PinkyLeft.png"

class Pinky(Ghost):
    def __init__(self, home_corner, scatter_corner, graph, target, state_size=100, action_size=4, level = 0):
        super().__init__(home_corner, scatter_corner, graph, target)
        self.qlearning = QLearning(state_size, action_size)
        self.load_image()
        self.load_q_table(level)

    def chase(self):
        self.target_position = self.calculate_next_position()
        self.follow_target(self.target_position)

    def calculate_target(self):
        pacman_position = self.target.get_current_node()
        pacman_direction = self.target.get_direction()

        # Seleccionar acción de Q-Learning
        state = self.get_state(pacman_position, pacman_direction)
        action = self.qlearning.choose_action(state)

        # Determinar el objetivo según la acción
        target_position = self.calculate_q_target(pacman_position, action)
        reward = self.get_reward(target_position, pacman_position)

        # Actualizar la tabla Q
        next_state = self.get_state(target_position, pacman_direction)
        self.qlearning.update_q_table(state, action, reward, next_state)

        return target_position

    def calculate_q_target(self, pacman_position, action):
        offset = [(-4, 0), (4, 0), (0, -4), (0, 4)][action]
        target_x = pacman_position.coordinate[0] + offset[0]
        target_y = pacman_position.coordinate[1] + offset[1]
        #Linea hecha con ChatGPT
        closest_node = min(self.graph.get_nodes(),
                           key=lambda node: (node.coordinate[0] - target_x) ** 2 + (node.coordinate[1] - target_y) ** 2)
        return closest_node

    def get_state(self, pacman_position, pacman_direction):
        return (pacman_position.coordinate, pacman_direction)

    def get_reward(self, target_position, pacman_position):
        # np.linalg.norm calcula la norma euclidiana
        distance = np.linalg.norm(np.array(target_position.coordinate) - np.array(pacman_position.coordinate))
        return 1.0 / (distance + 1e-5)  # Recompensa segun la distancia

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
        filename = f'../../../resource/qtable/q{level}_table_pinky.pkl'
        try:
            with open(filename, 'wb') as fw:
                pickle.dump(self.qlearning.q_table, fw)
        except Exception as e:
            pass

    def load_q_table(self, level):
        filename = f'../../../resource/qtable/q{level}_table_pinky.pkl'
        try:
            with open(filename, 'rb') as fr:
                self.qlearning.q_table = pickle.load(fr)
        except Exception as e:
            pass

    def print_q_table(self):
        print("Tabla Q de Pinky:")
        for state, actions in self.qlearning.q_table.items():
            print(f"Estado: {state} -> Acciones: {actions}")

    def save_state(self):
        state = super().save_state()
        state.update({
            'type': self.type()
        })
        return state

    def type(self):
        return 'Pinky'

    def load_state(self, state, maze, pacman):
        super().load_state(state, maze, pacman)
