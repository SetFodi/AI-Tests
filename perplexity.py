import pygame
import math

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spinning Hexagon with Bouncing Ball")
clock = pygame.time.Clock()

# Physics constants
GRAVITY = 0.2
FRICTION = 0.99
BOUNCE_ENERGY_LOSS = 0.9

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Ball:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.vx = 5
        self.vy = -5
        
    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy
        self.vx *= FRICTION
        self.vy *= FRICTION
        
    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)
        
    def bounce(self, normal):
        dot_product = self.vx * normal[0] + self.vy * normal[1]
        self.vx -= 2 * dot_product * normal[0] * BOUNCE_ENERGY_LOSS
        self.vy -= 2 * dot_product * normal[1] * BOUNCE_ENERGY_LOSS

class SpinningHexagon:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius
        self.angle = 0
        self.rotation_speed = 0.02
        
    def update(self):
        self.angle += self.rotation_speed
        
    def get_vertices(self):
        return [(self.center[0] + self.radius * math.cos(self.angle + i * math.pi/3),
                 self.center[1] + self.radius * math.sin(self.angle + i * math.pi/3)) 
                for i in range(6)]
    
    def get_edge_normals(self):
        vertices = self.get_vertices()
        return [(-math.sin(self.angle + i*math.pi/3), math.cos(self.angle + i*math.pi/3)) 
                for i in range(6)]

def main():
    hexagon = SpinningHexagon((WIDTH//2, HEIGHT//2), 200)
    ball = Ball(WIDTH//2, HEIGHT//2 - 150, 20)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Update positions
        hexagon.update()
        ball.update()
        
        # Collision detection
        normals = hexagon.get_edge_normals()
        vertices = hexagon.get_vertices()
        
        for i in range(6):
            px, py = vertices[i]
            nx, ny = normals[i]
            distance = nx*(ball.x - px) + ny*(ball.y - py)
            
            if distance < ball.radius:
                ball.bounce((nx, ny))
        
        # Drawing
        screen.fill(BLACK)
        pygame.draw.polygon(screen, WHITE, vertices, 2)
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

