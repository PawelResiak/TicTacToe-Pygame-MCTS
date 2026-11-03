import time
from board import OthelloBoard, MNKBoard
from ai import BotMonteCarlo

def run_arena(num_games):

    stats = {
        'bot1': {'B': 0, 'W': 0, 'total': 0},
        'bot2': {'B': 0, 'W': 0, 'total': 0},
        'draws': 0
    }
    total_time = 0

    for i in range(num_games):
        if i % 2 == 0:
            bot1 = BotMonteCarlo('B', 10)
            bot2 = BotMonteCarlo('W', 10)
        else:
            bot1 = BotMonteCarlo('W', 10)
            bot2 = BotMonteCarlo('B', 10)

        board = OthelloBoard()

        active_bot = bot1 if bot1.bot == 'B' else bot2
        start_time = time.time()
        print(f"round {i+1}")
        while True:
            result = board.check_winner()
            if result is not None:
                if result == 'draw':
                    stats['draws'] += 1
                else:
                    if bot1.bot == result:
                        stats['bot1'][result] += 1
                        stats['bot1']['total'] += 1
                    else:
                        stats['bot2'][result] += 1
                        stats['bot2']['total'] += 1
                break

            if not board.get_legal_moves(active_bot.bot):
                active_bot = bot1 if active_bot == bot2 else bot2
                continue

            index = active_bot.find_best_move(board)
            board.make_move(index, active_bot.bot)

            #if self.game_choice == 1:
                #self.current_player_mark = "O" if self.current_player_mark == "X" else "X"
            #else:
                #self.current_player_mark = "W" if self.current_player_mark == "B" else "B"
            #continue

            active_bot = bot1 if active_bot == bot2 else bot2


        game_duration = time.time() - start_time
        total_time += game_duration


    print("\n=== WYNIKI ARENY ===")
    print(f"Średni czas partii: {total_time / num_games:.2f}s")
    for b in ['bot1', 'bot2']:
        print(f"{b.upper()}: {stats[b]['total']} wygranych (B: {stats[b]['B']}, W: {stats[b]['W']})")
    print(f"Remisy: {stats['draws']}")


if __name__ == "__main__":
    run_arena(10)