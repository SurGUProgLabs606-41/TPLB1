ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2


class Board:
    def __init__(self, rows=ROWS, cols=COLS):
        self.rows = rows
        self.cols = cols
        self.grid = [[EMPTY] * cols for _ in range(rows)]
        self.heights = [rows - 1] * cols  # первая свободная строка в столбце

    # Полная копия доски (minmax)
    def copy(self):
        b = Board(self.rows, self.cols)
        b.grid = [row[:] for row in self.grid]
        b.heights = self.heights[:]
        return b
    
    # Не заполненые столбцы
    def valid_moves(self):
        return [c for c in range(self.cols) if self.heights[c] >= 0]

    # Кладёт фишку в столбец, возвращает строку
    def drop(self, col, piece):
        row = self.heights[col]
        if row < 0:
            return None
        self.grid[row][col] = piece
        self.heights[col] -= 1
        return row

    # Откатывает последний ход (minmax)
    def undo(self, col):
        row = self.heights[col] + 1
        self.grid[row][col] = EMPTY
        self.heights[col] = row

    # Все ли столбцы заполнены
    def is_full(self):
        return all(h < 0 for h in self.heights)

    # Ищет 4 в ряд по горизонтали, вертикали и двум диагоналям; возвращает список клеток-победителей или None
    def check_win(self, piece):
        # Возвращает список выигрышных клеток [(r,c), ...] или None.
        g, R, C = self.grid, self.rows, self.cols

        # Горизонталь
        for r in range(R):
            for c in range(C - 3):
                if all(g[r][c + i] == piece for i in range(4)):
                    return [(r, c + i) for i in range(4)]

        # Вертикаль
        for r in range(R - 3):
            for c in range(C):
                if all(g[r + i][c] == piece for i in range(4)):
                    return [(r + i, c) for i in range(4)]

        # Диагональ ↘
        for r in range(R - 3):
            for c in range(C - 3):
                if all(g[r + i][c + i] == piece for i in range(4)):
                    return [(r + i, c + i) for i in range(4)]

        # Диагональ ↗
        for r in range(3, R):
            for c in range(C - 3):
                if all(g[r - i][c + i] == piece for i in range(4)):
                    return [(r - i, c + i) for i in range(4)]

        return None