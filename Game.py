import random
import sys
from time import sleep

from AlienBullet import AlienBullet
from lib import g2d
from Actor import Actor
from Alien import Alien
from Obstacle import Obstacle
from util import POSITIONS


class Game:
    def __init__(self, dim: tuple):
        self._w, self._h = dim

        self.actors = list()
        self.bullets = list()
        self._obstacles = list()
        self.player = None

        self.score = 0

        g2d.init_canvas((self._w, self._h))

        # obstacles initialization
        for x in range(0 + POSITIONS["obstacle6"][2], self._w - POSITIONS["obstacle6"][2] + 1, self._w // 7):
            Obstacle(self, (x, 500))

    def tick(self):
        g2d.clear_canvas()

        if self.player.health <= 0:
            self.bullets.clear()
            self.actors.clear()
            self.player = None
            self._obstacles.clear()
            go_dims = POSITIONS["game_over"]
            g2d.draw_image_clip(
                                "res/game_over.png",
                                go_dims,
                                (self._w//2-go_dims[2]//2, self._h//2-go_dims[3]//2, go_dims[2], go_dims[3])
                                )
            g2d.confirm("quit?")
            g2d.close_canvas()
            sys.exit()

        g2d.draw_text(f"Health: {str(self.player.health)}", (200, 40), 30)
        g2d.draw_text(f"Score: {str(self.score)}", (200, 80), 30)

        if not self.actors:
            for y in range(200, 350, 50):
                self.spawn_aliens(y, False)
        if not random.randint(0, (1000 // (self.score + 20))):
            self.spawn_aliens(150)

        # player actor
        # self.player.control(g2d.pressed_keys(), g2d.released_keys())
        self.player.control(g2d.pressed_keys(), g2d.released_keys())
        self.player.move()
        g2d.draw_image_clip("res/assets.png", self.player.symbol(), self.player.position())

        # temporary actors (bullets, particles)
        # checks if the temporary actors are still in game
        for bullet in self.bullets:
            if not self.in_game(bullet):
                self.remove_bullet(bullet)
        for bullet in self.bullets:
            bullet.move()
            g2d.draw_image_clip("res/assets.png", bullet.symbol(), bullet.position())

        # main actors (aliens, enemies)
        for actor in self.actors + self._obstacles:
            actor.move()
            g2d.draw_image_clip("res/assets.png", actor.symbol(), actor.position())

        # spawns bullets randomly
        if not random.randint(0, 10):
            random.choice(self.actors).shoot()

        # checks for collisions and calls the corresponding methods
        for actor in self.bullets + [self.player] + self._obstacles:
            for other_actor in self.actors + [self.player] + self._obstacles:
                if actor is not other_actor and self.check_collision(actor, other_actor):
                    # print("{actor.position()} has collided with {other_actor.position()}")
                    if isinstance(actor, Alien) and isinstance(other_actor, AlienBullet):
                        pass
                    actor.collide(other_actor)
                    other_actor.collide(actor)

    def get_dims(self) -> tuple:
        return self._w, self._h

    def spawn_aliens(self, y, check: bool = True):
        if check:
            for actor in self.actors:
                if y - 30 < actor.position()[1] < y + 30:
                    return
        [Alien(self, (x, y)) for x in range(100, self._w - 40, self._w // 8)]

    def check_collision(self, a1: Actor, a2: Actor) -> bool:
        """Check the two actors (args) for mutual collision (bounding-box
        collision detection). Return True if colliding, False otherwise
        """
        x1, y1, w1, h1 = a1.position()
        x2, y2, w2, h2 = a2.position()
        return (y2 < y1 + h1 and y1 < y2 + h2
                and x2 < x1 + w1 and x1 < x2 + w2)

    def add(self, actor: Actor):
        self.actors.append(actor)

    def add_bullet(self, actor: Actor):
        self.bullets.append(actor)

    def add_player(self, actor: Actor):
        self.player = actor

    def add_obstacle(self, obstacle):
        self._obstacles.append(obstacle)

    def remove(self, actor):
        if actor in self.actors:
            self.actors.remove(actor)

    def remove_bullet(self, actor: Actor):
        self.bullets.remove(actor)

    def remove_obstacle(self, obstacle):
        if obstacle in self._obstacles:
            self._obstacles.remove(obstacle)

    def run(self):
        g2d.main_loop(self.tick, 60)

    def in_game(self, actor: Actor) -> bool:
        return actor.position()[0] > 0 \
               and actor.position()[0] + actor.position()[2] < self._w \
               and actor.position()[1] > 0 \
               and actor.position()[1] + actor.position()[3] < self._h

    def in_game_coord(self, pos: tuple):
        x, y, w, h = pos
        return x > 0 and x + w < self._w and y > 0 and y + h < self._h

    def increase_score(self, points):
        self.score += points
