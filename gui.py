"""Отрисовка игры на Pygame."""

import pygame
from game import ROWS, COLS, PLAYER, AI, EMPTY

CELL = 100
RADIUS = CELL // 2 - 8
TOP_MARGIN = CELL
WIDTH = COLS * CELL
HEIGHT = (ROWS + 1) * CELL

BG = (30, 30, 40)
BOARD_BLUE = (30, 90, 200)
BOARD_EDGE = (10, 40, 100)
RED = (220, 60, 60)
YELLOW = (240, 200, 60)
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)


def cell_center(row, col):
    x = col * CELL + CELL // 2
    y = (row + 1) * CELL + CELL // 2
    return x, y


def draw(screen, board, hover_col, win_cells, winner_text, font):
    screen.fill(BG)

    # Поле
    pygame.draw.rect(screen, BOARD_BLUE, (0, CELL, WIDTH, ROWS * CELL))
    pygame.draw.rect(screen, BOARD_EDGE, (0, CELL, WIDTH, ROWS * CELL), 4)

    # Подсветка столбца под курсором
    if hover_col is not None and board.heights[hover_col] >= 0:
        s = pygame.Surface((CELL, ROWS * CELL), pygame.SRCALPHA)
        s.fill((255, 255, 255, 40))
        screen.blit(s, (hover_col * CELL, CELL))

    # Лунки и фишки
    win_set = set(win_cells) if win_cells else set()
    for r in range(ROWS):
        for c in range(COLS):
            x, y = cell_center(r, c)
            pygame.draw.circle(screen, BG, (x, y), RADIUS + 4)
            v = board.grid[r][c]
            if v == EMPTY:
                pygame.draw.circle(screen, (20, 20, 25), (x, y), RADIUS)
            else:
                color = RED if v == PLAYER else YELLOW
                pygame.draw.circle(screen, color, (x, y), RADIUS)
                if (r, c) in win_set:
                    pygame.draw.circle(screen, WHITE, (x, y), RADIUS, 5)

    # Текст победителя
    if winner_text:
        txt = font.render(winner_text, True, WHITE)
        rect = txt.get_rect(center=(WIDTH // 2, CELL // 2))
        screen.blit(txt, rect)


def pixel_to_col(x):
    if 0 <= x < WIDTH:
        return x // CELL
    return None