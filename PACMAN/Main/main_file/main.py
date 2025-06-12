from PACMAN.Interface.GameController.controller import GameController
from PACMAN.Interface.GameController.LevelManager import LevelManager
"""
	Rodrigo Ureña Castillo 118910482
	Dylan ELizondo Alvarado 504610652
	Luis David Salgado Gamez 208670670
	Andrea Orozco Sanabria 119160741
"""

#========================================================

if __name__ == "__main__":
    game = GameController()
    game.main_menu()

    while True:
        game.update()