import pygame
import sys
import sudoku
import cProfile
import pstats
from string import digits

draw_rect = sudoku.draw_rect
EDGES_COLOR = (0, 0, 0)
CHOSEN_COLOR = (204, 204, 204)
CELL_COLOR = (255, 255, 255)
NUMBERS_COLOR = (0, 0, 0)
WINDOW_HEIGHT = 500
WINDOW_WIDTH = 800
BLOCK_SIZE = min(WINDOW_HEIGHT, WINDOW_WIDTH) // 9
MARGIN = 3
WINDOW_HEIGHT = BLOCK_SIZE * 9 + MARGIN * 2
WINDOW_WIDTH = BLOCK_SIZE * 9 + MARGIN * 2


def solve_game(board, visualisation):
    board.solve(visualisation)


def update_screen(screen, all_cells, prev_chosen, number_font):
    for index_row, row in enumerate(all_cells):
        for index_col, item in enumerate(row):
            rect, color = item[0]
            num = item[1]
            if prev_chosen and prev_chosen == (index_row, index_col):
                draw_rect(screen, CHOSEN_COLOR, EDGES_COLOR, rect)
            else:
                draw_rect(screen, CELL_COLOR, EDGES_COLOR, rect)
            if num:
                text_width, text_height = number_font.size(num)
                screen.blit(number_font.render(num, True, NUMBERS_COLOR),
                            (rect[0] + rect[2] // 2 - text_width / 2, rect[1] + rect[3] // 2 - text_height / 2))
    pygame.display.flip()
    pygame.display.update()


def event_handler(all_cells, prev_chosen, visualisation, board=None):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            for index_row, row in enumerate(all_cells):
                for index_col, item in enumerate(row):
                    rect, color = item[0]
                    if rect.collidepoint(event.pos):
                        if prev_chosen == (index_row, index_col):
                            prev_chosen = ()
                            continue
                        prev_chosen = (index_row, index_col)
        if event.type == pygame.KEYDOWN:
            if event.unicode and event.unicode in digits:
                key_down = event.unicode
                if prev_chosen:
                    x = prev_chosen[0]
                    y = prev_chosen[1]
                    if key_down == '0':
                        key_down = ''
                    all_cells[x][y][-1] = key_down
                    board.board[x][y] = None
                    if key_down:
                        board.board[x][y] = int(key_down)


            elif event.key == pygame.K_LCTRL:
                pygame.display.set_caption("Not Visualization")
                visualisation[0] = not visualisation[0]
                if visualisation[0] is True:
                    pygame.display.set_caption("Visualization")

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == pygame.K_SPACE:
                prev_chosen = ()
                with cProfile.Profile() as pr:
                    solve_game(board, visualisation[0])
                stats = pstats.Stats(pr)
                stats.sort_stats(pstats.SortKey.TIME)
                stats.print_stats()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    return prev_chosen


def main():
    pygame.init()
    board_values = [[9, 5, None, None, 1, None, 2, None, None], [None, 8, None, None, None, 7, None, 9, None],
                    [6, None, 2, None, None, None, 5, None, None], [None, 7, None, None, 6, None, None, None, None],
                    [None, None, None, 9, None, 1, None, None, None], [None, None, None, None, 2, None, None, 4, None],
                    [None, None, 5, None, None, None, 6, None, 3], [None, 9, None, 4, None, None, None, 7, None],
                    [None, None, 6, None, None, None, None, None, None]]
    board = sudoku.Board.constructor(board_values)

    screen, all_cells, number_font = board.init_gui(WINDOW_WIDTH, WINDOW_HEIGHT, BLOCK_SIZE, MARGIN)
    prev_chosen = ()
    visualisation = [False]
    pygame.display.set_caption("No Visualization")
    while True:
        prev_chosen = event_handler(all_cells, prev_chosen, visualisation, board)
        update_screen(screen, all_cells, prev_chosen, number_font)


if __name__ == '__main__':
    main()
