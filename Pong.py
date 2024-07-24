import pygame
import sys

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BALL_RADIUS = 10
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 5
BALL_SPEED_X, BALL_SPEED_Y = 5, 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

left_paddle_y = right_paddle_y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

left_score = 0
right_score = 0
font = pygame.font.SysFont(None, 36)

def draw_score():
    left_text = font.render(f"{left_score}", True, WHITE)
    right_text = font.render(f"{right_score}", True, WHITE)
    screen.blit(left_text, (SCREEN_WIDTH // 2.2, 20))
    screen.blit(right_text, (SCREEN_WIDTH - SCREEN_WIDTH // 2.2, 20))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle_y > 0:
        left_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        left_paddle_y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle_y > 0:
        right_paddle_y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle_y < SCREEN_HEIGHT - PADDLE_HEIGHT:
        right_paddle_y += PADDLE_SPEED

    ball_x += ball_dx
    ball_y += ball_dy

    if ball_y - BALL_RADIUS <= 0 or ball_y + BALL_RADIUS >= SCREEN_HEIGHT:
        ball_dy *= -1

    if (ball_x - BALL_RADIUS <= PADDLE_WIDTH and 
        left_paddle_y <= ball_y <= left_paddle_y + PADDLE_HEIGHT):
        ball_dx *= -1
    if (ball_x + BALL_RADIUS >= SCREEN_WIDTH - PADDLE_WIDTH and 
        right_paddle_y <= ball_y <= right_paddle_y + PADDLE_HEIGHT):
        ball_dx *= -1

    if ball_x - BALL_RADIUS <= 0:
        right_score += 1
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y
    if ball_x + BALL_RADIUS >= SCREEN_WIDTH:
        left_score += 1
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_dx, ball_dy = BALL_SPEED_X, BALL_SPEED_Y

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (0, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - PADDLE_WIDTH, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)
    draw_score()

    pygame.display.flip()
    pygame.time.Clock().tick(60)
