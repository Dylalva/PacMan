import random
import time

import pygame.constants
from pygame.display import update

from PACMAN.Player.PacMan import PacMan
from PACMAN.Interface.GameController.sound_manager import Sound_Manager
from PACMAN.Interface.GameController.ghost_manager import Ghost_manager
from PACMAN.Interface.constants import *
from PACMAN.Player.PacMan import *
from PACMAN.edible.fruit import *
from PACMAN.Interface.GameController.LevelManager import LevelManager  # Importar LevelManager
import pickle  # Módulo para serializar en Python
import os
from PACMAN.Interface.GameController.ButtonsGUI import *

# Tamaño de imágenes, fuente y otras constantes necesarias
SIZE_IMAGE = (264, 264)
INFO_HEIGHT = 20
INFO_WIDTH = SCREEN_WIDTH / 5 - 50
FONT_PATH = "../../../resource/font/Tiny5-Regular.ttf"


class GameController:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
        self.background = None   #maze
        self.clock = pygame.time.Clock()
        self.level_manager = LevelManager()
        self.pac_man = None
        self.fruit = None
        self.ghost_manager = None
        self.image_pause = pygame.transform.scale(pygame.image.load("../../../resource/game/PAUSE_GAME.PNG"),
                                                  SIZE_IMAGE)
        self.image_game_over = pygame.transform.scale(pygame.image.load("../../../resource/game/GAME_OVER.PNG"),
                                                      SIZE_IMAGE)
        self.loadFile = False

    # Métodos para guardar el estado actual del juego en un archivo

    #  =======================================================================================
    #        Página web que se utilizó para entender cómo funciona la
    #        serialización en Python con Pickle:
    #        https://www.datacamp.com/tutorial/pickle-python-tutorial?utm_source=google&utm_medium=paid_search&utm_campaignid=21057859163&utm_adgroupid=157296744657&utm_device=c&utm_keyword=&utm_matchtype=&utm_network=g&utm_adpostion=&utm_creative=719914247728&utm_targetid=dsa-2218886984100&utm_loc_interest_ms=&utm_loc_physical_ms=9075466&utm_content=&utm_campaign=230119_1-sea~dsa~tofu_2-b2c_3-es-lang-en_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na-fawnov24&gad_source=1&gclid=Cj0KCQiAire5BhCNARIsAM53K1i_u3X8w0rAgphTuPmXAsAkh05M1bG-S8g-iV693Dy5ACAL_nxAskQaAnxHEALw_wcB
    #  ========================================================================================

    def save_game_state_to_file(self):
        file_path = '../../../resource/saved_games/game_state.pkl'
        directory = os.path.dirname(file_path)

        if not os.path.exists(directory):
            os.makedirs(directory)

        game_state = {
            'level_manager': self.level_manager.save_state(),
            'pac_man': self.pac_man.save_state(),
            'ghost_manager': self.ghost_manager.save_state(),
        }
        with open(file_path, 'wb') as f:
            pickle.dump(game_state, f)

    def load_game_state_from_file(self):
        try:
            with open('../../../resource/saved_games/game_state.pkl', 'rb') as f:
                game_state = pickle.load(f)

            self.level_manager.load_state(game_state['level_manager'])
            self.pac_man.load_state(game_state['pac_man'],self.level_manager.maze,self.level_manager.maze.get_home(PACMAN))
            self.ghost_manager.load_state(game_state['ghost_manager'],self.level_manager.level, self.level_manager.maze, self.pac_man)
        except FileNotFoundError:
            print("No se encontró el archivo para cargar el juego")

    def check_save_file_exists(self):
        try:
            with open('../../../resource/saved_games/game_state.pkl', 'rb') as f:
                return True
        except FileNotFoundError:
            return False

    def exit_game(self):
        result = save_game(self.screen)
        if result == "save_game":
            self.save_game_state_to_file()
        if result == "back":
            return "back"
        return

    def set_background(self):
        self.background = self.level_manager.maze.get_as_sprite()

    def intro(self):
        Sound_Manager().play_intro()
        font = pygame.font.Font(FONT_PATH, 48)
        img = font.render('                   press intro to start!', True, YELLOW)
        self.screen.blit(img, (SCREEN_WIDTH / 4, SCREEN_HEIGHT - 70))
        pygame.display.update()
        self.pause_game()

    #Metodo para consultar al usuario si desea cargar o no la partida
    def main_menu(self):
        Sound_Manager().play_bg_music()
        result = main_menu(self.screen)
        Sound_Manager().stop_bg_music()
        if result == "new_game":
            self.loadFile = False
            self.start_game()
        elif result == "load_game":
            if self.check_save_file_exists():
                self.loadFile = True
                self.start_game()
            else:
                self.loadFile = False
                self.start_game()
        elif result == "exit":
            exit()

    def start_game(self):
        self.level_manager.load_level()

        self.pac_man = PacMan(self.level_manager.maze.get_home(PACMAN), self.level_manager.maze)
        self.ghost_manager = Ghost_manager(self.level_manager.maze, self.pac_man, self.level_manager.get_level())

        # Cargar la partida del archivo, en caso de que haya
        if self.loadFile:
            self.load_game_state_from_file()

        self.set_background()
        self.draw()
        self.intro()

    def update(self):
        self.check_events()
        self.generate_fruit()
        self.ghost_manager.update_ghost()
        self.check_collision()
        self.check_pallets()
        self.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.exit_game() == "back":     #Llama a la función para guardar el juego antes de terminar el programa
                    break
                self.ghost_manager.save()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.pac_man.set_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.pac_man.set_direction(RIGHT)
                elif event.key == pygame.K_UP:
                    self.pac_man.set_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.pac_man.set_direction(DOWN)
                elif event.key == pygame.K_ESCAPE:
                    self.draw_pause_game()

    def draw(self):
        self.clock.tick(120)
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (0, 0))
        self.pac_man.draw(self.screen)
        self.ghost_manager.draw_ghost(self.screen)
        self.draw_pallets()
        self.draw_info()
        pygame.display.update()

    def draw_info(self):
        font = pygame.font.Font(FONT_PATH, 48)

        img = font.render('level: ' + str(self.level_manager.get_level()+1), True, YELLOW)
        self.screen.blit(img, (INFO_WIDTH, INFO_HEIGHT))

        img = font.render('Score: ' + str(self.pac_man.get_score()), True, YELLOW)
        self.screen.blit(img, (INFO_WIDTH+250, INFO_HEIGHT))

        for i in range(1, self.pac_man.get_life() + 1):
            self.screen.blit(self.pac_man.get_heart_image(), ((INFO_WIDTH + 450) + i * 50, INFO_HEIGHT - 20))
        if self.pac_man.get_mode() == MODE_INVINCIBLE:
            img = font.render('time: ' + str(int(self.pac_man.get_power_time())), True, YELLOW)
            self.screen.blit(img, (INFO_WIDTH, SCREEN_HEIGHT - 75))


    def draw_pallets(self):
        for pallet in self.level_manager.pallets:
            self.level_manager.get_pallets()[pallet].draw(self.screen)

    def pause_game(self):
        pause = True
        while pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.exit_game() == 'back':
                        pause = False
                        break
                    self.ghost_manager.save()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pause = False

    def draw_game_over(self):
        self.screen.blit(self.image_game_over,
                         (SCREEN_SIZE[0] / 2 - SIZE_IMAGE[0] * 0.55, SCREEN_SIZE[1] / 2 - SIZE_IMAGE[0] * 0.5))
        pygame.display.update()

    def draw_pause_game(self):
        self.screen.blit(self.image_pause,
                         (SCREEN_SIZE[0] / 2 - SIZE_IMAGE[0] * 0.55, SCREEN_SIZE[1] / 2 - SIZE_IMAGE[0] * 0.5))
        pygame.display.update()
        result = pause_game(self.screen)
        if result == "exit":
            if self.exit_game() == "back":  # Llama a la función para guardar el juego antes de terminar el programa
                self.draw_pause_game()
                return
            self.ghost_manager.save()
            exit()
        elif result == "continue_game":
            return

    def check_collision(self):
        if self.ghost_manager.check_collisions():
            self.draw()
            self.reset()
            if self.pac_man.get_life() <= 0:
                self.draw_game_over()
                self.restart()
            else:
                font = pygame.font.Font(FONT_PATH, 44)
                img = font.render("PRESS ENTER TO RESTART", True, YELLOW)
                self.screen.blit(img, (SCREEN_SIZE[0] / 5, SCREEN_SIZE[1] / 2))
                pygame.display.update()
            Sound_Manager().pac_man_death()
            pygame.time.delay(2)
            self.pause_game()
        else:
            self.pac_man.eat_pallet(self.level_manager.pallets)

    def reset(self):
        self.ghost_manager.reset()
        self.pac_man.back_home()

    def restart(self):
        self.ghost_manager.reset()
        self.pac_man.restart()
        self.level_manager.reset_level()
        self.fruit = None

    # metodo encargado de gestionar la logica de las frutas, empieaza a generar frutas aleatorias luego de que pacman haya
    # consumido mas de la mitad de puntos, entre mas puntos coma mayor es la probabilidad de que aparezca una fruta
    # hay probabilidad de generar una fruta luego de haber comido 20 puntos
    def generate_fruit(self):
        fruits = self.level_manager.get_pallets()
        if self.fruit is not None:
            self.fruit.update()  # actualizar el tiempo restante de la fruta
            if self.fruit.get_time() <= 0:  # en caso de que se haya agotado el tiempo,
                # sacar la fruta de la lista de comestibles
                try:
                    f = self.fruit
                    self.fruit = None
                    del fruits[f.position]
                    print("fruta eliminada")
                except:
                    pass
            return
        # en caso de que no haya una fruta generada, vemos si generamos una en base a la cantidad de puntos de pacman
        # ver si pacman ya supero el 50% de los puntos
        total_points = len(self.level_manager.get_maze().get_pallets())  # cantidad de pallets totales
        relative_points = len(self.level_manager.get_pallets())  # cantidad de pallets restantes
        if relative_points <= total_points / 2 and relative_points % 20 == 0:  # si pacman ya supero la mitad de los puntos minimos, podemos generar una fruta
            pallets_eaten = total_points - relative_points
            dice = random.randint(0, 100)  # genera un numero aleatorio entre 1 y 100
            prob = (100 / total_points * pallets_eaten) // 70  # probabilidad del 30% de aparicion de una fruta
            if dice <= prob:
                position = random.choice(self.level_manager.get_maze().get_fruit_positions())
                self.fruit = Fruit(position, 500)
                self.level_manager.get_pallets()[position] = self.fruit

    def check_pallets(self):
        fruit = int(self.fruit is not None)
        if len(self.level_manager.get_pallets()) - fruit == 0:
            print("Nivel completado")
            font = pygame.font.Font(FONT_PATH, 44)
            img = font.render("Level Completed", True, YELLOW)
            self.screen.blit(img, (SCREEN_SIZE[0] / 4, SCREEN_SIZE[1] / 2))
            pygame.display.update()
            pygame.time.delay(2400)
            self.level_manager.pass_level()
            self.set_background()
            self.pac_man = PacMan(self.level_manager.maze.get_home(PACMAN), self.level_manager.maze)
            self.ghost_manager = Ghost_manager(self.level_manager.maze, self.pac_man, self.level_manager.get_level())