"""ИИ: Minimax с alpha-beta отсечением и эвристической оценкой."""

import math
import random
from game import Board, PLAYER, AI, ROWS, COLS

WIN_SCORE = 10_000_000


def score_window(window, piece):
    """Оценка окна из 4 клеток."""
    opp = PLAYER if piece == AI else AI
    score = 0
    p = window.count(piece)
    o = window.count(opp)
    e = window.count(0)

    if p == 4:
        score += 100_000
    elif p == 3 and e == 1:
        score += 100
    elif p == 2 and e == 2:
        score += 10
    if o == 3 and e == 1:
        score -= 120
    elif o == 4:
        score -= 100_000
    return score


def evaluate(board, piece):
    """Эвристическая оценка позиции для ИИ."""
    score = 0
    g, R, C = board.grid, board.rows, board.cols

    # Центральные столбцы важнее
    center = [g[r][C // 2] for r in range(R)]
    score += center.count(piece) * 6

    # Горизонтали
    for r in range(R):
        for c in range(C - 3):
            score += score_window([g[r][c + i] for i in range(4)], piece)

    # Вертикали
    for c in range(C):
        for r in range(R - 3):
            score += score_window([g[r + i][c] for i in range(4)], piece)

    # Диагонали ↘
    for r in range(R - 3):
        for c in range(C - 3):
            score += score_window([g[r + i][c + i] for i in range(4)], piece)

    # Диагонали ↗
    for r in range(3, R):
        for c in range(C - 3):
            score += score_window([g[r - i][c + i] for i in range(4)], piece)

    return score


def terminal_score(board, depth):
    if board.check_win(AI):
        return WIN_SCORE + depth  # быстрее — лучше
    if board.check_win(PLAYER):
        return -WIN_SCORE - depth
    return 0


def minimax(board, depth, alpha, beta, maximizing):
    moves = board.valid_moves()

    if board.check_win(AI) or board.check_win(PLAYER) or not moves:
        return terminal_score(board, depth), None

    if depth == 0:
        return evaluate(board, AI), None

    if maximizing:
        best = -math.inf
        best_col = random.choice(moves)
        for col in order_moves(board, moves):
            board.drop(col, AI)
            val, _ = minimax(board, depth - 1, alpha, beta, False)
            board.undo(col)
            if val > best:
                best, best_col = val, col
            alpha = max(alpha, best)
            if alpha >= beta:
                break
        return best, best_col
    else:
        best = math.inf
        best_col = random.choice(moves)
        for col in order_moves(board, moves):
            board.drop(col, PLAYER)
            val, _ = minimax(board, depth - 1, alpha, beta, True)
            board.undo(col)
            if val < best:
                best, best_col = val, col
            beta = min(beta, best)
            if alpha >= beta:
                break
        return best, best_col


def order_moves(board, moves):
    """Центральные ходы рассматриваем первыми — это ускоряет alpha-beta."""
    center = COLS // 2
    return sorted(moves, key=lambda c: abs(c - center))


def best_move(board, depth=5):
    _, col = minimax(board, depth, -math.inf, math.inf, True)
    return col