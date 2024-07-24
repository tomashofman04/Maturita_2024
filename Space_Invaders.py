import pygame
import random

pygame.init()

screen_width = 1280
screen_height = screen_width//16*9
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Invaders")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

player_width = 50
player_height = 50
player_x = (screen_width - player_width) // 2
player_y = screen_height - player_height - 20
player_speed = 5
player = pygame.Rect(player_x, player_y, player_width, player_height)

enemy_width = 50
enemy_height = 50
enemy_speed = 2
enemies = []
num_enemies = 10
for i in range(num_enemies):
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = random.randint(50, 200)
    enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

bullet_width = 5
bullet_height = 15
bullet_speed = 7
bullets = []

font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()

score = 0
level = 1

def game_over():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + game_over_text.get_height()))
    pygame.display.flip()
    pygame.time.delay(3000)
    pygame.quit()

running = True
move_left = False
move_right = False
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.x + player.width // 2 - bullet_width // 2, player.y, bullet_width, bullet_height)
                bullets.append(bullet)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            if event.key == pygame.K_RIGHT:
                move_right = False

    if move_left and player.left > 0:
        player.x -= player_speed
    if move_right and player.right < screen_width:
        player.x += player_speed

    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    for enemy in enemies:
        enemy.x += enemy_speed
        if enemy.x > screen_width - enemy_width or enemy.x < 0:
            enemy_speed *= -1
            for e in enemies:
                e.y += 20
        if enemy.y + enemy.height > player.y:
            game_over()

    bullets_to_remove = []
    for bullet in bullets:
        for enemy in enemies:
            if bullet.colliderect(enemy):
                bullets_to_remove.append(bullet)
                enemies.remove(enemy)
                score += 10

    for bullet in bullets_to_remove:
        bullets.remove(bullet)
    pygame.draw.rect(screen, WHITE, player)
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)

    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (screen_width - level_text.get_width() - 10, 10))
    pygame.display.flip()

    if len(enemies) == 0:
        level += 1
        enemy_speed += 0.5
        num_enemies += 5
        for i in range(num_enemies):
            enemy_x = random.randint(0, screen_width - enemy_width)
            enemy_y = random.randint(50, 200)
            enemies.append(pygame.Rect(enemy_x, enemy_y, enemy_width, enemy_height))

    clock.tick(60)
    if player.collidelist(enemies) != -1:
        game_over()

pygame.quit()
