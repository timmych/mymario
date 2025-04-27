"""Module for main game"""

from dataclasses import dataclass
import sys
import random
import pygame
from data.game_object import Boss, GameObjectFactory, GameObject
from data.const_data import Constants


@dataclass
class GameObjects:
    """Game objects state"""

    player: GameObject
    objects: list
    bullets: list


@dataclass
class GameStats:
    """Game statistics and state"""

    object_spawn_timer: int
    object_spawn_interval: int
    score: int
    game_on: bool
    game_won: bool
    game_loop_counter: int


@dataclass
class GameState:
    """Current state of the game"""

    objects: GameObjects
    stats: GameStats


def create_gradient_background_2(width, height):
    """Game background support"""
    # Create a surface for the gradient
    surface = pygame.Surface((width, height))

    # Define gradient colors
    top_color = (0, 0, 50)  # Dark blue
    bottom_color = (0, 0, 100)  # Lighter blue

    # Create the gradient
    for y_pos in range(height):
        # Calculate the color at this y position
        ratio = y_pos / height
        red = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        green = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        blue = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)

        # Draw a horizontal line of this color
        pygame.draw.line(surface, (red, green, blue), (0, y_pos), (width, y_pos))

    return surface


def reset_game():
    """Reset all game variables"""
    player = GameObjectFactory.create_player(
        pos_x=(Constants.SCREEN_WIDTH - Constants.DEFAULT_PLAYER_SIZE) // 2,
        pos_y=Constants.SCREEN_HEIGHT - Constants.DEFAULT_PLAYER_SIZE - 10,
    )
    return GameState(
        objects=GameObjects(
            player=player,
            objects=[],
            bullets=[],
        ),
        stats=GameStats(
            object_spawn_timer=0,
            object_spawn_interval=5,
            score=0,
            game_on=True,
            game_won=False,
            game_loop_counter=0,
        ),
    )


def handle_input(player, bullets, game_on, is_fullscreen):
    """Handle user input"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append(
                    GameObjectFactory.create_regular_bullet(
                        pos_x=player.pos_x, pos_y=player.pos_y
                    )
                )
            elif event.key == pygame.K_x:
                bullets.append(
                    GameObjectFactory.create_penetrable_bullet(
                        pos_x=player.pos_x, pos_y=player.pos_y
                    )
                )
            elif (
                event.key == pygame.K_f and event.mod & pygame.KMOD_SHIFT
            ):  # Check for capital F
                is_fullscreen = not is_fullscreen
                return True, is_fullscreen  # Signal to toggle fullscreen
            elif not game_on and event.key == pygame.K_r:
                return True, is_fullscreen  # Signal to reset game
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
    return False, is_fullscreen  # No special action needed


def handle_player_movement(player, current_width, current_height):
    """Handle player movement based on key presses"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.pos_x = max(0, player.pos_x - 6)
    if keys[pygame.K_RIGHT]:
        player.pos_x = min(
            current_width - Constants.DEFAULT_PLAYER_SIZE, player.pos_x + 6
        )
    if keys[pygame.K_UP]:
        player.pos_y = max(0, player.pos_y - 4)
    if keys[pygame.K_DOWN]:
        player.pos_y = min(
            current_height - Constants.DEFAULT_PLAYER_SIZE, player.pos_y + 4
        )


def update_game_state(
    game_state: GameState, current_width: int, current_height: int
) -> GameState:
    """Update game state including object movement, collisions, and scoring"""
    if not game_state.stats.game_on:
        return game_state

    game_state.stats.object_spawn_timer += 1
    game_state.stats.game_loop_counter += 1

    # Spawn new objects
    if game_state.stats.object_spawn_timer == game_state.stats.object_spawn_interval:
        game_state.objects.objects.append(
            GameObjectFactory.create_angry_cat(
                pos_x=random.randint(0, current_width - Constants.DEFAULT_OBJECT_SIZE),
                pos_y=-Constants.DEFAULT_OBJECT_SIZE,
                game_loop_i=game_state.stats.game_loop_counter,
            )
        )
        game_state.stats.object_spawn_timer = 0

    # Spawn boss if needed
    if (
        game_state.stats.score > Constants.BOSS_START_SCORE
        and game_state.stats.score % Constants.BOSS_START_SCORE == 0
    ):
        game_state.objects.objects.append(
            GameObjectFactory.create_boss_cat(
                pos_x=random.randint(0, current_width - Constants.BOSS_OBJECT_SIZE),
                pos_y=-Constants.BOSS_OBJECT_SIZE,
            )
        )

    # Move objects and bullets
    for obj in game_state.objects.objects:
        obj.move()
    for blt in game_state.objects.bullets:
        blt.move()

    # Remove objects and bullets that are off screen
    game_state.objects.objects = [
        obj for obj in game_state.objects.objects if obj.pos_y < current_height
    ]
    game_state.objects.bullets = [
        blt for blt in game_state.objects.bullets if blt.pos_y < current_height
    ]

    # Handle collisions
    for blt in game_state.objects.bullets:
        for obj in game_state.objects.objects:
            blt.check_collide_and_hit_if_so(obj)

    # Check for boss defeat
    bosses = [obj for obj in game_state.objects.objects if isinstance(obj, Boss)]
    game_state.stats.game_won = len(bosses) > 0 and any(b.dead() for b in bosses)
    if game_state.stats.game_won:
        game_state.stats.game_on = False
        return game_state

    # Remove dead objects and bullets
    game_state.objects.objects = [
        obj for obj in game_state.objects.objects if not obj.dead()
    ]
    game_state.objects.bullets = [
        blt for blt in game_state.objects.bullets if not blt.dead()
    ]

    # Check player collision
    for obj in game_state.objects.objects:
        if obj.check_collide(game_state.objects.player):
            game_state.stats.game_on = False
            return game_state

    # Update score
    game_state.stats.score += 1

    return game_state


def draw_game(screen, game_state: GameState):
    """Draw all game elements"""
    # Draw player and objects
    screen.blit(
        game_state.objects.player.surface,
        (game_state.objects.player.pos_x, game_state.objects.player.pos_y),
    )
    for obj in game_state.objects.objects:
        screen.blit(obj.surface, obj.pos())
    for blt in game_state.objects.bullets:
        screen.blit(blt.surface, blt.pos())

    # Draw score
    score_font = pygame.font.Font(None, 48)
    score_text = score_font.render(
        f"Score: {game_state.stats.score}", True, Constants.WHITE
    )
    score_rect = score_text.get_rect(topleft=(10, 10))
    pygame.draw.rect(screen, (0, 0, 0, 128), score_rect.inflate(20, 10))
    screen.blit(score_text, score_rect)

    # Draw game over screen if needed
    if not game_state.stats.game_on:
        show_game_end(screen, game_state.stats.game_won, game_state.stats.score)


def main():
    """Game main"""
    pygame.init()

    # Current screen dimensions (initially set to default constants)
    current_width = Constants.SCREEN_WIDTH
    current_height = Constants.SCREEN_HEIGHT

    # Create the screen
    screen = pygame.display.set_mode((current_width, current_height))
    pygame.display.set_caption("Henny Steel Rabbit vs Angry Cat")

    # Fullscreen state
    is_fullscreen = False

    # Create gradient background
    background = pygame.image.load("images/back.png")
    background = pygame.transform.scale(background, (current_width, current_height))

    # Initialize game variables
    game_state = reset_game()

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        # Draw gradient background
        screen.blit(background, (0, 0))

        # Handle input
        should_reset, is_fullscreen = handle_input(
            game_state.objects.player,
            game_state.objects.bullets,
            game_state.stats.game_on,
            is_fullscreen,
        )
        if should_reset:
            if is_fullscreen:
                screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                current_width = screen.get_width()
                current_height = screen.get_height()
                background = pygame.transform.scale(
                    background, (current_width, current_height)
                )
                game_state = reset_game()
            else:
                current_width = Constants.SCREEN_WIDTH
                current_height = Constants.SCREEN_HEIGHT
                screen = pygame.display.set_mode((current_width, current_height))
                background = pygame.transform.scale(
                    background, (current_width, current_height)
                )
                game_state = reset_game()

        # Handle player movement
        handle_player_movement(game_state.objects.player, current_width, current_height)

        # Update game state
        game_state = update_game_state(game_state, current_width, current_height)

        # Draw everything
        draw_game(screen, game_state)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(Constants.FPS)


def show_game_end(screen, game_won, score):
    """Game end prompt support"""
    # Create a semi-transparent overlay
    overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(overlay, (0, 0))

    # Main message
    font = pygame.font.Font(None, 80)
    win_msg = "YOU WIN!" if game_won else "You lost :("
    score_text = font.render(
        f"{win_msg} Score: {score}",
        True,
        Constants.GREEN if game_won else Constants.RED,
    )
    text_rect = score_text.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2 - 100)
    )
    screen.blit(score_text, text_rect)

    # Add restart instruction
    restart_font = pygame.font.Font(None, 36)
    restart_text = restart_font.render("Press 'R' to restart", True, Constants.WHITE)
    restart_rect = restart_text.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2 + 50)
    )
    screen.blit(restart_text, restart_rect)

    # Add quit instruction
    quit_text = restart_font.render("Press 'Q' to quit", True, Constants.WHITE)
    quit_rect = quit_text.get_rect(
        center=(screen.get_width() / 2, screen.get_height() / 2 + 100)
    )
    screen.blit(quit_text, quit_rect)


if __name__ == "__main__":
    main()
