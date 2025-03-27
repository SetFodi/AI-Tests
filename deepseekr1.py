import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Hexagon parameters
center = (screen_width // 2, screen_height // 2)
hex_radius = 200
rotation_speed = 1  # Degrees per frame

# Ball parameters
ball_radius = 10
ball_pos = [center[0] + 100, center[1]]  # Start offset from center
ball_velocity = [3, 3]

# Precompute original hexagon vertices (unrotated)
original_vertices = []
for i in range(6):
    angle = math.radians(60 * i)
    x = hex_radius * math.cos(angle)
    y = hex_radius * math.sin(angle)
    original_vertices.append((x, y))

# Main loop
clock = pygame.time.Clock()
rotation_angle = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update rotation angle
    rotation_angle += rotation_speed
    if rotation_angle >= 360:
        rotation_angle -= 360

    # Calculate current vertices with rotation
    current_vertices = []
    angle_rad = math.radians(rotation_angle)
    cos_angle = math.cos(angle_rad)
    sin_angle = math.sin(angle_rad)
    
    for x, y in original_vertices:
        # Apply rotation
        rot_x = x * cos_angle - y * sin_angle
        rot_y = x * sin_angle + y * cos_angle
        # Translate to screen position
        current_vertices.append((rot_x + center[0], rot_y + center[1]))

    # Update ball position
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]

    # Collision detection with hexagon walls
    for i in range(6):
        v1 = current_vertices[i]
        v2 = current_vertices[(i + 1) % 6]
        
        # Convert to floats for precision
        x1, y1 = v1
        x2, y2 = v2
        
        # Calculate edge vector
        edge_x = x2 - x1
        edge_y = y2 - y1
        
        # Calculate normal vector (pointing inward)
        norm_x = edge_y
        norm_y = -edge_x
        length = math.hypot(norm_x, norm_y)
        if length == 0:
            continue
        
        # Normalize normal vector
        norm_x /= length
        norm_y /= length
        
        # Calculate distance from ball to edge
        ball_to_v1_x = ball_pos[0] - x1
        ball_to_v1_y = ball_pos[1] - y1
        distance = (ball_to_v1_x * norm_x + ball_to_v1_y * norm_y) - ball_radius
        
        if distance < 0:
            # Calculate reflection
            dot_product = ball_velocity[0] * norm_x + ball_velocity[1] * norm_y
            ball_velocity[0] -= 2 * dot_product * norm_x
            ball_velocity[1] -= 2 * dot_product * norm_y
            
            # Move ball outside collision area
            ball_pos[0] -= distance * norm_x
            ball_pos[1] -= distance * norm_y
            break

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.polygon(screen, WHITE, current_vertices, 2)
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
