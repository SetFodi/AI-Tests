import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagon Bouncing Ball")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Ball settings
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 4
ball_dy = 4

# Hexagon settings
hexagon_radius = 250
center_x = WIDTH // 2
center_y = HEIGHT // 2
rotation_angle = 0

# Function to draw a rotated hexagon
def draw_hexagon(angle):
    points = []
    for i in range(6):
        x = center_x + hexagon_radius * math.cos(math.radians(60 * i + angle))
        y = center_y + hexagon_radius * math.sin(math.radians(60 * i + angle))
        points.append((x, y))
    pygame.draw.polygon(screen, BLACK, points, 5)

# Function to check if the ball is within the hexagon
def is_ball_inside_hexagon(x, y):
    # Ball must be within the inscribed circle of the hexagon
    distance_from_center = math.sqrt((x - center_x)**2 + (y - center_y)**2)
    return distance_from_center <= hexagon_radius - ball_radius

# Main game loop
clock = pygame.time.Clock()

while True:
    screen.fill(WHITE)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Draw rotating hexagon
    draw_hexagon(rotation_angle)
    
    # Update ball position
    ball_x += ball_dx
    ball_y += ball_dy
    
    # Ball bouncing logic
    if not is_ball_inside_hexagon(ball_x, ball_y):
        # Reflect the ball's direction based on which side of the hexagon it hits
        if ball_x < center_x - hexagon_radius or ball_x > center_x + hexagon_radius:
            ball_dx = -ball_dx
        if ball_y < center_y - hexagon_radius or ball_y > center_y + hexagon_radius:
            ball_dy = -ball_dy

    # Draw the ball
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    
    # Rotate the hexagon angle
    rotation_angle += 1
    if rotation_angle >= 360:
        rotation_angle = 0
    
    # Update the display
    pygame.display.flip()
    
    # Set the frame rate
    clock.tick(60)

