import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
FPS = 60
BALL_RADIUS = 15
HEX_SIZE = 250
SPEED = 5
ANGLE_INCREMENT = 1  # The speed of the rotation of the hexagon

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_COLOR = (255, 0, 0)
HEX_COLOR = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball Inside Rotating Hexagon")

# Ball's initial position and speed
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_velocity = [random.choice([-SPEED, SPEED]), random.choice([-SPEED, SPEED])]

# Function to draw a rotating hexagon
def draw_hexagon(angle):
    points = []
    for i in range(6):
        x = WIDTH // 2 + HEX_SIZE * math.cos(math.radians(60 * i + angle))
        y = HEIGHT // 2 + HEX_SIZE * math.sin(math.radians(60 * i + angle))
        points.append((x, y))
    pygame.draw.polygon(screen, HEX_COLOR, points, 3)

# Function to check if the ball is inside the hexagon
def is_ball_in_hexagon(ball_pos):
    x, y = ball_pos
    for i in range(6):
        angle_start = math.radians(60 * i)
        angle_end = math.radians(60 * (i + 1))
        
        # Calculate the vector that represents the edge
        edge_x1 = WIDTH // 2 + HEX_SIZE * math.cos(angle_start)
        edge_y1 = HEIGHT // 2 + HEX_SIZE * math.sin(angle_start)
        
        edge_x2 = WIDTH // 2 + HEX_SIZE * math.cos(angle_end)
        edge_y2 = HEIGHT // 2 + HEX_SIZE * math.sin(angle_end)
        
        # Check if the ball is within the angle boundaries
        if not (min(edge_x1, edge_x2) <= x <= max(edge_x1, edge_x2) and 
                min(edge_y1, edge_y2) <= y <= max(edge_y1, edge_y2)):
            return False
    return True

# Function to handle ball bounce inside hexagon
def handle_ball_bounce():
    global ball_pos, ball_velocity
    
    # Ball position update
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Ball bounce logic
    if not is_ball_in_hexagon(ball_pos):
        # Invert velocity to simulate a bounce
        if ball_pos[0] < WIDTH // 2:
            ball_velocity[0] = abs(ball_velocity[0])
        else:
            ball_velocity[0] = -abs(ball_velocity[0])

        if ball_pos[1] < HEIGHT // 2:
            ball_velocity[1] = abs(ball_velocity[1])
        else:
            ball_velocity[1] = -abs(ball_velocity[1])

# Main loop
angle = 0
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Rotate the hexagon continuously
    angle += ANGLE_INCREMENT

    # Handle the ball's movement and bounce
    handle_ball_bounce()

    # Draw the rotating hexagon and ball
    draw_hexagon(angle)
    pygame.draw.circle(screen, BALL_COLOR, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit pygame
pygame.quit()

