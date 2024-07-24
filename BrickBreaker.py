import pygame
import random

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = SCREEN_WIDTH//16*9
BRICK_ROWS, BRICK_COLS = 5, 10
BRICK_GAP = SCREEN_WIDTH//160
BRICK_WIDTH, BRICK_HEIGHT = (SCREEN_WIDTH-(BRICK_GAP*(BRICK_COLS-2)))//10, SCREEN_HEIGHT//20
PADDLE_WIDTH, PADDLE_HEIGHT = SCREEN_WIDTH//10, SCREEN_HEIGHT//40
BALL_RADIUS = SCREEN_WIDTH//80
PADDLE_SPEED = SCREEN_WIDTH//100
BALL_SPEED = PADDLE_SPEED//2

Black = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brick Breaker")
clock = pygame.time.Clock()

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 20))
        self.speed = PADDLE_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLUE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = BALL_SPEED
        self.dx = random.choice([-1, 1])
        self.dy = -1

    def update(self):
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.dx *= -1
        if self.rect.top <= 0:
            self.dy *= -1

all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()
paddle = Paddle()
ball = Ball()

for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = Brick(col * (BRICK_WIDTH + BRICK_GAP), row * (BRICK_HEIGHT + BRICK_GAP) + 50)
        bricks.add(brick)
        all_sprites.add(brick)

all_sprites.add(paddle, ball)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    if pygame.sprite.collide_rect(ball, paddle):
        ball.dy *= -1

    collisions = pygame.sprite.spritecollide(ball, bricks, True)
    if collisions:
        ball.dy *= -1

    if ball.rect.bottom >= SCREEN_HEIGHT:
        running = False

    screen.fill(Black)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
