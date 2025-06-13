# enemy.py
import random
from moving_object import MovingObject


class Enemy(MovingObject):
    def __init__(self, *, width, height, x, y, game):
        super().__init__(x=x, y=y, game=game, colour=(255, 0, 0), width=width, height=height, dx=game.MOVE_AMOUNT * 1, dy=game.MOVE_AMOUNT * 1)
        self.direction_y = None
        self.direction_x = None
        self.change_direction()

    def change_direction(self):
        self.direction_x = 0
        self.direction_y = 0
        while self.direction_x == 0 and self.direction_y == 0:
            self.direction_x = random.choice([-1, 0, 1])
            self.direction_y = random.choice([-1, 0, 1])
        self.dx = self.direction_x * self.game.MOVE_AMOUNT * 1
        self.dy = self.direction_y * self.game.MOVE_AMOUNT * 1


