from PACMAN.Interface.constants import *
import pygame
class Node:
    __slots__ = ['name', 'coordinate', 'neighbors', 'is_portal'] #Su funcion es ahorrar memoria, debido a la gran cantidad de nodos
                                                    #que se requieren para formar un grafo(mapa), si no hay un atributo
                                                    #en esta funcion se lanzara un AttributeError (Excepcion)
    def __init__(self, name, x, y):
        self.name = name #Nombre del nodo, puede servir para marcar un nodo con comida, pac-man, fantasma, etc
        self.coordinate = (x, y) #Coordenadas para saber la localizacion del nodo
        # Vecinos del nodo
        self.neighbors = {
            UP: None,
            DOWN: None,
            RIGHT: None,
            LEFT: None,
            PORTAL: None
        }
        self.is_portal = False  # Inicialmente, un nodo no es un portal

    def set_as_portal(self):
        self.is_portal = True

    def is_portal_node(self):
        return self.is_portal

    def get_name(self):
        return self.name

    def get_coordinate(self):
        return self.coordinate

    def add_neighbor(self, neighbor, direction, weight=1):
        self.neighbors[direction] = (neighbor, weight)
        neighbor.neighbors[opposite(direction)] = (self, weight)

    def draw(self, screen, visited_edges, color):
        if self.name in INVICIBLE_NODES:
            return
        if self.name == GATE:
            self._draw_gate(screen)
            return
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None and n is not PORTAL and self.neighbors[n] != self.neighbors[PORTAL]:
                if (self.neighbors[n][0], self) not in visited_edges:
                    self._draw_edges(self.coordinate, self.neighbors[n][0].coordinate, n, screen, color)
                visited_edges.append((self, self.neighbors[n][0]))

        self.close_holes(screen, color)

    def close_holes(self, screen, color):
        if self.neighbors[LEFT] is None:
            start = (self.coordinate[0]-16, self.coordinate[1]+14)
            end = (self.coordinate[0]-16, self.coordinate[1]-14)
            pygame.draw.line(screen, color, start, end, 4)
        if self.neighbors[RIGHT] is None:
            start = (self.coordinate[0]+16, self.coordinate[1]+14)
            end = (self.coordinate[0]+16, self.coordinate[1]-14)
            pygame.draw.line(screen, color, start, end, 4)
        if self.neighbors[UP] is None:
            start = (self.coordinate[0] + 14, self.coordinate[1]-16)
            end = (self.coordinate[0] - 14, self.coordinate[1]-16)
            pygame.draw.line(screen, color, start, end, 4)
        if self.neighbors[DOWN] is None:
            start = (self.coordinate[0] + 14, self.coordinate[1]+16)
            end = (self.coordinate[0] - 14, self.coordinate[1]+16)
            pygame.draw.line(screen, color, start, end, 4)

    def _draw_edges(self, orig, dest, direction, screen, color):
        if direction == LEFT or direction == RIGHT:
            line_start = (orig[0]+14, orig[1]+16)
            line_end = (dest[0]-14, dest[1]+16)
            pygame.draw.line(screen, color, line_start, line_end, 4)
            line_start = (orig[0]+14, orig[1]-16)
            line_end = (dest[0]-14, dest[1]-16)
            pygame.draw.line(screen, color, line_start, line_end, 4)
        else:
            line_start = (orig[0]+16, orig[1]+14)
            line_end = (dest[0]+16, dest[1]-14)
            pygame.draw.line(screen, color, line_start, line_end, 4)
            line_start = (orig[0]-16, orig[1]+14)
            line_end = (dest[0]-16, dest[1]-14)
            pygame.draw.line(screen, color, line_start, line_end, 4)

    #Obtener los vecinos disponibles
    def get_neighbors(self):
        return [(neighbor, weight) for direction, neighbor_weight in self.neighbors.items() if
                neighbor_weight is not None for neighbor, weight in [neighbor_weight]]

    def get_neighbor_dir(self, dir):
        if dir == STOP:
            return None
        if self.neighbors[dir] is None:
            return None
        else:
            neighbor, _ = self.neighbors[dir]
            return neighbor

    def get_neighbors_with_direction(self):
        neighbors = [
            (neighbor_weight[0], neighbor_weight[1], direction)
            for direction, neighbor_weight in self.neighbors.items()
            if neighbor_weight is not None and direction != PORTAL
        ]

        if self.neighbors[PORTAL] is not None:
            portal_node, weight = self.neighbors[PORTAL]
            neighbors.append((portal_node, 1, PORTAL))  # Añadir la conexión del portal

        return neighbors

    def get_portal_destination(self):
        if PORTAL in self.neighbors and self.neighbors[PORTAL] is not None:
            portal_node, _ = self.neighbors[PORTAL]
            return portal_node
        return None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Node({self.name}, {self.coordinate})"

    def __eq__(self, other):
        if isinstance(other, Node): #isinstance verifica el tipo de instancia que recibe por parametro
            return self.coordinate == other.coordinate
        elif isinstance(other, tuple):
            return self.coordinate == other
        return False

    def __lt__(self, other):
        return self.coordinate < other.coordinate

    def __hash__(self):
        return self.coordinate.__hash__()

    def _draw_gate(self, screen):
        beg = (self.coordinate[0]-8, self.coordinate[1]-16)
        end = (self.coordinate[0]+8, self.coordinate[1]-16)
        pygame.draw.line(screen, RED, beg, end, 3)
