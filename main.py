# main.py
from game import *

pygame.init()
height = 800
width = 800
screen = pygame.display.set_mode((width, height))



n = 25

game = Game(n, screen, width, height)
game.run()


