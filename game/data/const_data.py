"""Game constant data module"""


# pylint: disable=too-few-public-methods
class Constants:
    """Constants data holder"""

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    FPS = 60

    DEFAULT_OBJECT_SIZE = 40
    DEFAULT_OBJECT_COLOR = (255, 255, 0)
    DEFAULT_OBJECT_SPEED = 4
    DEFAULT_BULLET_SIZE = 30
    DEFAULT_BULLET_SPEED = 8
    DEFAULT_PLAYER_SIZE = 40

    BOSS_OBJECT_SIZE = 400
    BOSS_OBJECT_HEALTH = 20
    BOSS_START_SCORE = 400

    # Colors
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
