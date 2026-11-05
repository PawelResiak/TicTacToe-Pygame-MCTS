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





class MNKBitboard(BaseBoard):
    def __init__(self, width, height, win_streak):
        self.width = width
        self.height = height
        self.win_streak = win_streak
        self.size = width * height
        self.x_pieces = 0
        self.o_pieces = 0
        self.last_move = None
        self.last_mark = None

        lines = self._generate_winning_lines()
        self.masks_by_cell = {i: [] for i in range(self.size)}
        for line in lines:
            mask = 0
            for idx in line:
                mask |= (1 << idx)
            for idx in line:
                self.masks_by_cell[idx].append(mask)

    def _generate_winning_lines(self):
        w, h, s = self.width, self.height, self.win_streak
        lines = []

        for y in range(h):
            for x in range(w - s + 1):
                lines.append([w * y + x + k for k in range(s)])
        for y in range(h - s + 1):
            for x in range(w):
                lines.append([w * (y + k) + x for k in range(s)])
        for y in range(h - s + 1):
            for x in range(w - s + 1):
                lines.append([w * (y + k) + (x + k) for k in range(s)])
        for y in range(s - 1, h):
            for x in range(w - s + 1):
                lines.append([w * (y - k) + (x + k) for k in range(s)])
        return lines

    @property
    def grid(self):
        visual_grid = [' '] * self.size
        for i in range(self.size):
            if self.x_pieces & (1 << i):
                visual_grid[i] = 'X'
            elif self.o_pieces & (1 << i):
                visual_grid[i] = 'O'
        return visual_grid

    def get_legal_moves(self, player_mark=None):
        occupied = self.x_pieces | self.o_pieces
        return [i for i in range(self.size) if not (occupied & (1 << i))]

    def make_move(self, index, player_mark):
        if player_mark == 1:
            self.x_pieces |= (1 << index)
        else:
            self.o_pieces |= (1 << index)
            
        self.last_move = index
        self.last_mark = player_mark

    def check_winner(self):
        if self.last_move is not None:
            pieces = self.x_pieces if self.last_mark == 1 else self.o_pieces
            for mask in self.masks_by_cell[self.last_move]:
                if (pieces & mask) == mask:
                    return self.last_mark
        
        if (self.x_pieces | self.o_pieces) == (1 << self.size) - 1:
            return 'draw'
            
        return None

    def clone(self):
        new_board = MNKBitboard(self.width, self.height, self.win_streak)
        new_board.x_pieces = self.x_pieces
        new_board.o_pieces = self.o_pieces
        new_board.last_move = self.last_move
        new_board.last_mark = self.last_mark
        new_board.masks_by_cell = self.masks_by_cell 
        return new_board







class OthelloBitboard(BaseBoard):
    def __init__(self):
        self.white_pieces = (1<<27) | (1<<36)
        self.black_pieces = (1<<28) | (1<<35)

    @property
    def grid(self):
        visual_grid = [' '] * 64
        for i in range(64):
            if self.black_pieces & (1 << i):
                visual_grid[i] = 'B'
            elif self.white_pieces & (1 << i):
                visual_grid[i] = 'W'
        return visual_grid

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

        if player_mark == 1:
            self.black_pieces |= move_mask
            self.white_pieces &= ~flipped
        else:
            self.white_pieces |= move_mask
            self.black_pieces &= ~flipped


    def check_winner(self):
        legal_w = self.get_legal_moves(1)
        legal_b = self.get_legal_moves(-1)

        if len(legal_w) == 0 and len(legal_b) == 0:

            w_count = self.white_pieces.bit_count()
            b_count = self.black_pieces.bit_count()
            
            if w_count > b_count: return -1
            elif b_count > w_count: return 1
            else: return 'draw'
            
        return None



    def _get_flipped_discs(self, index, player_mark):
        my_pieces = self.black_pieces if player_mark == 1 else self.white_pieces
        opp_pieces = self.white_pieces if player_mark == 1 else self.black_pieces
        
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