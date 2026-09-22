import sys
import pygame
from game import Board, PLAYER, AI, EMPTY
from ai import best_move
from gui import draw, pixel_to_col, WIDTH, HEIGHT, CELL

AI_DEPTH = 5  # глубина поиска ИИ


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Четыре в ряд")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 36, bold=True)

    board = Board()
    turn = PLAYER
    winner_text = ""
    win_cells = None
    game_over = False
    ai_thinking = False
    ai_timer = 0

    running = True
    while running:
        hover_col = None
        mx, my = pygame.mouse.get_pos()
        if not game_over:
            hover_col = pixel_to_col(mx)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                board = Board()
                turn = PLAYER
                winner_text = ""
                win_cells = None
                game_over = False
            elif (event.type == pygame.MOUSEBUTTONDOWN
                  and event.button == 1
                  and not game_over
                  and turn == PLAYER):
                col = pixel_to_col(mx)
                if col is not None and board.heights[col] >= 0:
                    board.drop(col, PLAYER)
                    if board.check_win(PLAYER):
                        win_cells = board.check_win(PLAYER)
                        winner_text = "Вы победили! (R — заново)"
                        game_over = True
                    elif board.is_full():
                        winner_text = "Ничья! (R — заново)"
                        game_over = True
                    else:
                        turn = AI
                        ai_thinking = True
                        ai_timer = pygame.time.get_ticks()

        # Ход ИИ (с небольшой задержкой для анимации)
        if ai_thinking and not game_over:
            if pygame.time.get_ticks() - ai_timer > 350:
                col = best_move(board, AI_DEPTH)
                if col is not None:
                    board.drop(col, AI)
                    if board.check_win(AI):
                        win_cells = board.check_win(AI)
                        winner_text = "ИИ победил! (R — заново)"
                        game_over = True
                    elif board.is_full():
                        winner_text = "Ничья! (R — заново)"
                        game_over = True
                    else:
                        turn = PLAYER
                ai_thinking = False

        draw(screen, board, hover_col, win_cells, winner_text, font)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()