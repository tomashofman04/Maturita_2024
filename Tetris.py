import pygame
import random

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = SCREEN_WIDTH*2
BLOCK_SIZE = int(SCREEN_WIDTH/10)
FPS = 5
Time = 0
DificultyIncreaser = FPS**20
FONT_SIZE = 36

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],
    [[1, 1],
     [1, 1]],
    [[1, 1, 0],
     [0, 1, 1]],
    [[0, 1, 1],
     [1, 1, 0]],
    [[1, 1, 1, 1]],
    [[1, 1, 1],
     [1, 0, 0]],
    [[1, 1, 1],
     [0, 0, 1]]
]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

font = pygame.font.SysFont(None, FONT_SIZE)

def draw_block(x, y, color):
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

def draw_board(board):
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell:
                draw_block(x, y, cell)

def new_piece():
    shape = random.choice(SHAPES)
    piece = {'shape': shape, 'x': SCREEN_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2, 'y': 0}
    return piece

def rotate_piece(piece):
    rotated_piece = {'shape': [], 'x': piece['x'], 'y': piece['y']}
    for i in range(len(piece['shape'][0])):
        new_row = []
        for j in range(len(piece['shape'])):
            new_row.append(piece['shape'][j][i])
        rotated_piece['shape'].append(new_row[::-1])
    return rotated_piece

def draw_piece(piece):
    shape = piece['shape']
    x, y = piece['x'], piece['y']
    for j, row in enumerate(shape):
        for i, cell in enumerate(row):
            if cell:
                draw_block(x + i, y + j, YELLOW)

def is_collision(board, piece):
    shape = piece['shape']
    x, y = piece['x'], piece['y']
    for j, row in enumerate(shape):
        for i, cell in enumerate(row):
            if cell and (x + i < 0 or x + i >= len(board[0]) or y + j >= len(board) or board[y + j][x + i]):
                return True
    return False

def merge_board(board, piece):
    shape = piece['shape']
    x, y = piece['x'], piece['y']
    for j, row in enumerate(shape):
        for i, cell in enumerate(row):
            if cell:
                board[y + j][x + i] = YELLOW

def check_lines(board):
    lines_to_clear = []
    for j, row in enumerate(board):
        if all(row):
            lines_to_clear.append(j)
    for j in lines_to_clear:
        del board[j]
        board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
    return len(lines_to_clear)

def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


if __name__ == "__main__":
    clock = pygame.time.Clock()
    board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    piece = new_piece()
    game_over = False
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    piece['x'] -= 1
                    if is_collision(board, piece):
                        piece['x'] += 1
                elif event.key == pygame.K_RIGHT:
                    piece['x'] += 1
                    if is_collision(board, piece):
                        piece['x'] -= 1
                elif event.key == pygame.K_DOWN:
                    piece['y'] += 1
                    if is_collision(board, piece):
                        piece['y'] -= 1
                elif event.key == pygame.K_UP:
                    rotated_piece = rotate_piece(piece)
                    if not is_collision(board, rotated_piece):
                        piece = rotated_piece

        screen.fill(BLACK)

        piece['y'] += 1
        if is_collision(board, piece):
            piece['y'] -= 1
            merge_board(board, piece)
            score += check_lines(board)
            piece = new_piece()
            if is_collision(board, piece):
                game_over = True

        draw_board(board)
        draw_piece(piece)
        draw_text(f'Score: {score}', WHITE, SCREEN_WIDTH // 2, FONT_SIZE // 2)

        pygame.display.flip()
        clock.tick(FPS)
        Time += 1
        if Time >= DificultyIncreaser:
            Time = 1
            FPS += 1

    draw_text("Game Over", RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()

