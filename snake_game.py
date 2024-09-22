import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Set the game window size
WINDOW_SIZE = (600, 400)
CELL_SIZE = 20

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Set up the game window
game_window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption('Snake Game')

# Game clock
clock = pygame.time.Clock()

# Font and Sounds
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)
eat_sound = pygame.mixer.Sound('eat.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

# Snake class
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WINDOW_SIZE[0] // 2), (WINDOW_SIZE[1] // 2))]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.grow = False
    
    def move(self):
        head_x, head_y = self.positions[0]
        if self.direction == pygame.K_UP:
            new_head = (head_x, head_y - CELL_SIZE)
        elif self.direction == pygame.K_DOWN:
            new_head = (head_x, head_y + CELL_SIZE)
        elif self.direction == pygame.K_LEFT:
            new_head = (head_x - CELL_SIZE, head_y)
        elif self.direction == pygame.K_RIGHT:
            new_head = (head_x + CELL_SIZE, head_y)

        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False

        self.positions.insert(0, new_head)

    def grow_snake(self):
        self.grow = True
        self.length += 1

    def collides_with_self(self):
        return self.positions[0] in self.positions[1:]

    def collides_with_wall(self):
        head_x, head_y = self.positions[0]
        return head_x < 0 or head_x >= WINDOW_SIZE[0] or head_y < 0 or head_y >= WINDOW_SIZE[1]

# Food class
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_SIZE[0] // CELL_SIZE) - 1) * CELL_SIZE,
                         random.randint(0, (WINDOW_SIZE[1] // CELL_SIZE) - 1) * CELL_SIZE)

def display_score(score):
    value = score_font.render("Your Score: " + str(score), True, WHITE)
    game_window.blit(value, [0, 0])

def game_over():
    game_window.fill(BLACK)
    message = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
    game_window.blit(message, [WINDOW_SIZE[0] // 6, WINDOW_SIZE[1] // 3])
    pygame.display.update()
    game_over_sound.play()
    time.sleep(2)

def game_loop():
    snake = Snake()
    food = Food()
    score = 0

    running = True
    game_over_flag = False

    while running:
        while game_over_flag:
            game_over()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        game_over_flag = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    snake.direction = event.key

        snake.move()

        # Check if snake eats food
        if snake.positions[0] == food.position:
            snake.grow_snake()
            score += 1
            eat_sound.play()
            food.randomize_position()

        # Check for collisions
        if snake.collides_with_self() or snake.collides_with_wall():
            game_over_flag = True

        # Redraw game window
        game_window.fill(BLUE)
        for pos in snake.positions:
            pygame.draw.rect(game_window, GREEN, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(game_window, RED, pygame.Rect(food.position[0], food.position[1], CELL_SIZE, CELL_SIZE))

        display_score(score)
        pygame.display.update()

        clock.tick(10 + score)  # Increase speed as score increases

    pygame.quit()

# Run the game loop
game_loop()
