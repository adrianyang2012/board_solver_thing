import pygame
import sys

pieces= [[2,4],[3,4],[2,2],[1,4],[2,5],[3,3],[2,3],[1,5]]

ROWS, COLS = 8, 8
BLOCKS_NEEDED = 6
CELL_SIZE = 60
MARGIN = 2
WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE + 70  # Extra space for button

# Colors
COLORS = [
    (220, 220, 220),  # empty
    (50, 50, 50),     # blocked
    (255, 100, 100),  # A
    (100, 255, 100),  # B
    (100, 100, 255),  # C
    (255, 255, 100),  # D
    (255, 100, 255),  # E
    (100, 255, 255),  # F
    (200, 150, 100),  # G
    (150, 100, 200),  # H
    (100, 200, 150),  # I
]


def print_board(board):
    symbols = ['.', '#', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    for row in board:
        print(' '.join(symbols[cell] if cell < len(symbols) else str(cell) for cell in row))
    print()

def floodfill(board,piece):
    global pieces
    if piece==8:
        return board
    for i in range(len(board)):
        for j in range(len(board[0])):
            stop = 0
            new_board = [x[:] for x in board]
            for x in range(i,i+pieces[piece][0]):
                for y in range(j,j+pieces[piece][1]):
                    if x>=len(board) or y>=len(board[0]):
                        stop = 1
                        break
                    elif board[x][y]:
                        stop = 1
                        break
                    else:
                        new_board[x][y] = piece+2
                if stop:
                    break
            if not stop:
                a = floodfill(new_board,piece+1)
                if a:
                    return a
    for i in range(len(board)):
        for j in range(len(board[0])):
            stop = 0
            new_board = [x[:] for x in board]
            for x in range(i,i+pieces[piece][1]):
                for y in range(j,j+pieces[piece][0]):
                    if x>=len(board) or y>=len(board[0]):
                        stop = 1
                        break
                    elif board[x][y]:
                        stop = 1
                        break
                    else:
                        new_board[x][y] = piece+2
                if stop:
                    break
            if not stop:
                a = floodfill(new_board,piece+1)
                if a:
                    return a
    return False

def draw_board_pygame(board, blocked_positions, solved=False, show_button=False):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Board Solver Interactive')
    font = pygame.font.SysFont(None, 36)
    button_rect = pygame.Rect(WIDTH//2-130, HEIGHT-60, 120, 40)  # Solve button
    clear_rect = pygame.Rect(WIDTH//2+10, HEIGHT-60, 120, 40)    # Clear button
    running = True
    solution = None
    # Move show_button and solved to local variables so they can be reset
    local_show_button = show_button
    local_solved = solved
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not local_solved and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if my < ROWS * CELL_SIZE:
                    row = my // CELL_SIZE
                    col = mx // CELL_SIZE
                    if (row, col) not in blocked_positions and len(blocked_positions) < BLOCKS_NEEDED:
                        blocked_positions.append((row, col))
                    elif (row, col) in blocked_positions:
                        blocked_positions.remove((row, col))
                elif local_show_button:
                    if button_rect.collidepoint(mx, my):
                        # Solve button clicked
                        board2 = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                        for (i, j) in blocked_positions:
                            board2[i][j] = 1
                        solution = floodfill(board2, 0)
                        if solution:
                            print_board(solution)
                            local_solved = True
                        else:
                            local_solved = True  # Still show board, but indicate no solution
                    elif clear_rect.collidepoint(mx, my):
                        # Clear button clicked
                        blocked_positions.clear()
                        local_solved = False
                        solution = None
                        local_show_button = False
            elif local_solved and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if clear_rect.collidepoint(mx, my):
                    blocked_positions.clear()
                    local_solved = False
                    solution = None
                    local_show_button = False
        screen.fill((30, 30, 30))
        # Draw board
        for i in range(ROWS):
            for j in range(COLS):
                if not local_solved:
                    color = COLORS[1] if (i, j) in blocked_positions else COLORS[0]
                else:
                    if solution:
                        cell = solution[i][j]
                        color = COLORS[cell] if cell < len(COLORS) else (255,255,255)
                    else:
                        color = COLORS[1] if (i, j) in blocked_positions else COLORS[0]
                pygame.draw.rect(
                    screen,
                    color,
                    (j*CELL_SIZE+MARGIN, i*CELL_SIZE+MARGIN, CELL_SIZE-2*MARGIN, CELL_SIZE-2*MARGIN)
                )
        # Draw grid lines
        for i in range(ROWS+1):
            pygame.draw.line(screen, (100,100,100), (0, i*CELL_SIZE), (WIDTH, i*CELL_SIZE))
        for j in range(COLS+1):
            pygame.draw.line(screen, (100,100,100), (j*CELL_SIZE, 0), (j*CELL_SIZE, ROWS*CELL_SIZE))
        # Draw instructions
        if not local_solved:
            if len(blocked_positions) < BLOCKS_NEEDED:
                text = font.render(f"Select {BLOCKS_NEEDED-len(blocked_positions)} blocked squares", True, (255,255,255))
                screen.blit(text, (20, HEIGHT-60))
                local_show_button = False
            else:
                local_show_button = True
        # Draw Solve button
        if local_show_button and not local_solved:
            pygame.draw.rect(screen, (70, 170, 70), button_rect)
            btn_text = font.render("Solve", True, (255,255,255))
            screen.blit(btn_text, (button_rect.x+20, button_rect.y+5))
            # Draw Clear button
            pygame.draw.rect(screen, (170, 70, 70), clear_rect)
            clr_text = font.render("Clear", True, (255,255,255))
            screen.blit(clr_text, (clear_rect.x+20, clear_rect.y+5))
        # Draw result
        if local_solved:
            if solution:
                text = font.render("Solved!", True, (70, 255, 70))
            else:
                text = font.render("No solution found.", True, (255, 70, 70))
            screen.blit(text, (20, HEIGHT-60))
            # Draw Clear button even after solving
            pygame.draw.rect(screen, (170, 70, 70), clear_rect)
            clr_text = font.render("Clear", True, (255,255,255))
            screen.blit(clr_text, (clear_rect.x+20, clear_rect.y+5))
        pygame.display.flip()

def main():
    draw_board_pygame(
        board=[[0 for _ in range(COLS)] for _ in range(ROWS)],
        blocked_positions=[],
        solved=False,
        show_button=False
    )

if __name__ == "__main__":
    main()
