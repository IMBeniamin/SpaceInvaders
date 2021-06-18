import random

from Actor import Actor
from AlienBullet import AlienBullet
from Bullet import Bullet
from Player import Player
from util import POSITIONS
from lib import g2d


class Alien(Actor):
    def __init__(self, game, pos: tuple, group=None):
        if group:
            group.add(self)
        else:
            self._game = game
            game.add(self)

        self._symbol = POSITIONS["alien" + str(random.randint(1, 4))]

        self._x, self._y = pos
        self._width, self._height = self._symbol[2], self._symbol[3]

        self._dx = 1
        self._dy = 4
        self._spacing_multiplier = 30
        self._max_x = self._x + self._dx * self._spacing_multiplier
        self.mix_x = self._x - self._dx * self._spacing_multiplier

    def move(self):
        if self._max_x > self._x + self._dx > self.mix_x and self._x + self._dx < self._game.get_dims()[0]:
            self._x += self._dx
        else:
            self._dx = -self._dx
            self._y += self._dy

    def shoot(self):
        bullet = AlienBullet(self._game, (self._x+self._width//2, self._y+self._dy+15))

    def symbol(self):
        return self._symbol

    def position(self):
        return self._x, self._y, self._width, self._height

    def collide(self, other):
        if isinstance(other, Bullet) or isinstance(other, Player):
            g2d.play_audio("res/hit.wav")
            self._game.remove(self)
            self._game.increase_score(1)
