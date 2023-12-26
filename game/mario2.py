import pygame
import sys
import random
from data.game_object import Boss, GameObject, GameObjectFactory
from data.const_data import Constants


def main():
    # Initialize Pygame
    pygame.init()

    # Create the screen
    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))
    pygame.display.set_caption("Henny Steel Rabbit vs Angry Cat")

    # Load images
    background_image = pygame.image.load("images/back.png")

    # Player variables
    player = GameObjectFactory.create_player(
        x=(Constants.SCREEN_WIDTH - Constants.DEFAULT_PLAYER_SIZE) // 2,
        y=Constants.SCREEN_HEIGHT - Constants.DEFAULT_PLAYER_SIZE - 10,
    )

    # Object variables - list of GameObject
    objects = []
    bullets = []
    object_spawn_timer = 0
    object_spawn_interval = 5

    # is the game done?
    game_on = True
    game_won = False

    # Score variables
    score = 0
    font = pygame.font.Font(None, 36)

    # Clock to control the frame rate
    clock = pygame.time.Clock()

    game_loop_counter = 0

    # Main game loop
    while True:
        screen.blit(background_image, (0, 0))

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
                elif not game_on and event.key == pygame.K_r:
                    # reset everything
                    # todo: put this into a common class / function
                    player = GameObjectFactory.create_player(
                        x=(Constants.SCREEN_WIDTH - Constants.DEFAULT_PLAYER_SIZE) // 2,
                        y=Constants.SCREEN_HEIGHT - Constants.DEFAULT_PLAYER_SIZE - 10,
                    )
                    objects = []
                    bullets = []
                    object_spawn_timer = 0
                    score = 0
                    game_on = True
                    game_won = False
                    clock = pygame.time.Clock()
                    game_loop_counter = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= 6
        if (
            keys[pygame.K_RIGHT]
            and player.x < Constants.SCREEN_WIDTH - Constants.DEFAULT_PLAYER_SIZE
        ):
            player.x += 6
        if (
            keys[pygame.K_UP]
            and player.y < Constants.SCREEN_HEIGHT - Constants.DEFAULT_PLAYER_SIZE
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
                            0, Constants.SCREEN_WIDTH - Constants.DEFAULT_OBJECT_SIZE
                        ),
                        y=-Constants.DEFAULT_OBJECT_SIZE,
                        game_loop_i=game_loop_counter,
                    )
                )
                object_spawn_timer = 0

            # create boss cat
            if (
                score > Constants.BOSS_START_SCORE
                and score % Constants.BOSS_START_SCORE is 0
            ):
                objects.append(
                    GameObjectFactory.create_boss_cat(
                        x=random.randint(
                            0, Constants.SCREEN_WIDTH - Constants.BOSS_OBJECT_SIZE
                        ),
                        y=-Constants.BOSS_OBJECT_SIZE,
                    )
                )

            bosses = [obj for obj in objects if isinstance(obj, Boss)]

            for obj in objects:
                obj.move()

            for blt in bullets:
                blt.move()

            objects = [obj for obj in objects if obj.y < Constants.SCREEN_HEIGHT]
            bullets = [blt for blt in bullets if blt.y < Constants.SCREEN_HEIGHT]

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

        # Display score
        score_text = font.render(f"Score: {score}", True, Constants.WHITE)
        screen.blit(score_text, (10, 10))

        if not game_on:
            show_game_end(screen, game_won, score)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(Constants.FPS)


def show_game_end(screen, game_won, score):
    font = pygame.font.Font(None, 80)
    win_msg = "YOU WIN!" if game_won else "You lost :("
    score_text = font.render(
        f"{win_msg} Score: {score}",
        True,
        Constants.GREEN if game_won else Constants.RED,
    )
    screen.blit(
        score_text,
        (Constants.SCREEN_WIDTH / 2 - 250, Constants.SCREEN_HEIGHT / 2 - 100),
    )


if __name__ == "__main__":
    main()
