import sys
import math
import random
import pygame

# --- Configuration ---
WIDTH, HEIGHT = 800, 600
HEX_RADIUS = 250
BALL_RADIUS = 15
ROTATION_SPEED = 0.5  # radians per second
BALL_SPEED = 300      # pixels per second
FPS = 60

# --- Initialization ---
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
center = pygame.math.Vector2(WIDTH / 2, HEIGHT / 2)

# Precompute unrotated hexagon vertices
orig_vertices = []
for i in range(6):
    angle = math.pi / 3 * i
    x = center.x + HEX_RADIUS * math.cos(angle)
    y = center.y + HEX_RADIUS * math.sin(angle)
    orig_vertices.append(pygame.math.Vector2(x, y))

# Ball state
ball_pos = center + pygame.math.Vector2(random.uniform(-100, 100),
                                        random.uniform(-100, 100))
angle = random.uniform(0, 2 * math.pi)
ball_vel = pygame.math.Vector2(math.cos(angle),
                               math.sin(angle)) * BALL_SPEED

rotation = 0.0

def reflect(vel, normal):
    """Reflect velocity vel around unit normal."""
    return vel - 2 * vel.dot(normal) * normal

running = True
while running:
    dt = clock.tick(FPS) / 1000.0
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False

    # Update rotation
    rotation += ROTATION_SPEED * dt
    cos_r = math.cos(rotation)
    sin_r = math.sin(rotation)

    # Compute rotated hexagon vertices
    verts = []
    for v in orig_vertices:
        rel = v - center
        rx = rel.x * cos_r - rel.y * sin_r
        ry = rel.x * sin_r + rel.y * cos_r
        verts.append(center + pygame.math.Vector2(rx, ry))

    # Move ball
    ball_pos += ball_vel * dt

    # Collision with each edge
    for i in range(6):
        p1 = verts[i]
        p2 = verts[(i + 1) % 6]
        edge = p2 - p1
        edge_len2 = edge.length_squared()
        # Project ball center onto edge
        t = max(0.0, min(1.0, (ball_pos - p1).dot(edge) / edge_len2))
        closest = p1 + edge * t
        diff = ball_pos - closest
        dist2 = diff.length_squared()
        if dist2 <= BALL_RADIUS * BALL_RADIUS:
            # Collision detected
            if diff.length() == 0:
                # Degenerate: push out along normal of edge
                normal = pygame.math.Vector2(-edge.y, edge.x).normalize()
            else:
                normal = diff.normalize()
            ball_vel = reflect(ball_vel, normal)
            # Reposition ball just outside
            ball_pos = closest + normal * BALL_RADIUS

    # Draw
    screen.fill((30, 30, 30))
    pygame.draw.polygon(screen, (200, 200, 0), verts, 4)
    pygame.draw.circle(screen, (0, 200, 200),
                       (int(ball_pos.x), int(ball_pos.y)),
                       BALL_RADIUS)
    pygame.display.flip()

pygame.quit()
sys.exit()
