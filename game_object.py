# game_object.py
import pygame


class GameObject:
    def __init__(self, *, x, y, game, colour=(0, 0, 0), width, height):
        self.x = x
        self.y = y
        self.game = game
        self.colour = colour
        self.width = width
        self.height = height

    def draw(self):
        pygame.draw.rect(self.game.screen, self.colour,
                         (self.x + self.game.offset_x, self.y + self.game.offset_y,
                          self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_collided(self, game_object):
        return game_object.get_rect().colliderect(self.get_rect())



