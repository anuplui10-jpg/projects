import pygame
import math

# ---------- Setup ----------
pygame.init()

width, height = 800, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Needle Hit")

clock = pygame.time.Clock()

# ---------- Colors ----------
black = (0, 0, 0)
white = (255, 255, 255)
brown = (139, 69, 19)
red = (200, 30, 30)
silver = (200, 200, 200)

font = pygame.font.SysFont("arial", 30)
big_font = pygame.font.SysFont("arial", 50)

# ---------- Fruit settings ----------
fruit_center = (width // 2, height // 2 - 50)
fruit_radius = 80
fruit_angle = 0
fruit_speed = 1.5  # degrees per frame, increases over time

# ---------- Needle settings ----------
needle_length = 60
needle_speed = 25
flying_needle = None  # None when no needle is currently flying
stuck_needles = []  # list of angles (in degrees) where needles are stuck
needle_start_y = height - 100

# ---------- Score ----------
score = 0
winning_score = 15

def show_score():
    text = font.render(f"Score: {score}", True, white)
    goal_text = font.render(f"Reach {winning_score} to win!", True, white)
    screen.blit(text, [20, 20])
    screen.blit(goal_text, [20, 55])

def draw_fruit():
    pygame.draw.circle(screen, brown, fruit_center, fruit_radius)

    # Draw a stripe so the rotation is actually visible
    radians = math.radians(fruit_angle)
    stripe_end_x = fruit_center[0] + fruit_radius * math.sin(radians)
    stripe_end_y = fruit_center[1] - fruit_radius * math.cos(radians)
    pygame.draw.line(screen, black, fruit_center, (stripe_end_x, stripe_end_y), 5)

def draw_stuck_needles():
    for local_angle in stuck_needles:
        # Recalculate this needle's real screen angle every frame, based on
        # the fruit's CURRENT rotation plus where it's fixed on the fruit's surface.
        screen_angle = (fruit_angle + local_angle) % 360
        radians = math.radians(screen_angle)

        # Needle tip touches the edge of the fruit
        tip_x = fruit_center[0] + fruit_radius * math.sin(radians)
        tip_y = fruit_center[1] - fruit_radius * math.cos(radians)
        # Needle tail points outward from the fruit
        tail_x = fruit_center[0] + (fruit_radius + needle_length) * math.sin(radians)
        tail_y = fruit_center[1] - (fruit_radius + needle_length) * math.cos(radians)
        pygame.draw.line(screen, silver, (tip_x, tip_y), (tail_x, tail_y), 6)

def draw_flying_needle():
    if flying_needle is not None:
        y_position = flying_needle
    else:
        y_position = needle_start_y  # sits waiting here until clicked

    pygame.draw.line(screen, silver, (width // 2, y_position), (width // 2, y_position + needle_length), 6)

def angles_are_close(a, b, tolerance=12):
    diff = abs(a - b) % 360
    return diff < tolerance or diff > 360 - tolerance

def game_loop():
    global fruit_angle, fruit_speed, flying_needle, score

    game_over = False
    you_win = False

    while not game_over and not you_win:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if flying_needle is None:
                    flying_needle = needle_start_y

        # ---------- Rotate the fruit ----------
        fruit_angle = (fruit_angle + fruit_speed) % 360

        # ---------- Move the flying needle ----------
        if flying_needle is not None:
            flying_needle -= needle_speed

            # Check if it reached the fruit's edge
            if flying_needle <= fruit_center[1] + fruit_radius:
                # The needle always physically hits the bottom of the fruit (180 degrees).
                # Check if any already-stuck needle is currently sitting at that same spot.
                hit_something = False
                for local_angle in stuck_needles:
                    current_screen_angle = (fruit_angle + local_angle) % 360
                    if angles_are_close(current_screen_angle, 180, tolerance=15):
                        hit_something = True
                        break

                if hit_something:
                    game_over = True
                else:
                    # Store this needle's position relative to the fruit's own rotation,
                    # so it turns together with the fruit afterward.
                    local_angle = (180 - fruit_angle) % 360
                    stuck_needles.append(local_angle)
                    score += 1
                    fruit_speed += 0.15 # speeds up each successful hit

                    if score >= winning_score:
                        you_win = True

                flying_needle = None

        # ---------- Draw everything ----------
        screen.fill(black)
        draw_fruit()
        draw_stuck_needles()
        draw_flying_needle()
        show_score()
        pygame.display.update()

        clock.tick(60)

    # ---------- End screen ----------
    screen.fill(black)

    if you_win:
        text = big_font.render("Congratulations!", True, (0, 220, 0))
    else:
        text = big_font.render("Game Over!", True, red)

    score_text = font.render(f"Final Score: {score}", True, white)
    screen.blit(text, [width / 2 - 180, height / 2 - 30])
    screen.blit(score_text, [width / 2 - 90, height / 2 + 30])
    pygame.display.update()
    pygame.time.wait(3000)

    pygame.quit()

game_loop()