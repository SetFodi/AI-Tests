import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Hexagon properties
center_x = WIDTH // 2
center_y = HEIGHT // 2
hex_size = 200
hex_angle = 0
rotation_speed = 2  # degrees per frame

# Ball properties
ball_radius = 20
ball_x = center_x
ball_y = center_y
ball_dx = random.uniform(-3, 3)  # Initial random velocity x
ball_dy = random.uniform(-3, 3)  # Initial random velocity y
gravity = 0.1
friction = 0.99

# Clock for controlling frame rate
clock = pygame.time.Clock()

def rotate_point(x, y, angle, cx, cy):
    """Rotate a point around a center point"""
    angle_rad = math.radians(angle)
    temp_x = x - cx
    temp_y = y - cy
    rotated_x = temp_x * math.cos(angle_rad) - temp_y * math.sin(angle_rad)
    rotated_y = temp_x * math.sin(angle_rad) + temp_y * math.cos(angle_rad)
    return rotated_x + cx, rotated_y + cy

def get_hexagon_vertices(cx, cy, size, angle):
    """Calculate hexagon vertices with rotation"""
    vertices = []
    for i in range(6):
        angle_rad = math.radians(60 * i + angle)
        x = cx + size * math.cos(angle_rad)
        y = cy + size * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices

def line_intersection(p1, p2, p3, p4):
    """Find intersection point of two lines"""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4
    
    denom = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if denom == 0:
        return None
    
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denom
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denom
    
    return px, py

def reflect_velocity(ball_pos, ball_vel, wall_p1, wall_p2):
    """Calculate reflection of ball velocity off a wall"""
    vx, vy = ball_vel
    
    # Wall vector
    wx = wall_p2[0] - wall_p1[0]
    wy = wall_p2[1] - wall_p1[1]
    
    # Normal vector
    length = math.sqrt(wx * wx + wy * wy)
    nx = -wy / length
    ny = wx / length
    
    # Dot product of velocity and normal
    dot = vx * nx + vy * ny
    
    # Reflect velocity
    new_vx = vx - 2 * dot * nx
    new_vy = vy - 2 * dot * ny
    
    return new_vx * friction, new_vy * friction

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update hexagon rotation
    hex_angle = (hex_angle + rotation_speed) % 360
    vertices = get_hexagon_vertices(center_x, center_y, hex_size, hex_angle)
    
    # Update ball position
    ball_dy += gravity  # Apply gravity
    ball_x += ball_dx
    ball_y += ball_dy
    
    # Check collision with hexagon walls
    for i in range(6):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % 6]
        
        # Previous ball position
        prev_x = ball_x - ball_dx
        prev_y = ball_y - ball_dy
        
        # Check if ball crossed the wall
        intersection = line_intersection(
            (prev_x, prev_y),
            (ball_x, ball_y),
            p1,
            p2
        )
        
        if intersection:
            # Distance to wall
            dx = ball_x - intersection[0]
            dy = ball_y - intersection[1]
            dist = math.sqrt(dx * dx + dy * dy)
            
            if dist < ball_radius:
                # Reflect velocity
                ball_dx, ball_dy = reflect_velocity(
                    (ball_x, ball_y),
                    (ball_dx, ball_dy),
                    p1,
                    p2
                )
                
                # Move ball back to surface
                ball_x = intersection[0] - dx * (ball_radius / dist)
                ball_y = intersection[1] - dy * (ball_radius / dist)
    
    # Clear screen
    screen.fill(BLACK)
    
    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, vertices, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), ball_radius)
    
    # Update display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(60)

pygame.quit()
