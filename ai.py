import random
import time

class BotMinimax_3x3:
    def __init__(self, bot_mark):
        self.bot = bot_mark
        self.opponent_mark = 'X' if bot_mark == 'O' else "O"


        
    def _minmax(self, board_object, current_player_mark):
        result = board_object.check_winner()
        if result == 'draw':
            return 0
        elif result == self.bot:
            return 1
        elif result is not None and result != self.bot:
            return -1

        movey = board_object.get_legal_moves(current_player_mark)
        resulti = []
        for move in movey:
            board_object.make_move(move, current_player_mark)
            kolejny_player_mark = "X" if current_player_mark == "O" else "O"
            result = self._minmax(board_object, kolejny_player_mark)
            resulti.append(result)
            board_object.make_move(move, " ")

        if current_player_mark == self.bot:
            return max(resulti)
        else:
            return min(resulti)



    def find_best_move(self, board_object):
        best_result = -100
        best_move = None

        for move in board_object.get_legal_moves(self.bot):
            board_object.make_move(move, self.bot)  
            result = self._minmax(board_object, self.opponent_mark) 
            board_object.make_move(move, " ")  

            if result > best_result:
                best_result = result
                best_move = move

        return best_move




class BotMonteCarlo:
    def __init__(self, bot_mark, time_for_move):
        self.bot = bot_mark
        self.time_for_move = time_for_move
        if bot_mark == 'O':
            self.opponent_mark = 'X'
        elif bot_mark == 'X':
            self.opponent_mark = 'O'
        elif bot_mark == 'B':
            self.opponent_mark = 'W'
        else:
            self.opponent_mark = 'B'



    def _simulate_game(self, board_copy, current_player_mark):
        while True:
            result = board_copy.check_winner()
            if result == 'draw':
                return 0
            elif result == self.bot:
                return 1
            elif result is not None and result != self.bot:
                return -1
            legal_moves = board_copy.get_legal_moves(current_player_mark)
            if legal_moves == []:
                current_player_mark = self.opponent_mark if current_player_mark == self.bot else self.bot
                continue

            random_move = random.choice(legal_moves)
            board_copy.make_move(random_move, current_player_mark)
            current_player_mark = self.opponent_mark if current_player_mark == self.bot else self.bot



    def find_best_move(self, board_object):
        best_move = None
        best_result = -999999
        get_legal_moves = board_object.get_legal_moves(self.bot)
        time_for_move = self.time_for_move / len(get_legal_moves)
        for move in get_legal_moves:
            sum_of_points = 0
            start_time = time.time()
            while time.time() - start_time < time_for_move:
                board_copy = board_object.clone()
                board_copy.make_move(move, self.bot)
                sum_of_points += self._simulate_game(board_copy, self.opponent_mark)
            if sum_of_points > best_result:
                best_result = sum_of_points
                best_move = move

        return best_move



