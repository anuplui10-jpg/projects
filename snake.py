import pygame
import random

# ---------- Setup ----------
pygame.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# ---------- Colors ----------
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# ---------- Snake settings ----------
block_size = 20
speed = 10

font = pygame.font.SysFont("arial", 30)

def show_score(score):
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, [10, 10])

def draw_snake(block_size, snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, green, [block[0], block[1], block_size, block_size])

def game_loop():
    game_over = False

    # Starting position (middle of screen)
    x = width / 2
    y = height / 2

    # Movement change per frame
    x_change = 0
    y_change = 0

    snake_list = []
    snake_length = 1

    # Random starting food position
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -block_size
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = block_size
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -block_size
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = block_size
                    x_change = 0

        # Check wall collision
        if x >= width or x < 0 or y >= height or y < 0:
            game_over = True

        x += x_change
        y += y_change
        screen.fill(black)

        # Draw food
        pygame.draw.rect(screen, red, [food_x, food_y, block_size, block_size])

        # Update snake body
        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check self collision
        for block in snake_list[:-1]:
            if block == snake_head:
                game_over = True

        draw_snake(block_size, snake_list)
        show_score(snake_length - 1)
        pygame.display.update()

        # Check if snake ate the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1

        clock.tick(speed)

    pygame.quit()

game_loop()