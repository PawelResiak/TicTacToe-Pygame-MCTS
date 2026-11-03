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







class OthelloBitboard(BaseBoard):
    def __init__(self):

        self.white_pieces = (1<<27) | (1<<36)
        self.black_pieces = (1<<28) | (1<<35)

    def clone(self):
        new_board = OthelloBitboard()
        new_board.white_pieces = self.white_pieces
        new_board.black_pieces = self.black_pieces
        return new_board

    def get_legal_moves(self, player_mark):
        result = []
        occupied = self.black_pieces | self.white_pieces

        for index in range(64):
            if not (occupied & (1 << index)):
                if self._get_flipped_discs(index, player_mark) > 0:
                    result.append(index)
        return result


    def make_move(self, index, player_mark):
        flipped = self._get_flipped_discs(index, player_mark)
        move_mask = (1 << index) | flipped

        if player_mark == 'B':
            self.black_pieces |= move_mask
            self.white_pieces &= ~flipped
        else:
            self.white_pieces |= move_mask
            self.black_pieces &= ~flipped


    def check_winner(self):
        legal_w = self.get_legal_moves('W')
        legal_b = self.get_legal_moves('B')

        if len(legal_w) == 0 and len(legal_b) == 0:

            w_count = self.white_pieces.bit_count()
            b_count = self.black_pieces.bit_count()
            
            if w_count > b_count: return 'W'
            elif b_count > w_count: return 'B'
            else: return 'draw'
            
        return None



    def _get_flipped_discs(self, index, player_mark):
        my_pieces = self.black_pieces if player_mark == 'B' else self.white_pieces
        opp_pieces = self.white_pieces if player_mark == 'B' else self.black_pieces
        
        occupied = my_pieces | opp_pieces
        if occupied & (1 << index):
            return 0


        row = index // 8
        col = index % 8

        flipped = 0

        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]

        for d_row, d_col in directions:
            path = 0
            r, c = row + d_row, col + d_col

            while 0 <= r < 8 and 0 <= c < 8:
                current_bit = 1 << (r * 8 + c)
                if opp_pieces & current_bit:
                    path |= current_bit
                    r += d_row
                    c += d_col
                elif (my_pieces & current_bit) and path > 0:
                    flipped |= path
                    break
                else:
                    break


        return flipped