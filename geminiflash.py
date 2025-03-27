import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagon Ball Bounce")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Hexagon properties
HEXAGON_RADIUS = 200
HEXAGON_CENTER = (WIDTH // 2, HEIGHT // 2)
HEXAGON_POINTS = []
HEXAGON_ROTATION = 0
HEXAGON_ROTATION_SPEED = 0.5  # Degrees per frame

# Ball properties
BALL_RADIUS = 20
ball_x = random.uniform(HEXAGON_CENTER[0] - HEXAGON_RADIUS, HEXAGON_CENTER[0] + HEXAGON_RADIUS)
ball_y = random.uniform(HEXAGON_CENTER[1] - HEXAGON_RADIUS, HEXAGON_CENTER[1] + HEXAGON_RADIUS)
ball_speed_x = random.uniform(-5, 5)
ball_speed_y = random.uniform(-5, 5)

def calculate_hexagon_points(center, radius, rotation):
    points = []
    for i in range(6):
        angle_deg = 60 * i + rotation
        angle_rad = math.radians(angle_deg)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))
    return points

def check_collision(ball_x, ball_y, ball_radius, hexagon_points):
    for i in range(6):
        x1, y1 = hexagon_points[i]
        x2, y2 = hexagon_points[(i + 1) % 6]

        # Calculate the distance from the ball center to the line
        numerator = abs((x2 - x1) * (y1 - ball_y) - (x1 - ball_x) * (y2 - y1))
        denominator = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        distance = numerator / denominator if denominator != 0 else 0

        if distance <= ball_radius:
            # Collision detected, calculate reflection
            normal_x = y2 - y1
            normal_y = -(x2 - x1)
            normal_length = math.sqrt(normal_x**2 + normal_y**2)
            if normal_length != 0:
                normal_x /= normal_length
                normal_y /= normal_length

            dot_product = ball_speed_x * normal_x + ball_speed_y * normal_y
            ball_speed_x -= 2 * dot_product * normal_x
            ball_speed_y -= 2 * dot_product * normal_y
            return True
    return False

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    HEXAGON_ROTATION += HEXAGON_ROTATION_SPEED

    # Calculate hexagon points
    HEXAGON_POINTS = calculate_hexagon_points(HEXAGON_CENTER, HEXAGON_RADIUS, HEXAGON_ROTATION)

    # Update ball position
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Check for collision
    if check_collision(ball_x, ball_y, BALL_RADIUS, HEXAGON_POINTS):
        #Collision already handled in check_collision function.
        pass

    # Clear screen
    screen.fill(BLACK)

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, HEXAGON_POINTS, 2)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), BALL_RADIUS)

    # Update display
    pygame.display.flip()

    # Control frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
