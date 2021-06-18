from lib import g2d

from Actor import Actor
from util import POSITIONS
from Bullet import Bullet


class Player(Actor):
    def __init__(self, game, pos: tuple):
        self._game = game
        game.add_player(self)

        self.health = 100.0
        self._speed = 5

        self._symbol = POSITIONS["player"]

        self._x, self._y = pos
        self._width, self._height = self._symbol[2], self._symbol[3]

        self._dx = self._dy = 0

    def symbol(self):
        return self._symbol

    def move(self):
        if not (
                self._x + self._dx + self._width > self._game.get_dims()[0]
                or self._x + self._dx < 0
                or self._y + self._dy + self._height > self._game.get_dims()[1]
                or self._y + self._dy < 0
                ):
            self._x += self._dx
            self._y += self._dy

    def position(self):
        return self._x, self._y, self._width, self._height

    def shoot(self):
        g2d.play_audio("res/gunshot.wav")
        Bullet(self._game, (self._x + self._width // 2, self._y-15))

    def control(self, pressed, released):
        u, d, l, r, shoot = "w", "s", "a", "d", "Spacebar"
        if shoot in pressed:
            self.shoot()
        if u in pressed:
            self._dy = -self._speed
        if d in pressed:
            self._dy = self._speed
        if l in pressed:
            self._dx = -self._speed
        if r in pressed:
            self._dx = self._speed
        if u in released and self._dy < 0:
            self._dy = 0
        if d in released and self._dy > 0:
            self._dy = 0
        if l in released and self._dx < 0:
            self._dx = 0
        if r in released and self._dx > 0:
            self._dx = 0

    def hurt(self, amount):
        self.health -= amount

    def collide(self, other):
        if isinstance(other, Bullet):
            self.hurt(5)
        else:
            self.hurt(10)
