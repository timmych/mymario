import random
from typing import Tuple
import pygame
from pygame.surface import Surface
from data.const_data import Constants

ANGRY_CAT_COUNT = 4
angry_images = []
for i in range(ANGRY_CAT_COUNT):
    angry_images.append(pygame.image.load(f"images/angrypongpong{i}.png"))


class GameObject:
    x: int
    y: int
    size: int
    speed: int
    surface: Surface

    def __init__(
        self,
        x,
        y,
        size=Constants.DEFAULT_OBJECT_SIZE,
        speed=Constants.DEFAULT_OBJECT_SPEED,
        surface=None,
    ):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.surface = surface

    def pos(self):
        return (self.x, self.y)

    def move(self):
        self.y += self.speed

    # returns True if colliding with the input object
    def check_collide(self, pos: Tuple[int, int], size: Tuple[int, int]) -> bool:
        return (
            pos[0] < self.x + self.size
            and pos[0] + size[0] > self.x
            and pos[1] < self.y + self.size
            and pos[1] + size[1] > self.y
        )


class Bullet(GameObject):
    penetrable: bool

    def __init__(self, x, y, penetrable, surface):
        super().__init__(
            x,
            y,
            size=Constants.DEFAULT_BULLET_SIZE,
            speed=-Constants.DEFAULT_BULLET_SPEED,
            surface=surface,
        )
        self.penetrable = penetrable

    def can_penetrate(self) -> bool:
        return self.penetrable


class GameObjectFactory:
    REGULAR_BULLET_SURFACE = pygame.image.load("images/carrot.png")
    PENETRABLE_BULLET_SURFACE = pygame.image.load("images/mango.png")

    @staticmethod
    def create_regular_bullet(x, y) -> Bullet:
        return Bullet(x, y, False, GameObjectFactory.REGULAR_BULLET_SURFACE)

    @staticmethod
    def create_penetrable_bullet(x, y) -> Bullet:
        return Bullet(x, y, True, GameObjectFactory.PENETRABLE_BULLET_SURFACE)

    @staticmethod
    def create_angry_cat(x, y, game_loop_i) -> GameObject:
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
