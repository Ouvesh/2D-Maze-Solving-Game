# player.py
from moving_object import MovingObject


class Player(MovingObject):
    def __init__(self,*, width, height, x, y, game, dx=0, dy=0):
        super().__init__(x=x, y=y, game=game, colour=(0, 0, 255), width=width, height=height, dy=dy, dx=dx)
        self.lives = 3

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def is_alive(self):
        return self.lives > 0
