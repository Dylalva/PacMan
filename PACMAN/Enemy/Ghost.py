# Librerias/modulos utilizados
from PACMAN.Interface.Map.Graph import Graph
import pygame.draw
import random
from PACMAN.Player.PacMan import *
from PACMAN.Utils import AlgorithmicSearch
from PACMAN.Interface.Map.Node import Node
from PACMAN.Interface.constants import *
"""
Clase padre de los diferentes fantasmas que persiguen a Pac-Man
"""

# Modos de comportamiento
MODE_CHASE = "CHASE"
MODE_SCATTER = "SCATTER"
MODE_FRIGHTENED = "FRIGHTENED"


# ==========================================

class Ghost:
    __slots__ = \
        (
            "mode", "isAlive", "position", "position_frame", "speed", "home_corner", "frightened_time",
            "scatter_corner",
            "graph", "target",
            "direction", "in_scatter", "last_move_time", "movement", "images", "frame", "path", "change_direction",
            "image_eyes",
            "image_frightened"
        )

    def __init__(self, home_corner: Node, scatter_corner: Node, graph: Graph, target: PacMan):
        self.mode = MODE_SCATTER
        self.isAlive = True
        self.position = home_corner
        self.position_frame = home_corner.coordinate
        self.speed = 7  # Velocidad con la que se va a mover el fantasma (tiempo)
        self.home_corner = home_corner  # Ubicación inicial
        self.frightened_time = 0
        self.scatter_corner = scatter_corner  # Esquina predeterminada para cada fantasma (esquinas)
        self.graph = graph  # Grafo
        self.target = target  # Pac-Man
        self.target.add_observer(self)
        self.direction = STOP
        self.in_scatter = False
        self.change_direction = False
        self.last_move_time = 0  # Tiempo desde la última vez que se movió
        self.movement = {
            STOP: (0, 0),
            LEFT: (-1, 0),
            RIGHT: (1, 0),
            DOWN: (0, 1),
            UP: (0, -1)
        }
        self.images = {}
        self.frame = 0
        self.path = []  # Camino que se generará a la hora del modo scatter
        self.image_eyes = pygame.transform.scale(pygame.image.load("../../../resource/Ghost/eyes.png"), (32, 32))
        self.image_frightened = pygame.transform.scale(pygame.image.load("../../../resource/Ghost/frightedGhost.png"),
                                                       G_SIZE)

    def get_position(self):
        return self.position

    # region Movimiento y modos de comportamiento
    def move(self):
        if not self.isAlive:
            self.reset()
        elif self.mode == MODE_CHASE:
            self.chase()
        elif self.mode == MODE_SCATTER:
            self.scatter()
        elif self.mode == MODE_FRIGHTENED:
            self.frightened()

    def teleport_to_opposite_portal(self):
        for direction, neighbor_data in self.position.neighbors.items():
            neighbor, weight = neighbor_data if neighbor_data else (None, None)

            if neighbor and neighbor.is_portal_node() and neighbor != self.position:
                # Teletransporta al otro lado del portal
                self.position_frame = self.get_position().get_portal_destination().coordinate
                self.position = self.get_position().get_portal_destination()


    # Metodo de persecución, se comporta de acuerdo al tipo de fantasma
    def chase(self):
        pass

    def type(self):
        pass

    def save_state(self):
        return {
            'mode': self.mode,
            'isAlive': self.isAlive,
            'position': self.position.coordinate,
            'home_corner': self.home_corner.coordinate,
            'scatter_corner': self.scatter_corner.coordinate,
            'position_frame': self.position_frame,
            'speed': self.speed,
            'frame': self.frame,
            'frightened_time': self.frightened_time,
            'direction': self.direction,

        }

    def load_state(self, state, graph, pacman):
        self.mode = state.get('mode', self.mode)
        self.frame = state.get('frame', self.frame)
        self.isAlive = state.get('isAlive', self.isAlive)
        self.position = graph.get_node_from_coordinate(state['position'])
        self.position_frame = state.get('position_frame', self.position_frame)
        self.speed = state.get('speed', self.speed)
        self.home_corner = graph.get_node_from_coordinate(state['home_corner'])
        self.frightened_time = state.get('frightened_time', self.frightened_time)
        self.scatter_corner = graph.get_node_from_coordinate(state['scatter_corner'])
        self.direction = state.get('direction', self.direction)
        self.graph = graph
        self.target = pacman

    def set_level(self, level):
        self.speed -= level*2

    def notify(self):
        if self.target.get_mode() == MODE_INVINCIBLE:
            if self.mode == MODE_FRIGHTENED:
                return
            self.mode = MODE_FRIGHTENED
        else:
            if self.mode == MODE_CHASE:
                return
            self.mode = MODE_CHASE
        # self.position_frame = self.position.coordinate

    # Metodo para dispersión, el fantasma se dirige a su esquina asignada
    def scatter(self):
        #Comprueba si se debe teletransportar
        if self.position.is_portal_node():
            return self.teleport()
        if self.position == self.scatter_corner and not self.in_scatter:
            self.in_scatter = True
            self.find_path()
        elif self.in_scatter and self.path:
            self.follow_target(self.path[0])
            self.path.pop(0)
            if not self.path:
                self.in_scatter = False
        else:
            self.follow_target(self.scatter_corner)

    # Metodo para el comportamiento en modo asustado(busca la posición mas lejana a Pac-Man)
    def frightened(self):
        # Comprueba si se debe teletransportar
        if self.position.is_portal_node():
            return self.teleport()
        pacman_position = self.target.get_next_position()
        distance = self._heuristic(self.position, pacman_position)
        target_position = self.find_furthest_point(pacman_position)
        if distance > 100:
            self.follow_target(self.find_median_target(self.position))
        else:
            self.follow_target(target_position)

    def update_mode(self, mode):
        if self.mode != mode:
            self.mode = mode
            self.change_direction = True

    # Metodo para verificar colisiones con Pac-Man
    def check_collision_with_pacman(self):
        pacman_position = self.target.get_position()
        xp = pacman_position[0]
        yp = pacman_position[1]

        xs = self.position_frame[0]
        ys = self.position_frame[1]

        if ((xp-xs)**2 + (yp-ys)**2)**(1/2) <= 10:
            if self.mode == MODE_FRIGHTENED:
                if self.isAlive:
                    self.position_frame = self.position.coordinate
                self.isAlive = False
                self.target.ghost_kill()
                self.reset()
            elif self.isAlive and self.mode != MODE_FRIGHTENED:
                self.target.lose_life()
                return True

        return False

    def get_next_frame(self):
        x = self.position_frame[0] + self.movement[self.direction][0]
        y = self.position_frame[1] + self.movement[self.direction][1]
        return (x, y)

    # Metodo para reiniciar al fantasma a su estado inicial
    def reset(self):
        if self.isAlive:
            self.position = self.home_corner
            self.position_frame = self.home_corner.coordinate
        elif self.position != self.home_corner:
            self.position_frame = self.position.coordinate
            self.change_direction = True
            self.follow_target(self.home_corner)
            return
        self.mode = MODE_SCATTER
        self.direction = STOP
        self.isAlive = True

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.speed:
            self.update_frame()
            if self.position_frame == self.position.coordinate:
                self.position_frame = self.position.coordinate
                self.move()
            self.last_move_time = current_time

    # endregion

    def teleport(self):
        self.teleport_to_opposite_portal()
        if self.position.get_portal_destination() == self.position.get_neighbor_dir(RIGHT):
            return self.follow_target(self.position.get_neighbor_dir(LEFT))
        if self.position.get_portal_destination() == self.position.get_neighbor_dir(LEFT):
            return self.follow_target(self.position.get_neighbor_dir(RIGHT))


    # region Metodos para seguir
    def calculate_next_position(self):
        # Comprueba si se debe teletransportar
        if self.position.is_portal_node():
            return self.teleport()

        # Si tiene al pacman al frente
        if self.position == self.target.get_next_position():
            return self.target.current_node
        else:
            return self.calculate_target()

    # Metodo para calcular la siguiente estrategia de cada fantasma
    def calculate_target(self):
        pass

    # Metodo para seguir la posición objetivo
    def follow_target(self, movement):
        start = self.position
        goal = movement
        if not self.change_direction:
            came_from, _ = AlgorithmicSearch.a_star_search_with_direction(start, goal, self.direction)
        else:
            came_from, _ = AlgorithmicSearch.a_star_search_with_direction(start, goal, STOP)
            self.change_direction = False

        # Mueve al siguiente nodo en la ruta genereda por A*
        next_node = self.move_with_dict_with_direction(start, goal, came_from)
        if next_node:
            self._set_direction(next_node)
            if next_node == self.position:
                self.position_frame = next_node.coordinate
            self.position = next_node
        return self.position

    # endregion

    # region Algoritmos de búsqueda y cálculo de caminos
    # Algoritmo A* para buscar el camino más corto
    # Fuente base: https://www.geeksforgeeks.org/a-search-algorithm-in-python/
    def a_star_search(self, start, goal):
        return AlgorithmicSearch.a_star_search(start, goal)

    # Heurística de distancia Manhattan (distancia entre dos puntos en un plano)
    def _heuristic(self, nodeA, nodeB):
        return AlgorithmicSearch.heuristic(nodeA, nodeB)

    # Algoritmo para sacar la ruta de un diccionario
    def move_with_dict(self, start, goal, dict):
        path = []
        current = goal
        if current not in dict:
            return start
        while current != start:
            path.append(current)
            current = dict[current]
        path.reverse()
        if path:
            return path[0]
        else:
            return None

    def move_with_dict_with_direction(self, start, goal, came_from):
        path = []
        current = goal
        if current not in came_from:
            return start
        while current != start:
            path.append(current)
            current, _ = came_from[current]
        path.reverse()
        if path:
            return path[0]
        else:
            return None

    """
    Método para buscar una ruta que seguir en el momento que llega a su scatter_corner correspondiente.
    Este método busca la ruta más corta para dar la 'vuelta' alrededor de su esquina.
    """
    def find_path(self):
        directions = [LEFT, RIGHT, UP, DOWN]
        dir_ini = None
        node_visited = set()
        movement = 0

        for dir in directions:
            if self.scatter_corner.get_neighbor_dir(dir) is not None:
                dir_ini = dir
                break
        node_visited.add(self.scatter_corner)
        node = self.scatter_corner.get_neighbor_dir(dir_ini)
        self.path.append(node)
        node_visited.add(node)

        while node != self.scatter_corner:
            if movement >= 2:
                for i in directions:
                    if node.get_neighbor_dir(i) == self.scatter_corner:
                        self.path.append(self.scatter_corner)
                        return
            distances = []
            neighbors_with_distances = {}
            for i in directions:
                aux = node.get_neighbor_dir(i)
                if aux and aux not in node_visited:
                    distance = self._heuristic(aux, self.scatter_corner)
                    distances.append(distance)
                    neighbors_with_distances[distance] = (aux, i)

            if distances:
                min_distance = min(distances)
                next_node, dir_ini = neighbors_with_distances[min_distance]
                self.path.append(next_node)
                node_visited.add(next_node)
                node = next_node
                movement += 1
            else:
                break

        if self.path[-1] != self.scatter_corner:
            self.path.append(self.scatter_corner)

    # endregion

    # region Auxiliares para los metodos de busqueda
    # Encuentra un nodo que esté a una distancia media desde el goal.
    def find_median_target(self, goal):
        candidates = []
        for node in self.graph.get_nodes():
            distance = self._heuristic(goal, node)
            if 2 <= distance <= 320:
                candidates.append(node)
        if candidates:
            return random.choice(candidates)
        else:
            return goal

    # Encontrar el punto más lejano de Pac-Man
    def find_furthest_point(self, pacman_position):
        max_distance = -1
        furthest_Node = None
        for node in self.graph.get_nodes():
            distance = self._heuristic(node, pacman_position)
            if distance > max_distance:
                max_distance = distance
                furthest_Node = node
        return furthest_Node

    # endregion

    # region Funciones para la interfaz
    def load_image(self):
        pass

    def draw(self, screen):
        pass

    def update_frame(self):
        if self.position_frame != self.position.coordinate:
            self.position_frame = tuple(a + b for a, b in zip(self.position_frame, self.movement[self.direction]))

    def _set_direction(self, next_node):
        cx = next_node.coordinate[0] - self.position.coordinate[0]
        cy = next_node.coordinate[1] - self.position.coordinate[1]
        if cx > 0:
            self.direction = RIGHT
        elif cx < 0:
            self.direction = LEFT
        elif cy > 0:
            self.direction = DOWN
        elif cy < 0:
            self.direction = UP
        else:
            self.direction = STOP

    # endregion

    def save_q_table(self, level):
        pass
