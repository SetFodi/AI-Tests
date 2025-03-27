import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hexagon Ball Bounce")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up the hexagon
hexagon_radius = 200
hexagon_center = (width // 2, height // 2)
hexagon_points = []
for i in range(6):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    x = int(hexagon_center[0] + hexagon_radius * math.cos(angle_rad))
    y = int(hexagon_center[1] + hexagon_radius * math.sin(angle_rad))
    hexagon_points.append((x, y))

# Set up the ball
ball_radius = 20
ball_center = [width // 2, height // 2]
ball_speed = [3, 4]

# Set up the clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(WHITE)

    # Rotate the hexagon
    angle = pygame.time.get_ticks() / 1000 * 30  # Adjust the speed of rotation
    rotated_points = []
    for point in hexagon_points:
        x, y = point
        dx = x - hexagon_center[0]
        dy = y - hexagon_center[1]
        rotated_x = dx * math.cos(math.radians(angle)) - dy * math.sin(math.radians(angle))
        rotated_y = dx * math.sin(math.radians(angle)) + dy * math.cos(math.radians(angle))
        rotated_points.append((int(rotated_x + hexagon_center[0]), int(rotated_y + hexagon_center[1])))

    # Draw the hexagon
    pygame.draw.polygon(screen, BLACK, rotated_points, 2)

    # Move the ball
    ball_center[0] += ball_speed[0]
    ball_center[1] += ball_speed[1]

    # Check for collision with hexagon edges
    for i in range(6):
        p1 = rotated_points[i]
        p2 = rotated_points[(i + 1) % 6]
        edge_vector = (p2[0] - p1[0], p2[1] - p1[1])
        ball_vector = (ball_center[0] - p1[0], ball_center[1] - p1[1])
        edge_length_sq = edge_vector[0] ** 2 + edge_vector[1] ** 2
        proj_length = (ball_vector[0] * edge_vector[0] + ball_vector[1] * edge_vector[1]) / edge_length_sq
        closest_point = (int(p1[0] + proj_length * edge_vector[0]), int(p1[1] + proj_length * edge_vector[1]))
        distance = math.sqrt((ball_center[0] - closest_point[0]) ** 2 + (ball_center[1] - closest_point[1]) ** 2)
        if distance <= ball_radius:
            # Calculate reflection vector
            normal = (closest_point[1] - ball_center[1], ball_center[0] - closest_point[0])
            normal_length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
            normal = (normal[0] / normal_length, normal[1] / normal_length)
            dot_product = ball_speed[0] * normal[0] + ball_speed[1] * normal[1]
            ball_speed[0] -= 2 * dot_product * normal[0]
            ball_speed[1] -= 2 * dot_product * normal[1]

    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_center[0]), int(ball_center[1])), ball_radius)

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
