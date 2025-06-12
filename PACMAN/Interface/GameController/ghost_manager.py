import pygame
from PACMAN.Enemy.Blinky import Blinky
from PACMAN.Enemy.Clyde import Clyde
from PACMAN.Enemy.Ghost import MODE_SCATTER, MODE_CHASE, MODE_FRIGHTENED
from PACMAN.Enemy.Inky import Inky
from PACMAN.Enemy.Pinky import Pinky
from PACMAN.Interface.constants import *


class Ghost_manager:
    def __init__(self, maze, pac_man, level):
        self.ghost = []
        self.ghost.append(Blinky(maze.get_home(BLINKY), maze.get_corner(BLINKY), maze, pac_man))
        self.ghost.append(Pinky(maze.get_home(PINKY), maze.get_corner(PINKY), maze, pac_man, level))
        self.ghost.append(Clyde(maze.get_home(CLYDE), maze.get_corner(CLYDE), maze, pac_man))
        self.ghost.append(Inky(maze.get_home(INKY), maze.get_corner(INKY), maze, pac_man, self.ghost[0], level))
        self.time = pygame.time.get_ticks()
        self.set_level(level)  #le setea el nivel a todos los fantasmas
        self.cycle = 0
        self.level = level

    def update_ghost(self):
        for g in self.ghost:
            g.update()
        self.update_mode()

    def draw_ghost(self, screen):
        for g in self.ghost:
            g.draw(screen)

    def  reset(self):
        for g in self.ghost:
            g.reset()
        self.cycle = 0
        self.time = pygame.time.get_ticks()

    def check_collisions(self):
        for g in self.ghost:
            if g.check_collision_with_pacman():
                return True
        return False

    def save(self):
        for g in self.ghost:
            g.save_q_table(self.level)

    # Métodos para guardar y cargar los fantasmas
    def load_state(self, state,level, maze, pacman):

        # Cargar los estados de los fantasmas
        for ghost_state in state['ghosts']:
            for g in self.ghost:
                if ghost_state['type'] == g.type():
                    g.load_state(ghost_state, maze, pacman)
                    break


    def save_state(self):
        return {
            'ghosts': [g.save_state() for g in self.ghost]
        }


    def update_mode(self):
        for g in self.ghost:
            if g.mode == MODE_FRIGHTENED:
                return
        SCATTER_TIME = 7000  # 7 segundos para scatter
        CHASE_TIME = 20000  # 20 segundos para chase

        current_time = pygame.time.get_ticks()

        elapsed_time = current_time - self.time

        if self.cycle >= 3:
            for ghost in self.ghost:
                if ghost.mode != MODE_CHASE:
                    ghost.update_mode(MODE_CHASE)
        else:
            if elapsed_time <= SCATTER_TIME:
                for ghost in self.ghost:
                    ghost.update_mode(MODE_SCATTER)
            elif SCATTER_TIME < elapsed_time <= SCATTER_TIME + CHASE_TIME:
                for ghost in self.ghost:
                    ghost.update_mode(MODE_CHASE)
            else:
                self.cycle += 1
                self.time = current_time

    def set_level(self, level):
        self.level = level
        for g in self.ghost:
            g.set_level(level)
