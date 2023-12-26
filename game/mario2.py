import pygame
import sys
import random
from data.game_object import GameObject, GameObjectFactory
from data.const_data import Constants


def main():
    # Initialize Pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    PLAYER_SIZE = 40
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)

    # Create the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Mymario vs Angry Pong")

    # Load images
    background_image = pygame.image.load("images/back.png")
    player_image = pygame.image.load("images/hennysteel.png")

    # Player variables
    player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
    player_y = SCREEN_HEIGHT - PLAYER_SIZE - 10

    # Object variables - list of GameObject
    objects = []
    bullets = []
    object_speed = 5
    object_spawn_timer = 0
    object_spawn_interval = 5
    bullet_ready = False

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
                        GameObjectFactory.create_regular_bullet(x=player_x, y=player_y)
                    )
                elif event.key == pygame.K_x:
                    bullets.append(
                        GameObjectFactory.create_penetrable_bullet(
                            x=player_x, y=player_y
                        )
                    )

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 6
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
            player_x += 6
        if keys[pygame.K_UP] and player_y < SCREEN_HEIGHT - PLAYER_SIZE:
            player_y -= 4
        if keys[pygame.K_DOWN] and player_y >= 0:
            player_y += 4

        object_spawn_timer += 1
        game_loop_counter += 1
        if object_spawn_timer == object_spawn_interval:
            objects.append(
                GameObjectFactory.create_angry_cat(
                    x=random.randint(0, SCREEN_WIDTH - Constants.DEFAULT_OBJECT_SIZE),
                    y=-Constants.DEFAULT_OBJECT_SIZE,
                    game_loop_i=game_loop_counter,
                )
            )
            object_spawn_timer = 0

        for obj in objects:
            obj.move()

        for blt in bullets:
            blt.move()

        objects = [obj for obj in objects if obj.y < SCREEN_HEIGHT]
        bullets = [blt for blt in bullets if blt.y < SCREEN_HEIGHT]

        used_bullets = []

        # Collision detection: bullets and objects
        for blt in bullets:
            old_objects_len = len(objects)
            objects = [
                obj
                for obj in objects
                if not blt.check_collide((obj.x, obj.y), (obj.size, obj.size))
            ]
            if len(objects) is not old_objects_len and not blt.can_penetrate():
                used_bullets.append(blt)
        # take out used bullets that can't penetrate
        bullets = [blt for blt in bullets if blt not in used_bullets]

        # Collision detection: objects and player
        for obj in objects:
            if obj.check_collide((player_x, player_y), (PLAYER_SIZE, PLAYER_SIZE)):
                print("Game Over! Your Score:", score)
                pygame.quit()
                sys.exit()

        # Update score
        score += 1

        # Draw everything
        screen.blit(player_image, (player_x, player_y))
        for obj in objects:
            screen.blit(obj.surface, obj.pos())
        for blt in bullets:
            screen.blit(blt.surface, blt.pos())

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)


if __name__ == "__main__":
    main()
