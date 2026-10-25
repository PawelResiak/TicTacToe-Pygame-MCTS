from abc import ABC, abstractmethod

class BaseBoard(ABC):
    
    @abstractmethod
    def get_legal_moves(self) -> list:
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

    def get_legal_moves(self):
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