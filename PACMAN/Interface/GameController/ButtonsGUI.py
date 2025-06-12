import os
import pygame
from PACMAN.Interface.constants import *

# Rect(left, top, width, height)
FONT_PATH = "../../../resource/font/Tiny5-Regular.ttf"

# Configuración de colores y parámetros de botones
button_color = (50, 50, 150)
button_hover_color = (150, 80, 150)
# Configuración de animación de fondo
ANIMATION_FOLDER = "../../../resource/animation/anim/"
ANIMATION_FOLDER2 = "../../../resource/animation/anim2/"
animation_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(ANIMATION_FOLDER, frame)), (SCREEN_WIDTH, SCREEN_HEIGHT))
    for frame in sorted(os.listdir(ANIMATION_FOLDER))
]

animation_frames2 = [
    pygame.transform.scale(pygame.image.load(os.path.join(ANIMATION_FOLDER2, frame)), (SCREEN_WIDTH, SCREEN_HEIGHT))
    for frame in sorted(os.listdir(ANIMATION_FOLDER2))
]

frame_index = 0
frame_index2 = 0
animation_speed = 0.018
animation_speed2 = 0.03

# Imagen de fondo para el menú principal
image_main_menu = pygame.transform.scale(pygame.image.load("../../../resource/animation/pacman.jpg"),
                                         (SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()


# Función para dibujar botones con hover y texto
def draw_button(screen, button, text, font, is_hovered, color, hover_color, text_color=WHITE):
    button_color = hover_color if is_hovered else color
    pygame.draw.rect(screen, button_color, button)
    text_render = font.render(text, True, text_color)
    screen.blit(text_render, (button.x + (button.width - text_render.get_width()) / 2,
                              button.y + (button.height - text_render.get_height()) / 2))


# Función de animación de fondo
def animate_background(screen, frames, frame_index, animation_speed):
    screen.blit(frames[int(frame_index)], (0, 0))
    return (frame_index + animation_speed) % len(frames)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clock.tick(120)
            return event
    return None

# Menú principal
def main_menu(screen):
    clock.tick(60)
    font_Tittle = pygame.font.Font(FONT_PATH, 92)
    font = pygame.font.Font(FONT_PATH, 48)
    screen.fill((150, 250, 150))
    screen.blit(image_main_menu, (0, 0))
    title_text = font_Tittle.render("PAC-MAN", True, (231, 51, 11))
    screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 180))
    new_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 300, 300, 50)
    load_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 400, 300, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 500, 300, 50)

    global frame_index
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for button, text in [(new_game_button, "New Game"), (load_game_button, "Load Game"), (quit_button, "Exit")]:
            draw_button(screen, button, text, font, button.collidepoint(mouse_pos), button_color, button_hover_color)

        pygame.display.update()

        event = handle_events()
        if event:
            if new_game_button.collidepoint(event.pos):
                clock.tick(120)
                return "new_game"
            elif load_game_button.collidepoint(event.pos):
                clock.tick(120)
                return "load_game"
            elif quit_button.collidepoint(event.pos):
                exit()

# Menú de guardado
def save_game(screen):
    clock.tick(60)
    font = pygame.font.Font(FONT_PATH, 48)
    font_title = pygame.font.Font(FONT_PATH, 92)
    title_text = font_title.render("PAC-MAN", True, ORANGE)
    save_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 300, 300, 50)
    dont_save_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 400, 300, 50)
    back_button = pygame.Rect(SCREEN_WIDTH / 2 - 150, 500, 300, 50)
    color = (255,110,50)
    hover_color = (205,105,30)
    global frame_index
    while True:
        frame_index = animate_background(screen, animation_frames, frame_index, animation_speed)

        screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 25))
        mouse_pos = pygame.mouse.get_pos()
        for button, text in [(save_button, "Save Game"), (dont_save_button, "Don't Save"), (back_button, "Back")]:
            draw_button(screen, button, text, font, button.collidepoint(mouse_pos), color, hover_color)

        pygame.display.update()

        event = handle_events()
        if event:
            if save_button.collidepoint(event.pos):
                return "save_game"
            elif dont_save_button.collidepoint(event.pos):
                return "dont_save"
            elif back_button.collidepoint(event.pos):
                clock.tick(120)
                return "back"

# Menú de pausa
def pause_game(screen):
    clock.tick(60)
    font = pygame.font.Font(FONT_PATH, 48)
    font_title = pygame.font.Font(FONT_PATH, 72)
    title_text = font_title.render("PAUSE", True, YELLOW)
    continue_game_button = pygame.Rect(SCREEN_WIDTH / 2 - 300, SCREEN_HEIGHT - 100, 250, 50)
    exit_button = pygame.Rect(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 100, 250, 50)

    global frame_index2
    while True:
        frame_index2 = animate_background(screen, animation_frames2, frame_index2, animation_speed2)

        screen.blit(title_text, (SCREEN_WIDTH / 2 - title_text.get_width() / 2, 50))
        mouse_pos = pygame.mouse.get_pos()
        for button, text in [(continue_game_button, "Continue"), (exit_button, "Exit")]:
            draw_button(screen, button, text, font, button.collidepoint(mouse_pos), button_color, button_hover_color)

        pygame.display.update()
        event = handle_events()
        if event:
            if continue_game_button.collidepoint(event.pos):
                clock.tick(120)
                return "continue_game"
            elif exit_button.collidepoint(event.pos):
                return "exit"