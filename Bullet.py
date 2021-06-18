from Actor import Actor
from util import POSITIONS


class Bullet:
    def __init__(self, game, pos: tuple):
        self._game = game
        game.add_bullet(self)

        self._symbol = POSITIONS["bullet"]

        self._x, self._y = pos
        self._width, self._height = self._symbol[2], self._symbol[3]

        self._dy = -10

    def symbol(self):
        return self._symbol

    def move(self):
        self._y += self._dy

    def position(self):
        return self._x, self._y, self._width, self._height

    def collide(self, other: Actor):
        self._game.remove_bullet(self)
