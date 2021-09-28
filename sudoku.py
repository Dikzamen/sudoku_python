import pygame

EDGES_COLOR = (0, 0, 0)
CHOSEN_COLOR = (204, 204, 204)
CELL_COLOR = (255, 255, 255)
NUMBERS_COLOR = (0, 0, 0)

def draw_rect(surface, fill_color, outline_color, rect, border=1):
    surface.fill(outline_color, rect)
    surface.fill(fill_color, rect.inflate(-border * 2, -border * 2))


def animate(function):
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        self = args[0]
        if self.gui_active:
            number = args[3]
            i = args[1]
            j = args[2]
            self.gui_board[i][j][-1] = number
            if number is not None:
                self.gui_board[i][j][-1] = str(number)
            if self.visualisation:
                self.update_screen_((i, j))
                element = self.gui_board[i][j]
                pair = element[0]
                rect = pair[0]
                pygame.display.update(rect)
            pygame.event.pump()
        return result

    return wrapper


def init_cells(board, window_width, window_height, block_size, margin):
    all_cells = []
    for index_y, y in enumerate(range(0, window_height, block_size)):
        if index_y == 9:
            break
        row = []
        for index_x, x in enumerate(range(0, window_width, block_size)):
            if index_x == 9:
                break
            rect = pygame.Rect(x + (index_x // 3) * margin, y + (index_y // 3) * margin, block_size - 1, block_size - 1)
            if board and board[index_y][index_x]:
                row.append([[rect, CELL_COLOR], str(board[index_y][index_x])])
            else:
                row.append([[rect, CELL_COLOR], ''])
        all_cells.append(row)
    return all_cells


class Board:

    def update_screen_(self, cell=None):
        text_width, text_height = self.text_width, self.text_height
        if cell is not None:
            item = self.gui_board[cell[0]][cell[1]]
            rect, color = item[0]
            num = item[1]

            draw_rect(self.SCREEN, CELL_COLOR, EDGES_COLOR, rect)
            if num:
                self.SCREEN.blit(self.numbers_rendered[int(num) - 1],
                                 (rect[0] + rect[2] // 2 - text_width / 2, rect[1] + rect[3] // 2 - text_height / 2))
            return

        for index_row, row in enumerate(self.gui_board):
            for index_col, item in enumerate(row):
                rect, color = item[0]
                num = item[1]
                draw_rect(self.SCREEN, CELL_COLOR, EDGES_COLOR, rect)
                if num:
                    self.SCREEN.blit(self.numbers_rendered[int(num) - 1],
                                     (rect[0] + rect[2] // 2 - text_width / 2,
                                      rect[1] + rect[3] // 2 - text_height / 2))

    def init_gui(self, window_width, window_height, block_size, margin):
        self.gui_active = True
        self.SCREEN = pygame.display.set_mode((window_width, window_height))
        self.SCREEN.fill(CELL_COLOR)
        self.gui_board = init_cells(self.board, window_width, window_height, block_size, margin)
        self.font = pygame.font.SysFont('Calibri', int(block_size // 1.5))
        self.text_width, self.text_height = self.font.size('1')
        self.prev_chosen = ()
        self.numbers_rendered = [self.font.render(str(num), True, NUMBERS_COLOR) for num in range(1, 10)]
        return self.SCREEN, self.gui_board, self.font

    def __init__(self):
        self.board = []
        self.visualisation = False
        for _ in range(9):
            self.board.append([None, None, None, None, None, None, None, None, None])
        self.SCREEN = None
        self.gui_board = None
        self.font = None
        self.text_width = self.text_height = None
        self.prev_chosen = ()
        self.gui_active = False
        self.numbers_rendered = None

    @classmethod
    def constructor(cls, numbers):
        board = cls()
        board.board = numbers
        return board

    def __len__(self):
        return len(self.board)

    def __str__(self):
        result = ''
        for i in range(9):
            for j in range(9):
                if not j % 3:
                    result += ' | '
                if self.board[i][j] is None:
                    result += '   '
                else:
                    result += f' {self.board[i][j]} '
            result += "\n"
            if not (i + 1) % 3:
                result += ' _ ' * 12
                result += '\n'
        return result

    def __repr__(self):
        return self.__str__()

    def __setitem__(self, item, value):
        print('setting item', item, value)
        # return self.board[item]

    def __getitem__(self, item):
        print('getting item', item)
        return self.board[item]

    def numbers_in_row(self, i):
        return [cell for cell in self.board[i] if cell is not None]

    def numbers_in_col(self, i):
        return [cell for cell in list(zip(*self.board))[i] if cell is not None]

    def numbers_in_square(self, i, j):
        lst = []
        for row in range((i // 3) * 3, (i // 3) * 3 + 3):
            lst.extend(self.board[row][(j // 3) * 3:(j // 3) * 3 + 3])
        return [cell for cell in lst if cell is not None]

    def get_number_for_cell(self, i, j):
        lst = [*self.numbers_in_col(j), *self.numbers_in_row(i), *self.numbers_in_square(i, j)]
        numbers = [i for i in range(1, 10) if i not in lst]
        return numbers

    def next_cell(self, i, j):
        try:
            _ = self.board[i][j + 1]
            indexes = i, j + 1
        except IndexError:
            try:
                _ = self.board[i + 1][0]
                indexes = i + 1, 0
            except IndexError:
                return None
        if self.board[indexes[0]][indexes[1]] is not None:
            return self.next_cell(indexes[0], indexes[1])
        return indexes

    @animate
    def set_value_cell(self, i, j, number):
        self.board[i][j] = number

    def solve_for_cell(self, i, j):
        if self.board[i][j] is not None:
            next_cell = self.next_cell(i, j)
            res = self.solve_for_cell(next_cell[0], next_cell[1])
            if res:
                return True
            if not res:
                return False
        numbers_for_cell = self.get_number_for_cell(i, j)
        if not numbers_for_cell:
            return False
        for number in numbers_for_cell:
            self.set_value_cell(i, j, number)
            next_cell = self.next_cell(i, j)
            if next_cell is None:
                return True
            res = self.solve_for_cell(next_cell[0], next_cell[1])
            if res:
                return True
            if not res:
                self.set_value_cell(i, j, None)
        return False

    def solve(self, visualisation):
        self.visualisation = visualisation
        self.solve_for_cell(0, 0)


if __name__ == '__main__':
    ex = [[9, 5, None, None, 1, None, 2, None, None], [None, 8, None, None, None, 7, None, 9, None],
          [6, None, 2, None, None, None, 5, None, None], [None, 7, None, None, 6, None, None, None, None],
          [None, None, None, 9, None, 1, None, None, None], [None, None, None, None, 2, None, None, 4, None],
          [None, None, 5, None, None, None, 6, None, 3], [None, 9, None, 4, None, None, None, 7, None],
          [None, None, 6, None, None, None, None, None, None]]

    board = Board.constructor(ex)
    print(board)
    board.solve(False)
    print(board)
