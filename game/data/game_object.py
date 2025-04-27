"""Game Object Models"""

import random
import pygame
from data.const_data import Constants
from pygame.surface import Surface

ANGRY_CAT_COUNT = 4
angry_images = []
for i in range(ANGRY_CAT_COUNT):
    angry_images.append(pygame.image.load(f"images/angrypongpong{i}.png"))

player_image = pygame.image.load("images/hennysteel.png")
boss_cat_image = pygame.image.load("images/big_angry_cat.png")


class GameObject:
    """Base class for objects in the game"""

    x: int
    y: int
    size: int
    speed: int
    surface: Surface
    health: int

    def __init__(
        self,
        x,
        y,
        size=Constants.DEFAULT_OBJECT_SIZE,
        speed=Constants.DEFAULT_OBJECT_SPEED,
        surface=None,
        health=1,
    ):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.surface = surface
        self.health = health

    def pos(self):
        """Return the object position"""
        return (self.x, self.y)

    def move(self):
        """Move the object"""
        self.y += self.speed

    def check_collide(self, another_object) -> bool:
        """Check if it's colliding with another object"""
        pos = another_object.pos()
        return (
            pos[0] < self.x + self.size
            and pos[0] + another_object.size > self.x
            and pos[1] < self.y + self.size
            and pos[1] + another_object.size > self.y
        )

    def check_collide_and_hit_if_so(self, another_object) -> bool:
        """Check if it's colliding with another object; will also hit the object if so"""
        checked = self.check_collide(another_object)
        if checked:
            self.hit()
            another_object.hit()
        return checked

    def hit(self) -> int:
        """Take a hit and reduce health by one"""
        self.health -= 1
        return self.health

    def dead(self) -> bool:
        """Returns whether health has gone to zero or less"""
        return self.health < 1


class Bullet(GameObject):
    """Game object: Bullet"""

    def __init__(self, x, y, penetrable, surface):
        super().__init__(
            x,
            y,
            size=Constants.DEFAULT_BULLET_SIZE,
            speed=-Constants.DEFAULT_BULLET_SPEED,
            surface=surface,
            health=9999 if penetrable else 1,
        )


class Boss(GameObject):
    """Game object: Boss"""

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            size=Constants.BOSS_OBJECT_SIZE,
            surface=boss_cat_image,
            speed=Constants.DEFAULT_OBJECT_SPEED * 0.5,
            health=Constants.BOSS_OBJECT_HEALTH,
        )


class GameObjectFactory:
    """Game object factory for creation of standard objects"""

    REGULAR_BULLET_SURFACE = pygame.image.load("images/carrot.png")
    PENETRABLE_BULLET_SURFACE = pygame.image.load("images/mango.png")

    @staticmethod
    def create_regular_bullet(x, y) -> Bullet:
        """Create regular bullet"""
        return Bullet(x, y, False, GameObjectFactory.REGULAR_BULLET_SURFACE)

    @staticmethod
    def create_penetrable_bullet(x, y) -> Bullet:
        """Create penetrable bullet that goes through other objects"""
        return Bullet(x, y, True, GameObjectFactory.PENETRABLE_BULLET_SURFACE)

    @staticmethod
    def create_angry_cat(x, y, game_loop_i) -> GameObject:
        """Create an angry cat object"""
        new_obj_image = angry_images[random.randint(0, ANGRY_CAT_COUNT - 1)]
        return GameObject(
            x=x,
            y=y,
            size=Constants.DEFAULT_OBJECT_SIZE,
            surface=new_obj_image,
            speed=Constants.DEFAULT_OBJECT_SPEED
            - 1
            + random.randint(0, 2) * (1 + game_loop_i / 200.0),
        )

    @staticmethod
    def create_player(x, y) -> GameObject:
        """Create the main player"""
        return GameObject(
            x=x, y=y, size=Constants.DEFAULT_PLAYER_SIZE, surface=player_image, speed=0
        )

    @staticmethod
    def create_boss_cat(x, y) -> Boss:
        """Create boss"""
        return Boss(x, y)
