import pygame
import random

# ---------- Setup ----------
pygame.init()

# Detect the laptop's actual screen size, then use 70% of it
info = pygame.display.Info()
width = int(info.current_w * 0.7)
height = int(info.current_h * 0.7)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

clock = pygame.time.Clock()

# ---------- Colors ----------
black = (0, 0, 0)
white = (255, 255, 255)
blue = (30, 144, 255)
green = (0, 200, 0)
yellow = (255, 255, 0)

font = pygame.font.SysFont("arial", 30)

# ---------- Bird settings ----------
bird_x = 60
bird_y = height / 2
bird_size = 25
bird_velocity = 0
gravity = 0.5
flap_strength = -8

# ---------- Pipe settings ----------
pipe_width = 60
pipe_gap = 150
pipe_speed = width / 150  # scales with screen size instead of a fixed number

def make_pipe():
    # Random height for the top pipe, gap comes after it
    top_height = random.randint(50, height - pipe_gap - 50)
    return {"x": width, "top_height": top_height, "scored": False}

pipes = [make_pipe()]

# ---------- Score ----------
score = 0

def show_score():
    text = font.render("Score: " + str(score), True, white)
    screen.blit(text, [10, 10])

def draw_bird(y):
    pygame.draw.circle(screen, yellow, (bird_x, int(y)), bird_size // 2)

def draw_pipes():
    for pipe in pipes:
        # Top pipe
        pygame.draw.rect(screen, green, [pipe["x"], 0, pipe_width, pipe["top_height"]])
        # Bottom pipe
        bottom_y = pipe["top_height"] + pipe_gap
        pygame.draw.rect(screen, green, [pipe["x"], bottom_y, pipe_width, height - bottom_y])

def game_loop():
    global bird_y, bird_velocity, score

    game_over = False
    game_started = False

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_started = True
                    bird_velocity = flap_strength

        # ---------- Bird physics ----------
        if game_started:
            bird_velocity += gravity
            bird_y += bird_velocity

        # ---------- Move pipes ----------
        if game_started:
            for pipe in pipes:
                pipe["x"] -= pipe_speed

        # Remove pipes that went off screen
        pipes[:] = [p for p in pipes if p["x"] + pipe_width > 0]

        # Add a new pipe once the last one is far enough left
        if pipes[-1]["x"] < width - (width * 0.55):
            pipes.append(make_pipe())

        # ---------- Scoring ----------
        for pipe in pipes:
            if not pipe["scored"] and pipe["x"] + pipe_width < bird_x:
                score += 1
                pipe["scored"] = True

        # ---------- Collision detection ----------
        bird_rect = pygame.Rect(bird_x - bird_size // 2, bird_y - bird_size // 2, bird_size, bird_size)

        # Hitting the ground or flying above the screen
        if bird_y + bird_size / 2 >= height or bird_y - bird_size / 2 <= 0:
            game_over = True

        for pipe in pipes:
            top_rect = pygame.Rect(pipe["x"], 0, pipe_width, pipe["top_height"])
            bottom_y = pipe["top_height"] + pipe_gap
            bottom_rect = pygame.Rect(pipe["x"], bottom_y, pipe_width, height - bottom_y)

            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                game_over = True

        # ---------- Draw everything ----------
        screen.fill(black)
        draw_pipes()
        draw_bird(bird_y)
        show_score()
        pygame.display.update()

        clock.tick(60)

    # ---------- Game over screen ----------
    screen.fill(black)
    text = font.render("Game Over! Final Score: " + str(score), True, white)
    screen.blit(text, [width / 2 - 150, height / 2])
    pygame.display.update()
    pygame.time.wait(3000)

    pygame.quit()

game_loop()