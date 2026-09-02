import pygame
import random

# ---------- Setup ----------
pygame.init()

width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pikachu Game")

clock = pygame.time.Clock()

# ---------- Colors ----------
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# ---------- Snake settings ----------
block_size = 32
speed = 10

# ---------- Images ----------
pikachu_img = pygame.image.load("pikachu.png")
apple_img = pygame.image.load("apple.png")

pikachu_img = pygame.transform.scale(pikachu_img, (block_size, block_size))
apple_img = pygame.transform.scale(apple_img, (block_size, block_size))

font = pygame.font.SysFont("arial", 30)

def show_score(score):
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, [10, 10])

def draw_pikachu(block_size, pikachu_list):
    for block in pikachu_list:
        screen.blit(pikachu_img, (block[0], block[1]))

def game_loop():
    game_over = False

    # Starting position (middle of screen), snapped to the grid
    x = round((width / 2) / block_size) * block_size
    y = round((height / 2) / block_size) * block_size

    # Movement change per frame
    x_change = 0
    y_change = 0

    pikachu_list = []
    pikachu_length = 1

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
        screen.blit(apple_img, (food_x, food_y))

        # Update snake body
        pikachu_head = [x, y]
        pikachu_list.append(pikachu_head)
        if len(pikachu_list) > pikachu_length:
            del pikachu_list[0]

        # Check self collision
        for block in pikachu_list[:-1]:
            if block == pikachu_head:
                game_over = True

        draw_pikachu(block_size, pikachu_list)
        show_score(pikachu_length - 1)
        pygame.display.update()

        # Check if snake ate the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            pikachu_length += 1

        clock.tick(speed)

    pygame.quit()

game_loop()