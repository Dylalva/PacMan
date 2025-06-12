import random

import pygame.draw
from PACMAN.Interface.constants import *
from PACMAN.Interface.Map.Node import *


class Graph:
    __slots__ = ('nodes', 'homes', 'corners', 'color', 'pallets', 'fruit_positions')

    def __init__(self):
        self.nodes = []  # lista que contiene los nodos del grafo
        self.homes = {  # nodos de inicio de cada personaje
            PACMAN: None,
            BLINKY: None,
            PINKY: None,
            INKY: None,
            CLYDE: None
        }
        self.pallets = None
        self.corners = {  # esquinas de cada enemigo
            BLINKY: None,
            PINKY: None,
            INKY: None,
            CLYDE: None
        }
        self.color = random.choice(MAZE_COLORS)
        self.fruit_positions = []

    def get_node_from_coordinate(self, coordinate):
        for node in self.nodes:
            if node.coordinate == coordinate:
                return node


    # Agregar un Nodo
    def add_node(self, node: Node):
        if node not in self.nodes:
            self.nodes.append(node)

    def connect_nodes(self, node1: Node, node2: Node, direction: str):
        if node1 not in self.nodes or node2 not in self.nodes:
            return
        node1.add_neighbor(node2, direction)

    # Metodo para dibujar el estado del grafo
    def _draw(self, screen):
        visited_edges = []
        for node in self.nodes:
            node.draw(screen, visited_edges, self.color)

    # metodo para pintar el mapa en una superficie, de esta manera solamente dibujamos el mapa una sola vez en vez de
    # estarlo renderizando constantemente
    def get_as_sprite(self):
        surface = pygame.Surface(SCREEN_SIZE, pygame.SRCALPHA)
        self._draw(surface)
        return surface.convert()

    def get_nodes(self):
        return self.nodes

    def get_home(self, character):
        if character in self.homes.keys():
            return self.homes[character]
        return None

    def get_corner(self, character):
        if character in self.corners.keys():
            return self.corners[character]
        return None

    def get_pallets(self):
        return self.pallets

    def get_fruit_positions(self):
        return self.fruit_positions

    def set_color(self, color):
        self.color = color