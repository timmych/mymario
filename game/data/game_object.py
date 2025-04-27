"""Game Object Models"""

from dataclasses import dataclass
from typing import Optional
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


@dataclass
class GameObjectConfig:
    """Configuration for game objects"""

    size: int = Constants.DEFAULT_OBJECT_SIZE
    speed: float = Constants.DEFAULT_OBJECT_SPEED
    surface: Optional[pygame.Surface] = None
    health: int = 1


class GameObject:
    """Base class for objects in the game"""

    pos_x: int
    pos_y: int
    size: int
    speed: float
    surface: Optional[pygame.Surface]
    health: int

    def __init__(
        self,
        pos_x: int,
        pos_y: int,
        config: Optional[GameObjectConfig] = None,
    ):
        self.pos_x = pos_x
        self.pos_y = pos_y
        if config is None:
            config = GameObjectConfig()
        self.size = config.size
        self.speed = config.speed
        self.surface = config.surface
        self.health = config.health

    def pos(self):
        """Return the object position"""
        return (self.pos_x, self.pos_y)

    def move(self):
        """Move the object"""
        self.pos_y += self.speed

    def check_collide(self, another_object) -> bool:
        """Check if it's colliding with another object"""
        pos = another_object.pos()
        return (
            pos[0] < self.pos_x + self.size
            and pos[0] + another_object.size > self.pos_x
            and pos[1] < self.pos_y + self.size
            and pos[1] + another_object.size > self.pos_y
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

    def __init__(
        self, pos_x: int, pos_y: int, penetrable: bool, surface: pygame.Surface
    ):
        config = GameObjectConfig(
            size=Constants.DEFAULT_BULLET_SIZE,
            speed=-Constants.DEFAULT_BULLET_SPEED,
            surface=surface,
            health=9999 if penetrable else 1,
        )
        super().__init__(pos_x, pos_y, config)


class Boss(GameObject):
    """Game object: Boss"""

    def __init__(self, pos_x: int, pos_y: int):
        config = GameObjectConfig(
            size=Constants.BOSS_OBJECT_SIZE,
            surface=boss_cat_image,
            speed=Constants.DEFAULT_OBJECT_SPEED * 0.5,
            health=Constants.BOSS_OBJECT_HEALTH,
        )
        super().__init__(pos_x, pos_y, config)


class GameObjectFactory:
    """Game object factory for creation of standard objects"""

    REGULAR_BULLET_SURFACE = pygame.image.load("images/carrot.png")
    PENETRABLE_BULLET_SURFACE = pygame.image.load("images/mango.png")

    @staticmethod
    def create_regular_bullet(pos_x: int, pos_y: int) -> Bullet:
        """Create regular bullet"""
        return Bullet(pos_x, pos_y, False, GameObjectFactory.REGULAR_BULLET_SURFACE)

    @staticmethod
    def create_penetrable_bullet(pos_x: int, pos_y: int) -> Bullet:
        """Create penetrable bullet that goes through other objects"""
        return Bullet(pos_x, pos_y, True, GameObjectFactory.PENETRABLE_BULLET_SURFACE)

    @staticmethod
    def create_angry_cat(pos_x: int, pos_y: int, game_loop_i: int) -> GameObject:
        """Create an angry cat object"""
        new_obj_image = angry_images[random.randint(0, ANGRY_CAT_COUNT - 1)]
        config = GameObjectConfig(
            surface=new_obj_image,
            speed=Constants.DEFAULT_OBJECT_SPEED
            - 1
            + random.randint(0, 2) * (1 + game_loop_i / 200.0),
        )
        return GameObject(pos_x, pos_y, config)

    @staticmethod
    def create_player(pos_x: int, pos_y: int) -> GameObject:
        """Create the main player"""
        config = GameObjectConfig(
            size=Constants.DEFAULT_PLAYER_SIZE,
            surface=player_image,
            speed=0,
        )
        return GameObject(pos_x, pos_y, config)

    @staticmethod
    def create_boss_cat(pos_x: int, pos_y: int) -> Boss:
        """Create boss"""
        return Boss(pos_x, pos_y)
