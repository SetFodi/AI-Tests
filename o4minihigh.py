import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 600, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Hexagon Ball Bounce')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)

# Ball properties
ball_radius = 20
ball_x = width // 2
ball_y = height // 2
ball_speed_x = 4
ball_speed_y = 4

# Hexagon properties
hex_size = 200
angle = 0  # Initial angle for rotation
spin_speed = 0.5  # Speed of rotation

# Function to draw a rotated hexagon
def draw_hexagon(surface, x, y, size, angle):
    points = []
    for i in range(6):
        theta = math.radians(i * 60 + angle)
        x_pos = x + size * math.cos(theta)
        y_pos = y + size * math.sin(theta)
        points.append((x_pos, y_pos))
    pygame.draw.polygon(surface, WHITE, points, 2)

# Function to check if the ball is inside the hexagon
def is_ball_inside_hexagon(x, y, hex_x, hex_y, size):
    # Hexagon center to ball distance
    dx = x - hex_x
    dy = y - hex_y
    dist = math.sqrt(dx**2 + dy**2)
    return dist < size

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate the hexagon
    angle += spin_speed

    # Draw the spinning hexagon
    draw_hexagon(screen, width // 2, height // 2, hex_size, angle)

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check if the ball hits the walls of the hexagon
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
        ball_speed_x = -ball_speed_x
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
        ball_speed_y = -ball_speed_y

    # If ball hits the edge of the hexagon, reverse direction
    if not is_ball_inside_hexagon(ball_x, ball_y, width // 2, height // 2, hex_size):
        if ball_x - ball_radius <= width // 2:
            ball_speed_x = abs(ball_speed_x)
        elif ball_x + ball_radius >= width // 2:
            ball_speed_x = -abs(ball_speed_x)
        if ball_y - ball_radius <= height // 2:
            ball_speed_y = abs(ball_speed_y)
        elif ball_y + ball_radius >= height // 2:
            ball_speed_y = -abs(ball_speed_y)

    # Draw the ball
    pygame.draw.circle(screen, BALL_COLOR, (ball_x, ball_y), ball_radius)

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(60)

# Quit Pygame
pygame.quit()

