# Librerias/Modulos necesarios
from PACMAN.Interface.Map.Graph import Graph
from PACMAN.Interface.Map.mapGenerator import Maze_Generator
from PACMAN.edible.fruit import Fruit
from PACMAN.edible.pallet import Pallet
from PACMAN.edible.power_pill import Power_pill


class LevelManager:
    def __init__(self):
        self.level = 0  # Nivel y mapa del juego
        self.maze = Graph()  # El grafo que representa el laberinto
        self.pallets = {}  # Los objetos que Pac-Man puede comer

    def load_level(self):
        if 0 <= self.level <= 2:  # Límite para los niveles disponibles
            level_file = f"../../../resource/mazes/level{self.level}.txt"
            self.maze = Maze_Generator(level_file).get_graph()
            self.pallets = self.maze.get_pallets().copy()
        else:
            # Creditos o mensaje por pasar todos los niveles
            pass

    #Métodos para guardar el estado actual del nivel, los pallets e info del maze
    def save_state(self):
        pallets_state = [pallet.save_state() for pallet in self.pallets.values() if pallet is not None]
        return {
            'level': self.level,
            'maze_color': self.maze.color,
            'pallets': pallets_state
        }

    def load_state(self, state):
        self.level = state['level']
        self.pallets = {}
        self.maze = Graph()

        # Volver a cargar el grafo del nivel actual
        if 0 <= self.level <= 2:
            level_file = f"../../../resource/mazes/level{self.level}.txt"
            self.maze = Maze_Generator(level_file).get_graph()
            self.maze.set_color(state['maze_color'])
        else:
            # Créditos o mensaje por pasar todos los niveles
            pass

        for pallet_state in state['pallets']:
            if pallet_state:  #Si existe el estado entoces

                if pallet_state['type'] == "Pallet":
                    pallet = Pallet(pallet_state['position'])
                elif pallet_state['type'] == "PowerPill":
                    pallet = Power_pill(pallet_state['position'])
                else:
                    pallet = Fruit(pallet_state['position'], pallet_state['points'])

                pallet.load_state(pallet_state)
                self.pallets[pallet.position] = pallet

    def pass_level(self):
        self.level += 1
        if self.level > 2:
            self.level = 0
        self.load_level()

    def reset_level(self):
        self.pallets = self.maze.get_pallets().copy()

    def get_level(self):
        return self.level

    def get_pallets(self):
        return self.pallets

    def get_maze(self):
        return self.maze

    def has_pallets(self):
        return len(self.pallets) > 0