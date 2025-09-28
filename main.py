
import pygame
import sys
import math
import os

from game import Game
from tilemap import TileMap

pygame.init()

if __name__ == "__main__":
    game = Game()
    game.run()