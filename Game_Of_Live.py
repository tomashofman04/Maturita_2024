import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRID_WIDTH, GRID_HEIGHT = 1280, 720
CELL_SIZE = 10
ROWS = GRID_HEIGHT // CELL_SIZE
COLS = GRID_WIDTH // CELL_SIZE

def create_grid(random=False):
    if random:
        return np.random.choice([0, 1], size=(ROWS, COLS))
    else:
        return np.zeros((ROWS, COLS))

def draw_grid(screen, grid):
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row, col] == 1:
                pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def get_neighbors(grid, row, col):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (0 <= row + i < ROWS) and (0 <= col + j < COLS):
                count += grid[row + i, col + j]
    return count

def update_grid(grid):
    new_grid = np.copy(grid)
    for row in range(ROWS):
        for col in range(COLS):
            neighbors = get_neighbors(grid, row, col)
            if grid[row, col] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_grid[row, col] = 0
            else:
                if neighbors == 3:
                    new_grid[row, col] = 1
    return new_grid

def main():
    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
    pygame.display.set_caption("Game of Life")
    grid = create_grid(random=True)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        grid = update_grid(grid)
        draw_grid(screen, grid)
        pygame.display.flip()
        pygame.time.Clock().tick(10)
    pygame.quit()
if __name__ == "__main__":
    main()
