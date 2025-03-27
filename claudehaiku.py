import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hexagon Ball Physics Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Hexagon properties
HEXAGON_RADIUS = 250
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2

# Ball properties
BALL_RADIUS = 20
GRAVITY = 0.5
FRICTION = 0.99
BOUNCE_DAMPING = 0.9

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-5, 5)
        self.vy = random.uniform(-5, 5)
        self.radius = BALL_RADIUS
    
    def update(self):
        # Apply gravity
        self.vy += GRAVITY
        
        # Update position
        self.x += self.vx
        self.y += self.vy
        
        # Apply friction
        self.vx *= FRICTION
        self.vy *= FRICTION

def calculate_hexagon_vertices():
    vertices = []
    for i in range(6):
        angle = math.pi / 3 * i - math.pi / 2
        x = CENTER_X + HEXAGON_RADIUS * math.cos(angle)
        y = CENTER_Y + HEXAGON_RADIUS * math.sin(angle)
        vertices.append((x, y))
    return vertices

def line_intersection(line1, line2):
    x1, y1 = line1[0]
    x2, y2 = line1[1]
    x3, y3 = line2[0]
    x4, y4 = line2[1]
    
    # Calculate denominator
    denom = ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
    if denom == 0:
        return None
    
    # Calculate intersection point
    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    
    if 0 <= ua <= 1 and 0 <= ub <= 1:
        x = x1 + ua * (x2 - x1)
        y = y1 + ua * (y2 - y1)
        return (x, y)
    return None

def check_ball_hexagon_collision(ball, vertices):
    # Create hexagon lines
    hexagon_lines = [(vertices[i], vertices[(i+1)%6]) for i in range(6)]
    
    # Ball's potential next position
    ball_lines = [
        ((ball.x, ball.y), (ball.x + ball.vx, ball.y + ball.vy))
    ]
    
    for hex_line in hexagon_lines:
        for ball_line in ball_lines:
            # Check line segment intersections
            intersect = line_intersection(hex_line, ball_line)
            
            if intersect:
                # Calculate normal vector of the line
                line_vec_x = hex_line[1][0] - hex_line[0][0]
                line_vec_y = hex_line[1][1] - hex_line[0][1]
                
                # Normalize the vector
                line_length = math.sqrt(line_vec_x**2 + line_vec_y**2)
                normal_x = -line_vec_y / line_length
                normal_y = line_vec_x / line_length
                
                # Calculate reflection
                dot_product = ball.vx * normal_x + ball.vy * normal_y
                ball.vx -= 2 * dot_product * normal_x * BOUNCE_DAMPING
                ball.vy -= 2 * dot_product * normal_y * BOUNCE_DAMPING

def main():
    clock = pygame.time.Clock()
    ball = Ball(CENTER_X, CENTER_Y)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear screen
        screen.fill(BLACK)
        
        # Draw hexagon
        vertices = calculate_hexagon_vertices()
        pygame.draw.polygon(screen, WHITE, vertices, 2)
        
        # Update and draw ball
        ball.update()
        check_ball_hexagon_collision(ball, vertices)
        
        # Draw ball
        pygame.draw.circle(screen, RED, (int(ball.x), int(ball.y)), BALL_RADIUS)
        
        # Update display
        pygame.display.flip()
        
        # Control frame rate
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()
