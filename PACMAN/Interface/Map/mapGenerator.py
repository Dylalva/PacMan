from PACMAN.Interface.Map.Graph import *
from PACMAN.Interface.Map.Node import *
from PACMAN.edible.pallet import *
from PACMAN.edible.power_pill import *
import numpy


class Maze_Generator:
    def __init__(self, path):
        self.nodes_dict = {}
        self.node_symbols = ["+", "<", ">", PACMAN, BLINKY, PINKY, INKY, CLYDE, BLINKY.lower(), PINKY.lower(),
                             INKY.lower(), CLYDE.lower(), "*", "n", "F", GATE]
        self.path_symbols = [".", "-", "|"]
        self.pallet_symbols = ['.', '+', '<', '>', BLINKY.lower(), PINKY.lower(), INKY.lower(), CLYDE.lower()]
        self.pill_symbols = ["*"]
        self.fruit_symbols = ["F"]
        self.fruit_positions = []
        self.left_portal = None
        self.right_portal = None
        self.homes = {  # nodos de inicio de cada personaje
            PACMAN: None,
            BLINKY: None,
            PINKY: None,
            INKY: None,
            CLYDE: None
        }
        self.corners = {  # nodos de inicio de cada personaje
            BLINKY: None,
            PINKY: None,
            INKY: None,
            CLYDE: None
        }
        self.edibles = {}
        data = self.read_maze_file(path)
        self.create_node_table(data)
        self.connect_horizontally(data)
        self.connect_vertically(data)

    def read_maze_file(self, path):
        return numpy.loadtxt(path, dtype='<U1')

    def create_node_table(self, data, xoffset=10, yoffset=5):
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                x, y = self.construct_key(col + xoffset, row + yoffset)
                if data[row][col] in self.node_symbols:
                    self.nodes_dict[(x, y)] = Node(data[row][col], x, y)
                    self.check_portals(data[row][col], x, y)
                    self.check_homes(data[row][col], x, y)
                    self.check_corners(data[row][col], x, y)
                self.check_pallet(data[row][col], x, y)
                self.check_fruit(data[row][col], x, y)

    def check_portals(self, character, x, y):
        if character == "<":
            self.left_portal = self.nodes_dict[(x, y)]
            self.left_portal.set_as_portal()
        elif character == ">":
            self.right_portal = self.nodes_dict[(x, y)]
            self.right_portal.set_as_portal()

    def check_homes(self, character, x, y):
        if character in self.homes.keys():
            self.homes[character] = self.nodes_dict[(x, y)]

    def check_corners(self, character, x, y):
        if character.upper() in self.corners.keys():
            self.corners[character.upper()] = self.nodes_dict[(x, y)]

    def check_pallet(self, character, x, y):
        if character in self.pallet_symbols:
            self.edibles[(x, y)] = Pallet((x, y))
        if character in self.pill_symbols:
            self.edibles[(x, y)] = Power_pill((x, y))

    def connect_horizontally(self, data, xoffset=10, yoffset=5):
        if self.right_portal is not None and self.left_portal is not None:
            self.right_portal.add_neighbor(self.left_portal, RIGHT, 1)
            self.right_portal.add_neighbor(self.left_portal, PORTAL, 1)
            self.left_portal.add_neighbor(self.right_portal, LEFT, 1)
            self.left_portal.add_neighbor(self.right_portal, PORTAL, 1)
        for row in list(range(data.shape[0])):
            key = None
            for col in list(range(data.shape[1])):
                if data[row][col] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.construct_key(col + xoffset, row + yoffset)
                        self.nodes_dict[key].add_neighbor(self.nodes_dict[otherkey], RIGHT)
                        key = otherkey
                elif data[row][col] not in self.path_symbols:
                    key = None

    def connect_vertically(self, data, xoffset=10, yoffset=5):
        dataT = data.transpose()
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.node_symbols:
                    if key is None:
                        key = self.construct_key(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.construct_key(col + xoffset, row + yoffset)
                        self.nodes_dict[key].add_neighbor(self.nodes_dict[otherkey], DOWN)
                        key = otherkey
                elif dataT[col][row] not in self.path_symbols:
                    key = None

    def construct_key(self, x, y):
        return x * TILE_WIDTH, y * TILE_HEIGHT

    def get_graph(self):
        maze = Graph()
        for key in self.nodes_dict.keys():
            maze.add_node(self.nodes_dict[key])
        maze.homes = self.homes
        maze.corners = self.corners
        maze.pallets = self.edibles
        maze.fruit_positions = self.fruit_positions
        return maze

    def check_fruit(self, symbol, x, y):
        if symbol in self.fruit_symbols:
            self.fruit_positions.append((x, y))

# ===============================================================================================

# los algoritmos utilizados en este modulo fueron tomados de : https://pacmancode.com/maze-basics
# y adaptados a la estructura de este proyecto

# ===============================================================================================
