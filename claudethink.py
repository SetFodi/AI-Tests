import pygame
import math
import sys
import numpy as np

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Hexagon parameters
center = np.array([WIDTH / 2, HEIGHT / 2])
radius = 200
num_sides = 6
rotation_speed = 0.01  # radians per frame

# Ball parameters
ball_radius = 15
ball_pos = np.array([center[0], center[1] - 100])  # Start near top of hexagon
ball_vel = np.array([3.0, 1.0])  # Initial velocity
gravity = np.array([0.0, 0.2])
elasticity = 0.9  # Bounce energy retention

# Clock for controlling frame rate
clock = pygame.time.Clock()

def get_hexagon_points(center, radius, rotation):
    """Calculate the vertices of the hexagon given center, radius, and rotation."""
    points = []
    for i in range(num_sides):
        angle = rotation + i * (2 * math.pi / num_sides)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append((x, y))
    return points

def get_hexagon_edges(points):
    """Get the edges of the hexagon as line segments."""
    edges = []
    for i in range(num_sides):
        edges.append((points[i], points[(i + 1) % num_sides]))
    return edges

def distance_to_line(point, line_start, line_end):
    """Calculate the shortest distance from a point to a line segment."""
    line_vec = np.array(line_end) - np.array(line_start)
    point_vec = np.array(point) - np.array(line_start)
    
    line_length = np.linalg.norm(line_vec)
    line_unit_vec = line_vec / line_length
    
    # Calculate projection of point onto line
    projection = np.dot(point_vec, line_unit_vec)
    
    if projection <= 0:
        return np.linalg.norm(point_vec)
    elif projection >= line_length:
        return np.linalg.norm(np.array(point) - np.array(line_end))
    else:
        # Calculate perpendicular distance
        perpendicular = point_vec - projection * line_unit_vec
        return np.linalg.norm(perpendicular)

def get_normal_vector(line_start, line_end):
    """Get the normal vector to a line segment pointing inward to the hexagon."""
    line_vec = np.array(line_end) - np.array(line_start)
    # Rotate 90 degrees counter-clockwise to get normal pointing outward
    normal = np.array([-line_vec[1], line_vec[0]])
    normal = normal / np.linalg.norm(normal)
    
    # Check if normal points inward, if not reverse it
    midpoint = (np.array(line_start) + np.array(line_end)) / 2
    to_center = center - midpoint
    if np.dot(normal, to_center) < 0:
        normal = -normal
    
    return normal

def reflect_velocity(velocity, normal):
    """Reflect velocity vector across the normal."""
    return velocity - 2 * np.dot(velocity, normal) * normal

# Main game loop
rotation = 0
running = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    screen.fill(BLACK)
    
    # Update rotation
    rotation += rotation_speed
    
    # Get hexagon points and edges
    hex_points = get_hexagon_points(center, radius, rotation)
    hex_edges = get_hexagon_edges(hex_points)
    
    # Update ball position with gravity
    ball_vel += gravity
    ball_pos += ball_vel
    
    # Check for collision with hexagon edges
    for edge in hex_edges:
        distance = distance_to_line(ball_pos, edge[0], edge[1])
        if distance < ball_radius:
            normal = get_normal_vector(edge[0], edge[1])
            ball_vel = reflect_velocity(ball_vel, normal) * elasticity
            
            # Move ball slightly away from the edge to prevent sticking
            adjustment = (ball_radius - distance + 0.5) * normal
            ball_pos += adjustment
    
    # Draw hexagon
    pygame.draw.polygon(screen, BLUE, hex_points, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()

