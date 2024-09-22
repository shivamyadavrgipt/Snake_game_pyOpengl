import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 102)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 100, 100)
GREY = (169, 169, 169)

# Screen dimensions
WIDTH = 600
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game with Obstacles')

# Game settings
clock = pygame.time.Clock()
SNAKE_BLOCK = 10
SNAKE_SPEED = 10

# Fonts
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Score display function
def show_score(score):
    value = score_font.render("Your Score: " + str(score), True, YELLOW)
    screen.blit(value, [0, 0])

# Draw snake function
def draw_snake(snake_segments):
    for segment in snake_segments:
        pygame.draw.circle(screen, BLACK, (segment[0] + SNAKE_BLOCK // 2, segment[1] + SNAKE_BLOCK // 2), SNAKE_BLOCK // 2)

# Display messages
def show_message(msg, color):
    message = font_style.render(msg, True, color)
    screen.blit(message, [WIDTH / 6, HEIGHT / 3])

# Draw obstacles
def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(screen, GREY, [obs[0], obs[1], SNAKE_BLOCK, SNAKE_BLOCK])

# Main game function
def game_loop():
    game_over = False
    game_close = False

    x = WIDTH / 2
    y = HEIGHT / 2
    x_change = 0
    y_change = 0

    snake_segments = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    # Central region for obstacles
    center_width_start = WIDTH // 3
    center_width_end = 2 * WIDTH // 3
    center_height_start = HEIGHT // 3
    center_height_end = 2 * HEIGHT // 3

    # Generate random obstacles
    obstacles = []
    for _ in range(10):
        obs_x = round(random.randrange(center_width_start, center_width_end - SNAKE_BLOCK) / 10.0) * 10.0
        obs_y = round(random.randrange(center_height_start, center_height_end - SNAKE_BLOCK) / 10.0) * 10.0
        obstacles.append([obs_x, obs_y])

    while not game_over:

        while game_close:
            screen.fill(BLUE)
            show_message("You Lost! Press Q-Quit or C-Play Again", RED)
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = SNAKE_BLOCK
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -SNAKE_BLOCK
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = SNAKE_BLOCK
                    x_change = 0

        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True
        x += x_change
        y += y_change
        screen.fill(BLUE)

        # Draw food
        pygame.draw.circle(screen, GREEN, (int(food_x + SNAKE_BLOCK // 2), int(food_y + SNAKE_BLOCK // 2)), SNAKE_BLOCK // 2)

        # Draw obstacles
        draw_obstacles(obstacles)

        # Update snake
        snake_head = [x, y]
        snake_segments.append(snake_head)

        if len(snake_segments) > snake_length:
            del snake_segments[0]

        for segment in snake_segments[:-1]:
            if segment == snake_head:
                game_close = True

        # Check collisions with obstacles
        for obs in obstacles:
            if x == obs[0] and y == obs[1]:
                game_close = True

        draw_snake(snake_segments)
        show_score(snake_length - 1)

        pygame.display.update()

        # Check if snake eats food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            food_y = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            snake_length += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()
    quit()

game_loop()
