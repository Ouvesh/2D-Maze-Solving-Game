import pygame

from game_object import GameObject


class Image(GameObject):
    def __init__(self, *, centre_x=None, centre_y=None, width=None, height=None, x=None, y=None, game, image_path):
        super().__init__(x=x, y=y, game=game, width=width, height=height)
        self.image = pygame.image.load(image_path)
        self.width = width or self.image.get_width()
        self.height = height or self.image.get_height()
        print(centre_x, x)
        self.x = x if x is not None else (centre_x - self.width // 2)
        self.y = y if y is not None else (centre_y - self.height // 2)
        self.centre_x = centre_x if centre_x is not None else (self.x + self.width // 2)
        self.centre_y = centre_y if centre_y is not None else (self.y + self.height // 2)
        if width or height:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self):
        self.game.screen.blit(self.image, self.get_rect())


