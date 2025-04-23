import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hexagon Ball Bouncing")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)

# Ball properties
ball_radius = 15
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_dx = 4
ball_dy = 4

# Hexagon properties
hex_radius = 200
center_x = screen_width // 2
center_y = screen_height // 2
angle = 0

# Set up clock
clock = pygame.time.Clock()

def draw_hexagon(angle):
    points = []
    for i in range(6):
        x = center_x + hex_radius * math.cos(math.radians(angle + i * 60))
        y = center_y + hex_radius * math.sin(math.radians(angle + i * 60))
        points.append((x, y))
    pygame.draw.polygon(screen, WHITE, points, 3)

def check_collision():
    global ball_dx, ball_dy
    # Check collision with hexagon boundary
    distance_from_center = math.sqrt((ball_x - center_x) ** 2 + (ball_y - center_y) ** 2)
    if distance_from_center + ball_radius > hex_radius:
        angle_to_ball = math.atan2(ball_y - center_y, ball_x - center_x)
        ball_dx = -ball_dx * math.cos(angle_to_ball)
        ball_dy = -ball_dy * math.sin(angle_to_ball)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update angle for hexagon rotation
    angle += 1  # Change speed of rotation here

    # Draw hexagon
    draw_hexagon(angle)

    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy

    # Check for ball collision with hexagon boundary
    check_collision()

    # Draw ball
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), ball_radius)

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

pygame.quit()

