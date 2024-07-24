import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulace tří těles")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

G = 1.0
m = np.array([1.0, 1.0, 1.0])
r = np.array([[200.0, 300.0], [400.0, 200.0], [600.0, 400.0]])
v = np.array([[0.0, -0.5], [0.2, 0.0], [-0.2, 0.1]])

clock = pygame.time.Clock()
running = True
while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    a = np.zeros_like(r)
    for i in range(len(m)):
        for j in range(len(m)):
            if i != j:
                rij = r[j] - r[i]
                a[i] += G * m[j] * rij / np.linalg.norm(rij)**3
    v += a
    r += v
    win.fill(BLACK)
    for i in range(len(m)):
        pygame.draw.circle(win, RED, (int(r[i, 0]), int(r[i, 1])), 10)
    pygame.display.update()

pygame.quit()
