import random
import time

class BotMinimax_3x3:
    def __init__(self, bot_mark):
        self.bot = bot_mark
        self.opponent = bot_mark * -1

    def _minmax(self, board_object, current_player_mark):
        result = board_object.check_winner()
        if result == 'draw':
            return 0
        elif result == self.bot:
            return 1
        elif result is not None:
            return -1

        best_res = -100 if current_player_mark == self.bot else 100
        
        for move in board_object.get_legal_moves(current_player_mark):
            # Używamy clone() zamiast psucia planszy oryginalnej
            board_copy = board_object.clone()
            board_copy.make_move(move, current_player_mark)
            
            res = self._minmax(board_copy, current_player_mark * -1)
            
            if current_player_mark == self.bot:
                best_res = max(best_res, res)
            else:
                best_res = min(best_res, res)
                
        return best_res

    def find_best_move(self, board_object):
        best_result = -100
        best_move = None

        for move in board_object.get_legal_moves(self.bot):
            board_copy = board_object.clone()
            board_copy.make_move(move, self.bot) 
            
            result = self._minmax(board_copy, self.opponent) 
            
            if result > best_result:
                best_result = result
                best_move = move

        return best_move




class BotMonteCarlo:
    def __init__(self, bot_mark, simulations):
        self.bot = bot_mark
        self.simulations = simulations



    def _simulate_game(self, board_copy, current_player):
        while True:
            result = board_copy.check_winner()
            if result is not None:
                if result == self.bot:
                    return 1
                elif result == (self.bot * -1):
                    return -1
                else:
                    return 0
                
            legal_moves = board_copy.get_legal_moves(current_player)
            if legal_moves == []:
                current_player *= -1
                continue

            random_move = random.choice(legal_moves)
            board_copy.make_move(random_move, current_player)
            current_player *= -1



    def find_best_move(self, board_object):
        best_move = None
        best_result = -999999
        get_legal_moves = board_object.get_legal_moves(self.bot)

        for move in get_legal_moves:
            sum_of_points = 0

            for _ in range(self.simulations):
                board_copy = board_object.clone()
                board_copy.make_move(move, self.bot)
                sum_of_points += self._simulate_game(board_copy, self.bot * -1) 
            if sum_of_points > best_result:
                best_result = sum_of_points
                best_move = move

        return best_move



