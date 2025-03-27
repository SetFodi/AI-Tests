import sys
import math
import pygame

# --------- Configuration ----------
WIDTH, HEIGHT = 800, 600
FPS = 60

# Hexagon properties
HEX_RADIUS = 250
HEX_CENTER = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
rotation_angle = 0.0  # in radians
ANGULAR_SPEED = 1.0  # radians per second

# Ball properties
BALL_RADIUS = 10
ball_pos = pygame.math.Vector2(HEX_CENTER.x, HEX_CENTER.y - 100)
ball_vel = pygame.math.Vector2(200, 120)  # initial velocity (pixels/sec)
# -----------------------------------

def closest_point_on_segment(P, A, B):
    """
    Returns the closest point Q on the segment AB to point P.
    All parameters are pygame.math.Vector2.
    """
    AB = B - A
    if AB.length_squared() == 0:
        return A.copy()
    t = (P - A).dot(AB) / AB.length_squared()
    t = max(0, min(1, t))  # clamp to [0, 1]
    Q = A + AB * t
    return Q

def handle_collision(ball_pos, ball_vel, ball_radius, A, B, hex_center, angular_speed):
    """
    Checks if the ball (circle) collides with edge AB.
    If so, compute the collision response with a realistic reflection
    (using the relative velocity between ball and moving edge).
    
    Parameters:
      ball_pos: pygame.math.Vector2 of ball center.
      ball_vel: pygame.math.Vector2 of ball velocity.
      ball_radius: radius of the ball.
      A, B: endpoints of the edge (pygame.math.Vector2).
      hex_center: center of the hexagon.
      angular_speed: the hexagon’s angular speed (radians/sec).
      
    Returns:
      (new_ball_pos, new_ball_vel, collided_flag)
    """
    Q = closest_point_on_segment(ball_pos, A, B)
    diff = ball_pos - Q
    distance = diff.length()

    if distance < ball_radius:
        # Determine the collision normal
        if distance == 0:
            # Avoid division by zero; use a normal pointing from A to ball center.
            n = (ball_pos - A).normalize()
        else:
            n = diff.normalize()

        # Compute penetration depth.
        penetration = ball_radius - distance

        # For a rotating hexagon, each wall segment moves tangentially.
        # The velocity of point Q on the wall (assuming anticlockwise rotation)
        # is given by:
        #
        #   v_wall = ω × r = (-ω * (Q_y - center_y), ω * (Q_x - center_x))
        #
        r = Q - hex_center
        v_wall = pygame.math.Vector2(-angular_speed * r.y, angular_speed * r.x)

        # Compute the ball’s velocity relative to the moving wall.
        v_rel = ball_vel - v_wall
        # Reflect the relative velocity across the edge’s normal.
        v_rel_new = v_rel - 2 * v_rel.dot(n) * n
        new_ball_vel = v_wall + v_rel_new

        # Move ball out of penetration.
        new_ball_pos = Q + n * ball_radius
        return new_ball_pos, new_ball_vel, True

    return ball_pos, ball_vel, False

def compute_hexagon_vertices(center, radius, angle_offset):
    """
    Returns a list of 6 (x, y) tuples for the vertices of a regular hexagon.
    The hexagon will be rotated by angle_offset (radians).
    """
    vertices = []
    for i in range(6):
        theta = angle_offset + i * (2 * math.pi / 6)
        x = center.x + radius * math.cos(theta)
        y = center.y + radius * math.sin(theta)
        vertices.append((int(x), int(y)))
    return vertices

def main():
    global rotation_angle, ball_pos, ball_vel

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Spinning Hexagon With Bouncing Ball")
    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Duration of frame in seconds

        # Process events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the hexagon's rotation.
        rotation_angle += ANGULAR_SPEED * dt

        # Update the ball position (simple linear motion).
        ball_pos += ball_vel * dt

        # Compute current hexagon vertices.
        hex_vertices = compute_hexagon_vertices(HEX_CENTER, HEX_RADIUS, rotation_angle)
        # Also create pygame Vector2 versions for collision math.
        # Order vertices so that adjacent pairs form edges.
        vertices_vec = [
            pygame.math.Vector2(pt[0], pt[1]) for pt in hex_vertices
        ]

        # Check collision with each edge of the hexagon.
        # (If colliding with multiple edges, we update sequentially.)
        for i in range(len(vertices_vec)):
            j = (i + 1) % len(vertices_vec)
            A = vertices_vec[i]
            B = vertices_vec[j]
            new_pos, new_vel, collided = handle_collision(
                ball_pos, ball_vel, BALL_RADIUS, A, B, HEX_CENTER, ANGULAR_SPEED
            )
            if collided:
                ball_pos = new_pos
                ball_vel = new_vel

        # Clear the screen.
        screen.fill((30, 30, 30))  # dark gray background

        # Draw the spinning hexagon.
        pygame.draw.polygon(screen, (200, 200, 200), hex_vertices, 3)

        # Draw the ball.
        pygame.draw.circle(
            screen, (255, 100, 100), (int(ball_pos.x), int(ball_pos.y)), BALL_RADIUS
        )

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

