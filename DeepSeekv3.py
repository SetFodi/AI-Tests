import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagon Ball Physics")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Hexagon parameters
hexagon_radius = 200
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_angle = 0
hexagon_rotation_speed = 0.5  # degrees per frame

# Ball parameters
ball_radius = 20
ball_pos = [hexagon_center[0], hexagon_center[1] - 100]
ball_velocity = [random.uniform(-5, 5), random.uniform(-5, 5)]
ball_color = RED

# Physics parameters
gravity = 0.1
elasticity = 0.8  # Bounciness

def get_hexagon_points(center, radius, angle):
    points = []
    for i in range(6):
        angle_deg = 60 * i + angle
        angle_rad = math.radians(angle_deg)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))
    return points

def point_to_line_distance(point, line_start, line_end):
    x0, y0 = point
    x1, y1 = line_start
    x2, y2 = line_end

    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    
    if denominator == 0:
        return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
    return numerator / denominator

def check_collision(ball_pos, ball_radius, hexagon_points):
    for i in range(len(hexagon_points)):
        p1 = hexagon_points[i]
        p2 = hexagon_points[(i + 1) % len(hexagon_points)]
        
        # Check distance from ball center to hexagon edge
        distance = point_to_line_distance(ball_pos, p1, p2)
        
        if distance <= ball_radius:
            # Calculate normal vector of the edge
            edge_vec = (p2[0] - p1[0], p2[1] - p1[1])
            normal = (-edge_vec[1], edge_vec[0])
            
            # Normalize the normal vector
            length = math.sqrt(normal[0] ** 2 + normal[1] ** 2)
            if length > 0:
                normal = (normal[0] / length, normal[1] / length)
            
            return normal
    return None

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    screen.fill(BLACK)
    
    # Update hexagon rotation
    hexagon_angle = (hexagon_angle + hexagon_rotation_speed) % 360
    hexagon_points = get_hexagon_points(hexagon_center, hexagon_radius, hexagon_angle)
    
    # Update ball physics
    ball_velocity[1] += gravity  # Apply gravity
    
    # Move ball
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]
    
    # Check collision with hexagon
    collision_normal = check_collision(ball_pos, ball_radius, hexagon_points)
    if collision_normal:
        # Calculate dot product to determine reflection
        dot_product = ball_velocity[0] * collision_normal[0] + ball_velocity[1] * collision_normal[1]
        
        # Reflect velocity
        ball_velocity[0] = elasticity * (ball_velocity[0] - 2 * dot_product * collision_normal[0])
        ball_velocity[1] = elasticity * (ball_velocity[1] - 2 * dot_product * collision_normal[1])
        
        # Move ball outside the hexagon to prevent sticking
        ball_pos[0] += collision_normal[0] * (ball_radius - point_to_line_distance(ball_pos, 
            hexagon_points[0], hexagon_points[1]))
        ball_pos[1] += collision_normal[1] * (ball_radius - point_to_line_distance(ball_pos, 
            hexagon_points[0], hexagon_points[1]))
    
    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hexagon_points, 2)
    
    # Draw ball
    pygame.draw.circle(screen, ball_color, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

