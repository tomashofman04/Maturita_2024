import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 600, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vel = 0
        self.gravity = 0.5
        self.lift = -10

    def jump(self):
        self.vel += self.lift

    def update(self):
        self.vel += self.gravity
        self.y += self.vel

class Pipe:
    def __init__(self):
        self.top = random.randint(50, HEIGHT/2 - 50)
        self.bottom = random.randint(50, HEIGHT/2 - 50)
        self.x = WIDTH
        self.width = 40
        self.speed = 3

    def update(self):
        self.x -= self.speed

def check_collision():
    for pipe in pipes:
        if bird.x + 20 > pipe.x and bird.x < pipe.x + pipe.width:
            if bird.y < pipe.top or bird.y + 20 > HEIGHT - pipe.bottom:
                return True
    return False

def check_out_of_screen():
    if bird.y < 0 or bird.y + 20 > HEIGHT:
        return True
    return False

def display_score():
    score_surface = font.render(f"Score: {score}", True, WHITE)
    win.blit(score_surface, (10, 10))

bird = Bird()
pipes = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    bird.update()
    if check_collision():
        pygame.time.delay(1000)
        bird = Bird()
        pipes = []
        score = 0

    if check_out_of_screen():
        pygame.time.delay(1000)
        bird = Bird()
        pipes = []
        score = 0

    if pipes and pipes[0].x < -pipes[0].width:
        pipes.pop(0)
        score += 1

    if len(pipes) < 5:
        if pipes == [] or pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe())

    for pipe in pipes:
        pipe.update()

    win.fill(BLACK)
    pygame.draw.rect(win, WHITE, (bird.x, bird.y, 20, 20))

    for pipe in pipes:
        pygame.draw.rect(win, WHITE, (pipe.x, 0, pipe.width, pipe.top))
        pygame.draw.rect(win, WHITE, (pipe.x, HEIGHT - pipe.bottom, pipe.width, pipe.bottom))

    display_score()

    pygame.display.update()
    clock.tick(30)

