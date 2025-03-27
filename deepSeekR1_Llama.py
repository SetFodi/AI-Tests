import pygame
import math

# Window size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)

class Ball:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.radius = 10
        self.speed_x = 5
        self.speed_y = 5

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), self.radius)

def draw_hexagon(screen, center, size, angle):
    points = []
    for i in range(6):
        rad = math.radians(60 * i + angle)
        x = center[0] + size * math.cos(rad)
        y = center[1] + size * math.sin(rad)
        points.append((x, y))
    for i in range(6):
        pygame.draw.line(screen, CYAN, points[i], points[(i+1)%6], 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    ball = Ball()
    angle = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(WHITE)
        draw_hexagon(screen, (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 100, angle)
        ball.move()
        ball.draw(screen)

        # Simple boundary checking (would need more complex collision detection for hexagon)
        if ball.x < 0 or ball.x > SCREEN_WIDTH:
            ball.speed_x *= -1
        if ball.y < 0 or ball.y > SCREEN_HEIGHT:
            ball.speed_y *= -1

        angle += 1
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

