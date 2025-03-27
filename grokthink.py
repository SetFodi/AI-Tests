import pygame
import math

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")
clock = pygame.time.Clock()

# Constants
R = 200              # Radius of the hexagon (distance from center to vertex)
R_BALL = 10          # Radius of the ball
OMEGA = 1.0          # Angular velocity of the hexagon (radians per second)
DT = 1 / 60          # Time step per frame (assuming 60 FPS)
CENTER = (300, 300)  # Center of the screen

# Define hexagon vertices in the rotating frame (where hexagon is stationary)
vertices = [(R * math.cos(i * math.pi / 3), R * math.sin(i * math.pi / 3)) for i in range(6)]

# Define walls and their inward normals
walls = [(vertices[i], vertices[(i + 1) % 6]) for i in range(6)]
normals = []
for i in range(6):
    p1, p2 = walls[i]
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    # Inward normal for counterclockwise vertices: (-dy, dx)
    n = (-dy, dx)
    length = math.sqrt(n[0]**2 + n[1]**2)
    normals.append((n[0] / length, n[1] / length))

# Initialize ball in the rotating frame
x_prime, y_prime = 0, 0          # Start at the center
v_x_prime, v_y_prime = 100, 0    # Initial velocity (pixels per second)
phi = 0                          # Rotation angle of the hexagon

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the hexagon's rotation angle
    phi += OMEGA * DT

    # Calculate acceleration due to fictitious forces in the rotating frame
    a_x_prime = -OMEGA**2 * x_prime - 2 * OMEGA * v_y_prime  # Centrifugal + Coriolis
    a_y_prime = -OMEGA**2 * y_prime + 2 * OMEGA * v_x_prime

    # Update velocity (Euler integration)
    v_x_temp = v_x_prime + a_x_prime * DT
    v_y_temp = v_y_prime + a_y_prime * DT

    # Calculate potential new position
    x_temp = x_prime + v_x_temp * DT
    y_temp = y_prime + v_y_temp * DT

    # Collision detection
    collision = False
    min_t = DT
    collision_normal = None
    for i in range(6):
        p1, p2 = walls[i]
        n = normals[i]
        # Signed distance from current position to the wall
        d0 = (x_prime - p1[0]) * n[0] + (y_prime - p1[1]) * n[1]
        # Velocity component along the normal
        vd = v_x_temp * n[0] + v_y_temp * n[1]
        if vd < 0:  # Moving towards the wall
            t_coll = (R_BALL - d0) / vd  # Time when distance equals ball radius
            if 0 < t_coll < min_t:
                # Check if collision point is within the wall segment
                x_coll = x_prime + v_x_temp * t_coll
                y_coll = y_prime + v_y_temp * t_coll
                d = (p2[0] - p1[0], p2[1] - p1[1])
                len_d = d[0]**2 + d[1]**2
                s = ((x_coll - p1[0]) * d[0] + (y_coll - p1[1]) * d[1]) / len_d
                if 0 <= s <= 1:  # Collision within segment
                    collision = True
                    min_t = t_coll
                    collision_normal = n

    if collision:
        # Move to collision point
        x_prime += v_x_temp * min_t
        y_prime += v_y_temp * min_t
        # Reflect velocity across the normal
        dot = v_x_prime * collision_normal[0] + v_y_prime * collision_normal[1]
        v_x_prime -= 2 * dot * collision_normal[0]
        v_y_prime -= 2 * dot * collision_normal[1]
        # Update for remaining time
        remaining_dt = DT - min_t
        a_x_prime = -OMEGA**2 * x_prime - 2 * OMEGA * v_y_prime
        a_y_prime = -OMEGA**2 * y_prime + 2 * OMEGA * v_x_prime
        v_x_prime += a_x_prime * remaining_dt
        v_y_prime += a_y_prime * remaining_dt
        x_prime += v_x_prime * remaining_dt
        y_prime += v_y_prime * remaining_dt
    else:
        # No collision, apply the temporary values
        x_prime, y_prime = x_temp, y_temp
        v_x_prime, v_y_prime = v_x_temp, v_y_temp

    # Drawing
    screen.fill((0, 0, 0))  # Black background

    # Draw hexagon
    screen_vertices = []
    for vertex in vertices:
        x_lab = vertex[0] * math.cos(phi) + vertex[1] * math.sin(phi)
        y_lab = -vertex[0] * math.sin(phi) + vertex[1] * math.cos(phi)
        screen_x = CENTER[0] + x_lab
        screen_y = CENTER[1] - y_lab  # Invert y-axis for Pygame
        screen_vertices.append((screen_x, screen_y))
    pygame.draw.polygon(screen, (255, 255, 255), screen_vertices, 1)  # White outline

    # Draw ball
    x_lab = x_prime * math.cos(phi) + y_prime * math.sin(phi)
    y_lab = -x_prime * math.sin(phi) + y_prime * math.cos(phi)
    screen_x = CENTER[0] + x_lab
    screen_y = CENTER[1] - y_lab
    pygame.draw.circle(screen, (255, 0, 0), (int(screen_x), int(screen_y)), R_BALL)  # Red ball

    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
