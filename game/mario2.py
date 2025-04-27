"""Module for main game"""

import sys
import random
import pygame
from data.game_object import Boss, GameObjectFactory
from data.const_data import Constants


def create_gradient_background_2(width, height):
    """Game background support"""

    # Create a surface for the gradient
    surface = pygame.Surface((width, height))

    # Define gradient colors
    top_color = (0, 0, 50)  # Dark blue
    bottom_color = (0, 0, 100)  # Lighter blue

    # Create the gradient
    for y in range(height):
        # Calculate the color at this y position
        ratio = y / height
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)

        # Draw a horizontal line of this color
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

    return surface


def reset_game():
    """Reset all game variables"""

    player = GameObjectFactory.create_player(
        x=(Constants.SCREEN_WIDTH - Constants.DEFAULT_PLAYER_SIZE) // 2,
        y=Constants.SCREEN_HEIGHT - Constants.DEFAULT_PLAYER_SIZE - 10,
    )
    objects = []
    bullets = []
    object_spawn_timer = 0
    object_spawn_interval = 5
    score = 0
    game_on = True
    game_won = False
    game_loop_counter = 0
    return (
        player,
        objects,
        bullets,
        object_spawn_timer,
        object_spawn_interval,
        score,
        game_on,
        game_won,
        game_loop_counter,
    )


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
    # Scale background to match current screen dimensions
    background = pygame.transform.scale(background, (current_width, current_height))

    # Initialize game variables
    (
        player,
        objects,
        bullets,
        object_spawn_timer,
        object_spawn_interval,
        score,
        game_on,
        game_won,
        game_loop_counter,
    ) = reset_game()

    # Score variables
    score_font = pygame.font.Font(None, 48)  # Larger font for score

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    # Main game loop
    while True:
        # Draw gradient background
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(
                        GameObjectFactory.create_regular_bullet(x=player.x, y=player.y)
                    )
                elif event.key == pygame.K_x:
                    bullets.append(
                        GameObjectFactory.create_penetrable_bullet(
                            x=player.x, y=player.y
                        )
                    )
                elif event.key == pygame.K_f:
                    # Toggle fullscreen
                    is_fullscreen = not is_fullscreen
                    if is_fullscreen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        # Update current screen dimensions
                        current_width = screen.get_width()
                        current_height = screen.get_height()
                        # Scale background to match new dimensions
                        background = pygame.transform.scale(
                            background, (current_width, current_height)
                        )
                        # Reset game to use new dimensions
                        (
                            player,
                            objects,
                            bullets,
                            object_spawn_timer,
                            object_spawn_interval,
                            score,
                            game_on,
                            game_won,
                            game_loop_counter,
                        ) = reset_game()
                    else:
                        # Reset to default windowed dimensions
                        current_width = Constants.SCREEN_WIDTH
                        current_height = Constants.SCREEN_HEIGHT
                        screen = pygame.display.set_mode(
                            (current_width, current_height)
                        )
                        # Scale background to match new dimensions
                        background = pygame.transform.scale(
                            background, (current_width, current_height)
                        )
                        # Reset game to use new dimensions
                        (
                            player,
                            objects,
                            bullets,
                            object_spawn_timer,
                            object_spawn_interval,
                            score,
                            game_on,
                            game_won,
                            game_loop_counter,
                        ) = reset_game()
                elif not game_on and event.key == pygame.K_r:
                    # Reset game when game is over
                    (
                        player,
                        objects,
                        bullets,
                        object_spawn_timer,
                        object_spawn_interval,
                        score,
                        game_on,
                        game_won,
                        game_loop_counter,
                    ) = reset_game()
                elif event.key == pygame.K_q:
                    # Quit the game
                    pygame.quit()
                    sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= 6
        if (
            keys[pygame.K_RIGHT]
            and player.x < current_width - Constants.DEFAULT_PLAYER_SIZE
        ):
            player.x += 6
        if (
            keys[pygame.K_UP]
            and player.y < current_height - Constants.DEFAULT_PLAYER_SIZE
        ):
            player.y -= 4
        if keys[pygame.K_DOWN] and player.y >= 0:
            player.y += 4

        if game_on:
            object_spawn_timer += 1
            game_loop_counter += 1
            if object_spawn_timer == object_spawn_interval:
                objects.append(
                    GameObjectFactory.create_angry_cat(
                        x=random.randint(
                            0, current_width - Constants.DEFAULT_OBJECT_SIZE
                        ),
                        y=-Constants.DEFAULT_OBJECT_SIZE,
                        game_loop_i=game_loop_counter,
                    )
                )
                object_spawn_timer = 0

            # create boss cat
            if (
                score > Constants.BOSS_START_SCORE
                and score % Constants.BOSS_START_SCORE == 0
            ):
                objects.append(
                    GameObjectFactory.create_boss_cat(
                        x=random.randint(0, current_width - Constants.BOSS_OBJECT_SIZE),
                        y=-Constants.BOSS_OBJECT_SIZE,
                    )
                )

            bosses = [obj for obj in objects if isinstance(obj, Boss)]

            for obj in objects:
                obj.move()

            for blt in bullets:
                blt.move()

            objects = [obj for obj in objects if obj.y < current_height]
            bullets = [blt for blt in bullets if blt.y < current_height]

            # Collision detection: bullets and objects
            for blt in bullets:
                for obj in objects:
                    blt.check_collide_and_hit_if_so(obj)

            game_won = len(bosses) > 0 and any(b.dead() for b in bosses)

            if game_won:
                game_on = False
                continue

            objects = [obj for obj in objects if not obj.dead()]
            bullets = [blt for blt in bullets if not blt.dead()]

            # Collision detection: objects and player
            for obj in objects:
                if obj.check_collide(player):
                    game_on = False

            # Update score
            score += 1

        # Draw everything
        screen.blit(player.surface, (player.x, player.y))
        for obj in objects:
            screen.blit(obj.surface, obj.pos())
        for blt in bullets:
            screen.blit(blt.surface, blt.pos())

        # Display score with a nice background
        score_text = score_font.render(f"Score: {score}", True, Constants.WHITE)
        score_rect = score_text.get_rect(topleft=(10, 10))
        pygame.draw.rect(screen, (0, 0, 0, 128), score_rect.inflate(20, 10))
        screen.blit(score_text, score_rect)

        if not game_on:
            show_game_end(screen, game_won, score)

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
