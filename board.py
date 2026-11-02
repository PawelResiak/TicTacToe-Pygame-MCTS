from abc import ABC, abstractmethod
from collections import Counter

class BaseBoard(ABC):
    
    @abstractmethod
    def get_legal_moves(self, player_mark) -> list:
        pass

    @abstractmethod
    def make_move(self, move, player_mark) -> None:
        pass

    @abstractmethod
    def check_winner(self) -> str:
        pass

    @abstractmethod
    def clone(self):
        pass





class MNKBoard(BaseBoard):
    def __init__(self, width, height, win_streak):
        self.width = width
        self.height = height
        self.win_streak = win_streak
        self.grid = [' ']* (self.height * self.width)
        self.winning_lines = self.winning_lines()

    def winning_lines(self):
        width = self.width
        height = self.height
        win_streak = self.win_streak

        horizontal = [tuple(width * y + x + k for k in range(win_streak)) 
                for y in range(height) for x in range(width - win_streak + 1)]

        vertical = [tuple(width * (y + k) + x for k in range(win_streak)) 
                for y in range(height - win_streak + 1) for x in range(width)]

        diag_1 = [tuple(width * (y + k) + (x + k) for k in range(win_streak)) 
                    for y in range(height - win_streak + 1) for x in range(width - win_streak + 1)]

        diag_2 = [tuple(width * (y - k) + (x + k) for k in range(win_streak)) 
                    for y in range(win_streak - 1, height) for x in range(width - win_streak + 1)]

        return horizontal + vertical + diag_1 + diag_2

    def display_console(self):
        separator = '-' * (4 * self.width +1) + '\n'
        
        grid = separator
        for y in range(self.height):
            row = '|'
            for x in range(self.width):
                row += f' {self.grid[x + (y * self.width)]} |'
            grid += row + '\n' + separator
            
        print(grid, end='')

    def get_legal_moves(self, player_mark=None):
        return [x for x in range(self.height*self.width) if self.grid[x] == ' ']

    def check_winner(self):
        for line in self.winning_lines:
            first_mark = self.grid[line[0]]
            if first_mark != ' ':
                if all(self.grid[index] == first_mark for index in line):
                    return first_mark
                
        if len(self.get_legal_moves()) == 0:
            return 'draw'
            
        return None

    def make_move(self, index, player_mark):
        self.grid[index] = player_mark

    def clone(self):
        new_board = MNKBoard(self.width, self.height, self.win_streak)
        new_board.grid = self.grid.copy()
        return new_board







class OthelloBoard(BaseBoard):
    def __init__(self):
        self.grid = [' '] * 64

        # Standard Othello starting position in the center
        self.grid[3 * 8 + 3] = 'W'
        self.grid[3 * 8 + 4] = 'B'
        self.grid[4 * 8 + 3] = 'B'
        self.grid[4 * 8 + 4] = 'W'

    def get_legal_moves(self, player_mark):
        result = []
        for index in range(64):
            if self.grid[index] == ' ': # To make it faster
                if self._get_flipped_discs(index, player_mark):
                    result.append(index)
        return result


    def make_move(self, index, player_mark):
        to_flip = self._get_flipped_discs(index, player_mark)
        for spot in to_flip:
            self.grid[spot] = player_mark
        self.grid[index] = player_mark


    def check_winner(self):
        legal_w = self.get_legal_moves('W')
        legal_b = self.get_legal_moves('B')

        if len(legal_w) == 0 and len(legal_b) == 0:
            
            counter = Counter(self.grid)
            
            if counter['W'] > counter['B']:
                return 'W'
            elif counter['B'] > counter['W']:
                return 'B'
            else:
                return 'draw'
            
        return None

            
    def clone(self):
        new_board = OthelloBoard()
        new_board.grid = self.grid.copy()
        return new_board


    def _get_flipped_discs(self, index, player_mark):
        if self.grid[index] != ' ':
            return []

        opponent = 'B' if player_mark == 'W' else 'W'

        row = index // 8
        col = index % 8

        flipped = []

        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for d_row, d_col in directions:
            path = []
            r, c = row + d_row, col + d_col

            while 0 <= r < 8 and 0 <= c < 8 and self.grid[r * 8 + c] == opponent:
                path.append(r * 8 + c)
                r += d_row
                c += d_col

            if path and 0 <= r < 8 and 0 <= c < 8 and self.grid[r * 8 + c] == player_mark:
                flipped.extend(path)

        return flipped