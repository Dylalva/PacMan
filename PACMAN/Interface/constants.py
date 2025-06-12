#  constants that will be used to the graphic interface and graphs management
import enum

#  screen constants
TILE_WIDTH = 16
TILE_HEIGHT = 16
NROWS = 36
NCOLS = 28
SCREEN_WIDTH = NCOLS * TILE_WIDTH + TILE_WIDTH + 500
SCREEN_HEIGHT = NROWS * TILE_HEIGHT + TILE_HEIGHT + 100
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 125)
WHITE = (255, 255, 255)
PINK = (255, 205, 255)
SKY_BLUE = (0, 221, 221)
ORANGE = (255, 175, 0)
RED = (255, 0, 0)

MAZE_COLORS = [BLUE, SKY_BLUE, PINK, ORANGE]

#  node directions
UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"
PORTAL = "portal"
#  pacman stop
STOP = "stop"

# SPECIAL NODES

GATE = "="

# characters identificators
PACMAN = "P"
BLINKY = "B"
PINKY = "Y"
INKY = "I"
CLYDE = "C"

INVICIBLE_NODES = [PINKY, INKY, CLYDE]
# characters size
C_SIZE = (32, 32)
G_SIZE = (44, 44)
def opposite(direction):
    if direction == UP:
        return DOWN
    elif direction == DOWN:
        return UP
    elif direction == RIGHT:
        return LEFT
    elif direction == LEFT:
        return RIGHT
    return None

