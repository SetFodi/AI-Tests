import pygame
import math

# Initialize pygame
pygame.init()

# Set the screen size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagon Ball Bounce")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Hexagon parameters
HEX_RADIUS = 250  # Distance from center to a corner
CENTER = (WIDTH // 2, HEIGHT // 2)

# Ball parameters
BALL_RADIUS = 20
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_velocity = [5, 5]

# Function to draw rotating hexagon
def draw_hexagon(angle):
    points = []
    for i in range(6):
        x = CENTER[0] + HEX_RADIUS * math.cos(math.radians(i * 60 + angle))
        y = CENTER[1] + HEX_RADIUS * math.sin(math.radians(i * 60 + angle))
        points.append((x, y))
    pygame.draw.polygon(screen, WHITE, points, 3)

# Function to handle ball bouncing inside the hexagon
def ball_bounce():
    global ball_pos, ball_velocity

    # Ball movement
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Check collision with hexagon walls
    distance_from_center = math.sqrt((ball_pos[0] - CENTER[0]) ** 2 + (ball_pos[1] - CENTER[1]) ** 2)
    if distance_from_center + BALL_RADIUS > HEX_RADIUS:
        # Reflect the velocity (bouncing effect)
        normal_angle = math.atan2(ball_pos[1] - CENTER[1], ball_pos[0] - CENTER[0])
        ball_velocity[0] = -ball_velocity[0]
        ball_velocity[1] = -ball_velocity[1]

    # Keep ball inside the screen
    if ball_pos[0] - BALL_RADIUS < 0 or ball_pos[0] + BALL_RADIUS > WIDTH:
        ball_velocity[0] = -ball_velocity[0]
    if ball_pos[1] - BALL_RADIUS < 0 or ball_pos[1] + BALL_RADIUS > HEIGHT:
        ball_velocity[1] = -ball_velocity[1]

# Main loop
angle = 0
running = True
while running:
    screen.fill(BLACK)
    
    # Draw rotating hexagon
    draw_hexagon(angle)
    
    # Update ball position and handle bouncing
    ball_bounce()
    
    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update the angle to rotate the hexagon
    angle += 1  # Speed of rotation

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

