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

    # Player variables
    player_x = (SCREEN_WIDTH - PLAYER_SIZE) // 2
    player_y = SCREEN_HEIGHT - PLAYER_SIZE - 10

    # Object variables
    objects = []
    object_speed = 5
    object_spawn_timer = 0
    object_spawn_interval = 5

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
            new_obj_image = angry_images[random.randint(0, OBJECT_IMAGE_COUNT - 1)]
            new_obj = [
                random.randint(0, SCREEN_WIDTH - OBJECT_SIZE),
                -OBJECT_SIZE,
                # image of this object
                new_obj_image,
                # its own speed
                object_speed
                - 1
                + random.randint(0, 2) * (1 + game_loop_counter / 200.0),
            ]
            objects.append(new_obj)
            object_spawn_timer = 0

        for obj in objects:
            # adjust its Y
            obj[1] += obj[3]

        objects = [obj for obj in objects if obj[1] < SCREEN_HEIGHT]

        # Collision detection
        for obj in objects:
            if (
                player_x < obj[0] + OBJECT_SIZE
                and player_x + PLAYER_SIZE > obj[0]
                and player_y < obj[1] + OBJECT_SIZE
                and player_y + PLAYER_SIZE > obj[1]
            ):
                print("Game Over! Your Score:", score)
                pygame.quit()
                sys.exit()

        # Update score
        score += 1

        # Draw everything
        screen.blit(player_image, (player_x, player_y))
        for obj in objects:
            screen.blit(obj[2], (obj[0], obj[1]))

        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)


if __name__ == "__main__":
    main()
