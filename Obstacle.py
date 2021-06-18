from Actor import Actor
from util import POSITIONS


class Obstacle(Actor):
    def __init__(self, game, pos: tuple):
        self._x, self._y = pos
        self._health = 6
        self._symbol = POSITIONS["obstacle" + str(self._health)]
        self._game = game

        self._game.add_obstacle(self)

        self._width, self._height = self._symbol[2:]

    def symbol(self) -> (int, int, int, int):
        return self._symbol

    def _update_symbol(self) -> (int, int, int, int):
        if self._health > 0:
            self._symbol = POSITIONS["obstacle" + str(self._health)]

    def move(self):
        pass

    def position(self) -> (int, int, int, int):
        return self._x, self._y, self._width, self._height

    def collide(self, other):
        if self._health > 0:
            self._health -= 1
            self._update_symbol()
        else:
            self._game.remove_obstacle(self)
