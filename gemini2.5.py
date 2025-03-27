import pygame
import math
import sys

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Hexagon properties
HEX_CENTER_X = SCREEN_WIDTH // 2
HEX_CENTER_Y = SCREEN_HEIGHT // 2
HEX_RADIUS = 200  # Distance from center to vertex
HEX_SPIN_SPEED = 30  # Degrees per second
HEX_LINE_WIDTH = 3

# Ball properties
BALL_RADIUS = 15
BALL_INITIAL_POS = pygame.math.Vector2(HEX_CENTER_X, HEX_CENTER_Y)
BALL_INITIAL_SPEED = 250  # Pixels per second
BALL_INITIAL_ANGLE = 45  # Degrees
BOUNCINESS = 0.95 # Coefficient of restitution (1.0 = perfect bounce)

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")
clock = pygame.time.Clock()

# --- Game Variables ---
hexagon_angle = 0.0  # Current angle in degrees
ball_pos = pygame.math.Vector2(BALL_INITIAL_POS)
ball_vel = pygame.math.Vector2(
    BALL_INITIAL_SPEED * math.cos(math.radians(BALL_INITIAL_ANGLE)),
    BALL_INITIAL_SPEED * math.sin(math.radians(BALL_INITIAL_ANGLE)),
)

# --- Helper Functions ---
def get_hexagon_vertices(center_x, center_y, radius, angle_degrees):
    """Calculates the vertices of the hexagon based on its current rotation."""
    vertices = []
    center = pygame.math.Vector2(center_x, center_y)
    for i in range(6):
        angle_rad = math.radians(angle_degrees) + i * math.pi / 3
        vertex = center + pygame.math.Vector2(
            radius * math.cos(angle_rad), radius * math.sin(angle_rad)
        )
        vertices.append(vertex)
    return vertices

# --- Game Loop ---
running = True
while running:
    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Delta Time ---
    # Amount of time passed since the last frame in seconds
    dt = clock.tick(FPS) / 1000.0
    if dt > 0.1: # Avoid large jumps if debugging/stalling
        dt = 0.1

    # --- Updates ---
    # Spin the hexagon
    hexagon_angle = (hexagon_angle + HEX_SPIN_SPEED * dt) % 360

    # Move the ball
    ball_pos += ball_vel * dt

    # Calculate current hexagon vertices
    hexagon_vertices = get_hexagon_vertices(
        HEX_CENTER_X, HEX_CENTER_Y, HEX_RADIUS, hexagon_angle
    )

    # --- Collision Detection & Response ---
    for i in range(6):
        p1 = hexagon_vertices[i]
        p2 = hexagon_vertices[(i + 1) % 6] # Next vertex, wrapping around

        # Vector representing the hexagon side
        line_vec = p2 - p1
        line_len_sq = line_vec.length_squared()

        if line_len_sq == 0: # Avoid division by zero for zero-length segment
            continue

        # Vector from the start of the side to the ball's center
        point_vec = ball_pos - p1

        # Project point_vec onto line_vec to find the closest point on the infinite line
        # t is the projection parameter (0 <= t <= 1 means closest point is on the segment)
        t = point_vec.dot(line_vec) / line_len_sq
        t = max(0, min(1, t)) # Clamp t to the segment

        # Calculate the closest point on the line segment to the ball's center
        closest_point = p1 + t * line_vec

        # Vector from the closest point on the segment to the ball's center
        dist_vec = ball_pos - closest_point
        distance_sq = dist_vec.length_squared()

        # Check for collision
        if distance_sq <= (BALL_RADIUS * BALL_RADIUS):
            distance = math.sqrt(distance_sq)
            # Calculate the normal vector (points from wall towards ball center)
            if distance > 0: # Avoid division by zero if exactly on the point
                normal = dist_vec / distance
            else: # If distance is zero, pick a default normal (e.g., based on line)
                 # Perpendicular to line_vec (dx, dy) is (-dy, dx)
                 normal = pygame.math.Vector2(-line_vec.y, line_vec.x).normalize()


            # --- Collision Response ---
            # 1. Reflect velocity
            # Using pygame's reflect function: v' = v - 2 * dot(v, n) * n
            # We adjust for bounciness: v' = v - (1 + e) * dot(v, n) * n
            # Pygame's reflect assumes perfect reflection (e=1)
            # Manual calculation for bounciness:
            dot_product = ball_vel.dot(normal)
            # Only reflect if moving towards the wall (dot_product < 0)
            if dot_product < 0:
                ball_vel -= (1 + BOUNCINESS) * dot_product * normal

            # 2. Correct position to prevent sticking (move ball out of collision)
            overlap = BALL_RADIUS - distance
            if overlap > 0: # Ensure we only push out if truly overlapping
                 ball_pos += normal * overlap


    # --- Drawing ---
    screen.fill(BLACK)

    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hexagon_vertices, HEX_LINE_WIDTH)

    # Draw ball (convert Vector2 position to integer tuple for drawing)
    pygame.draw.circle(
        screen,
        RED,
        (int(ball_pos.x), int(ball_pos.y)),
        BALL_RADIUS,
    )

    # --- Display Update ---
    pygame.display.flip()

# --- Quit ---
pygame.quit()
sys.exit()

