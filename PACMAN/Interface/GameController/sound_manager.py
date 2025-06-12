import pygame.mixer
from PACMAN.Interface.constants import *

# ====================================================================
# rutas de los sonidos
INTRO = "../../../resource/game/pacman_beginning.wav"
# sonidos del pac_man
WAKA0 = "../../../resource/sounds/waka0.mp3"
WAKA1 = "../../../resource/sounds/waka1.mp3"
EATING_GHOST = "../../../resource/sounds/eating_ghost.mp3"
PAC_MAN_DEATH = "../../../resource/sounds/pacman_death.wav"
SIREN = "../../../resource/sounds/siren.mp3"
FRUIT = "../../../resource/sounds/pacman_eatfruit.wav"
BGMUSIC = "../../../resource/sounds/bgmusic.mp3"

# =====================================================================


# clase de servicios para manejar los sonidos
class Sound_Manager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # asegurarse que la instancia unica de la clase se inicialice una unica vez
        if not hasattr(self, "initialized"):  # Esto asegura que solo se inicialice una vez
            self.initialized = True
            pygame.mixer.init()
            self.intro = pygame.mixer.Sound(INTRO)
            self.eating_pallet = {
                0: pygame.mixer.Sound(WAKA0),
                1: pygame.mixer.Sound(WAKA1)
            }
            self.eatig_fruit = pygame.mixer.Sound(FRUIT)
            self.eating_ghost = pygame.mixer.Sound(EATING_GHOST)
            self.death = pygame.mixer.Sound(PAC_MAN_DEATH)
            self.tick = 0

    def play_intro(self):
        self.intro.play(loops=0)

    def eat_pallet(self):
        self.eating_pallet[self.tick].play(loops=0)
        self.tick = (self.tick + 1) % 2

    def eat_special_item(self):
        self.eatig_fruit.play()

    def pac_man_death(self):
        self.death.play(loops=0)

    def play_bg_music(self):
        pygame.mixer_music.load(BGMUSIC)
        pygame.mixer_music.play(loops=-1)

    def stop_bg_music(self):
        pygame.mixer_music.stop()
