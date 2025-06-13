import pygame

from game_object import GameObject
from image import Image


class Button(GameObject):
    def __init__(self, *, image_path, x=None, y=None, width=None, height=None, game, centre_x=None, centre_y=None):
        """
        :param image_path: file path
        :param x:
        :param y:
        :param width:
        :param height:
        :param game:
        """
        super().__init__(x=y, y=y, game=game, width=width, height=height, colour=(0, 0, 0))

        self.image = Image(image_path=image_path, x=x, y=y, game=game, centre_y=centre_y, centre_x=centre_x)

        self.width = width or self.image.width
        self.height = height or self.image.height
        self.clicked = False
        self.rect = self.image.get_rect()
        self.centre_x = centre_x
        self.centre_y = centre_y
        self.x = x if x is not None else (self.centre_x - self.width//2)
        self.y = y if y is not None else (self.centre_y - self.height//2)

    def draw(self):
        self.image.draw()

    def check_button_pressed(self):
        pos = pygame.mouse.get_pos()

        if self.get_rect().collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

        return False

