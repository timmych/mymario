import pygame
import sys
import random
from data.game_object import GameObject


def main():
    # Initialize Pygame
    pygame.init()

    # Constants
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    PLAYER_SIZE = 40
    OBJECT_SIZE = 40
    BULLET_SIZE = 30
    OBJECT_IMAGE_COUNT = 4
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
    angry_images = []
    for i in range(OBJECT_IMAGE_COUNT):
        angry_images.append(pygame.image.load(f"images/angrypongpong{i}.png"))
    bullet_image = pygame.image.load("images/mango.png")

    # Player variables
    player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
    player_y = SCREEN_HEIGHT - PLAYER_SIZE - 10

    # Object variables - list of GameObject
    objects = []
    bullets = []
    object_speed = 5
    bullet_speed = 8
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullets.append(
                    GameObject(
                        x=player_x,
                        y=player_y,
                        size=BULLET_SIZE,
                        surface=bullet_image,
                        speed=-bullet_speed,
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
            new_obj_image = angry_images[random.randint(
                0, OBJECT_IMAGE_COUNT - 1)]
            new_obj = GameObject(
                x=random.randint(0, SCREEN_WIDTH - OBJECT_SIZE),
                y=-OBJECT_SIZE,
                size=OBJECT_SIZE,
                surface=new_obj_image,
                speed=object_speed
                - 1
                + random.randint(0, 2) * (1 + game_loop_counter / 200.0),
            )
            objects.append(new_obj)
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
            if len(objects) is not old_objects_len:
                used_bullets.append(blt)
        # take out used bullets
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
