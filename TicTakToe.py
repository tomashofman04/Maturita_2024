import pygame
import sys
import random
import time

pygame.init()

WindowSize = 800
Chose_1 = 3
Chose_2 = 8
Chose_3 = 18

LINE_WIDTH = 5
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
PLAYER1_COLOR = (255, 0, 0)
PLAYER2_COLOR = (0, 0, 255)
Green = (0, 255, 0)

screen = pygame.display.set_mode((WindowSize, WindowSize))
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(BG_COLOR)
font = pygame.font.Font(None, int(WindowSize / 10))

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

button_1 = Button(WindowSize / 4, WindowSize / 4, WindowSize / 2, WindowSize / 8, f"{Chose_1}x{Chose_1} Board", (0, 255, 0))
button_2 = Button(WindowSize / 4, WindowSize / 2, WindowSize / 2, WindowSize / 8, f"{Chose_2}x{Chose_2} Board", (0, 255, 0))
button_3 = Button(WindowSize / 4, WindowSize * 3 / 4, WindowSize / 2, WindowSize / 8, f"{Chose_3}x{Chose_3} Board", (0, 255, 0))
button_2p = Button(WindowSize / 4, WindowSize * 2 / 4, WindowSize / 2, WindowSize / 8, "2 Player", (0, 255, 0))
button_Ai = Button(WindowSize / 4, WindowSize * 3 / 4, WindowSize / 2, WindowSize / 8, "Player vs Ai", (0, 255, 0))

def draw_menu(Stage):
    if Stage == 0:
        screen.fill(BG_COLOR)
        button_1.draw()
        button_2.draw()
        button_3.draw()
    else:
        screen.fill(BG_COLOR)
        button_2p.draw()
        button_Ai.draw()

def start_game(board_size, Ai):
    global BOARD_ROWS, BOARD_COLS, SQUARE_SIZE
    if board_size == Chose_1:
        BOARD_ROWS, BOARD_COLS = Chose_1, Chose_1
        SQUARE_SIZE = WindowSize // BOARD_ROWS
    elif board_size == Chose_2:
        BOARD_ROWS, BOARD_COLS = Chose_2, Chose_2
        SQUARE_SIZE = WindowSize // BOARD_ROWS
    elif board_size == Chose_3:
        BOARD_ROWS, BOARD_COLS = Chose_3, Chose_3
        SQUARE_SIZE = WindowSize // BOARD_ROWS

    global board
    board = [[None]*BOARD_COLS for _ in range(BOARD_ROWS)]

    game_loop(Ai)

def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WindowSize, i * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, WindowSize), LINE_WIDTH)


def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'X':
                pygame.draw.line(screen, PLAYER1_COLOR, (col * SQUARE_SIZE + 15, row * SQUARE_SIZE + 15),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 15, row * SQUARE_SIZE + SQUARE_SIZE - 15), 5)
                pygame.draw.line(screen, PLAYER1_COLOR, (col * SQUARE_SIZE + 15, row * SQUARE_SIZE + SQUARE_SIZE - 15),
                                 (col * SQUARE_SIZE + SQUARE_SIZE - 15, row * SQUARE_SIZE + 15), 5)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, PLAYER2_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE/2),
                                 int(row * SQUARE_SIZE + SQUARE_SIZE/2)), int(SQUARE_SIZE/2 - 15), 5)

def check_win(player):
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS - 4):
            if all([board[row][col + i] == player for i in range(5)]):
                return True

    for col in range(BOARD_COLS):
        for row in range(BOARD_ROWS - 4):
            if all([board[row + i][col] == player for i in range(5)]):
                return True

    for row in range(BOARD_ROWS - 4):
        for col in range(BOARD_COLS - 4):
            if all([board[row + i][col + i] == player for i in range(5)]) or \
               all([board[row + i][col + 4 - i] == player for i in range(5)]):
                return True

    for row in range(BOARD_ROWS):
        if all([board[row][col] == player for col in range(BOARD_COLS)]):
            return True

    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True

    if all([board[i][i] == player for i in range(BOARD_ROWS)]) or \
            all([board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True

    return False

def ai_move():
    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] is None:
                board[i][j] = 'O'
                if check_win('O'):
                    return i, j
                board[i][j] = None

    for i in range(BOARD_ROWS):
        for j in range(BOARD_COLS):
            if board[i][j] is None:
                board[i][j] = 'X'
                if check_win('X'):
                    board[i][j] = 'O'
                    return i, j
                board[i][j] = None

    empty_cells = [(i, j) for i in range(BOARD_ROWS) for j in range(BOARD_COLS) if board[i][j] == None]
    if empty_cells:
        return random.choice(empty_cells)
    return None


def game_loop(Ai):
    global player
    player = 'X'
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not check_win('X') and not check_win('O'):
                mouseX = event.pos[0]
                mouseY = event.pos[1]
                clicked_row = mouseY // SQUARE_SIZE
                clicked_col = mouseX // SQUARE_SIZE


                if board[clicked_row][clicked_col] == None:
                    board[clicked_row][clicked_col] = player
                    if check_win(player):
                        Winner = player
                        running = False
                    player = 'O' if player == 'X' else 'X'

                    # AI move
                    if Ai and running:
                        player = 'O'
                        ai_row, ai_col = ai_move()
                        if ai_row is not None and ai_col is not None:
                            board[ai_row][ai_col] = 'O'
                            if check_win('O'):
                                Winner = player
                                running = False
                            player = 'X'

        screen.fill(BG_COLOR)
        draw_lines()
        draw_figures()
        pygame.display.update()
    print(f"Player {Winner} wins!")
    Win_Text = font.render(f"Player {Winner} wins!", True, Green)
    Win_textRect = Win_Text.get_rect()
    Win_textRect.center = (WindowSize // 2, WindowSize // 2)
    screen.blit(Win_Text, Win_textRect)
    pygame.display.update()
    time.sleep(2.5)
    screen.fill(BG_COLOR)
    screen.blit(Win_Text, Win_textRect)
    pygame.display.update()
    time.sleep(2)


menu_running = True
M_Stage = 0
Grid_Chose = None
Ai = False
while menu_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_running = False
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            if M_Stage == 0:
                if button_1.rect.collidepoint(mouseX, mouseY):
                    M_Stage = 1
                    Grid_Chose = Chose_1
                elif button_2.rect.collidepoint(mouseX, mouseY):
                    M_Stage = 1
                    Grid_Chose = Chose_2
                elif button_3.rect.collidepoint(mouseX, mouseY):
                    M_Stage = 1
                    Grid_Chose = Chose_3
            elif M_Stage == 1:
                if button_2p.rect.collidepoint(mouseX, mouseY):
                    Ai = False
                    start_game(Grid_Chose, Ai)
                    M_Stage = 0
                    Grid_Chose = None
                elif button_Ai.rect.collidepoint(mouseX, mouseY):
                    Ai = True
                    start_game(Grid_Chose, Ai)
                    M_Stage = 0
                    Grid_Chose = None

    draw_menu(M_Stage)
    pygame.display.update()

