import pygame
from pygame.surface import Surface

DEFAULT_OBJECT_SIZE = 40
DEFAULT_OBJECT_COLOR = (255, 255, 0)
DEFAULT_OBJECT_SPEED = 4
DEFAULT_OBJECT_SURFACE = pygame.Surface((DEFAULT_OBJECT_SIZE, DEFAULT_OBJECT_SIZE))
DEFAULT_OBJECT_SURFACE.fill(DEFAULT_OBJECT_COLOR)


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
        size=DEFAULT_OBJECT_SIZE,
        speed=DEFAULT_OBJECT_SPEED,
        surface=DEFAULT_OBJECT_SURFACE,
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
    def check_collide(self, pos, size):
        return (
            pos[0] < self.x + self.size
            and pos[0] + size[0] > self.x
            and pos[1] < self.y + self.size
            and pos[1] + size[1] > self.y
        )
