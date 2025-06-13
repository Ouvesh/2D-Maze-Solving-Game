# moving_object.py
from game_object import GameObject
import pygame


class MovingObject(GameObject):
    def __init__(self, *, width, height, x, y, game, dx, dy, colour):
        super().__init__(x=x, y=y, game=game, colour=colour, width=width, height=height)
        self.starting_y = y
        self.starting_x = x
        self.dx = dx
        self.dy = dy

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def next_position(self):
        return pygame.Rect(self.x + self.dx, self.y + self.dy, self.width, self.height)

    def going_to_collide(self, game_object):
        return self.next_position().colliderect(game_object.get_rect())

    def reset_to_start(self):
        self.x = self.starting_x
        self.y = self.starting_y



