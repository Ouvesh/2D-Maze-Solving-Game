# coin.py
import random
import pygame.draw

from game_object import GameObject


def choose_random_nodes(n, total_nodes):
    nodes = []
    for i in range(n):
        node = random.randint(1, total_nodes)
        while node in nodes:
            node = random.randint(1, total_nodes)
        nodes.append(node)
    return nodes


class Coin(GameObject):
    def __init__(self, *, width, height, x, y, game):
        super().__init__(x=x, y=y, game=game, colour=(255, 255, 0), width=width, height=height)

    def draw(self):
        pygame.draw.circle(self.game.screen, self.colour, (self.x + self.game.offset_x, self.y + self.game.offset_y), self.game.SMALL_COIN_SIZE//2)



