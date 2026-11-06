import pygame

from gui import GameView
from board import MNKBitboard, OthelloBitboard #, Connect4Bitboard
from ai import BotMinimax_3x3, BotMonteCarlo
         

class Game:
    def __init__(self):
        pygame.init()
        self.interface = GameView()

        # --- STATE MACHINE --- 
        self.state = 'MAIN_MENU'

        # --- MAIN MENU - CHOOSE GAME ---
        self.selected_game = None # Othello, XO, Gomoku, Connect4

        # --- GAME SETUP ---
        self.game_mode = None
        self.player_1_type = 'HUMAN'
        self.player_2_type = 'BOT'
        self.bot_mark = None
        self.difficulty_level = None
        self.time_setting = None

        # --- VISUALS ---
        self.board_color = 'CLASSIC'
        self.show_possible_moves = True

        # --- GAME ENGINE ---
        self.board = None
        self.current_player_mark = 1
        self.move_history = []
        self.simulations_config = {1: 10, 2:50, 3:150}

    # --- GAME LOOP ---
    def run(self):
        while True:
            if self.state == 'MAIN_MENU':
                self.handle_main_menu()
            elif self.state == 'SETUP_MENU':
                self.handle_setup_menu()
            elif self.state == 'PLAYING':
                self.handle_playing()
            elif self.state == 'END_SCREEN':
                self.handle_end_screen()
            elif self.state == 'QUIT':
                break

        pygame.quit()


    def handle_main_menu(self):
        choice = self.interface.show_main_menu()
        if choice == 'QUIT':
            self.state = 'QUIT'
        else:
            self.selected_game = choice
            self.state = 'SETUP_MENU'

    def handle_setup_menu(self):
        settings = self.interface.show_setup_menu(self.selected_game)

        if settings == 'QUIT':
            self.state = 'QUIT'
        elif settings == 'BACK':
            self.state = 'MAIN_MENU'
        else:
            self.game_mode, bot_color, diff_pack, self.time_setting = settings

            if bot_color in ['X', 'B', 'RED']:
                self.bot_mark = 1
            else:
                self.bot_mark = -1

            # Transformacja: diff_pack staje się słownikiem {numer_gracza: poziom}
            if self.game_mode == 'PvP':
                self.player_1_type = 'HUMAN'
                self.player_2_type = 'HUMAN'
                self.difficulty_level = {}
            elif self.game_mode == 'PvE':
                self.player_1_type = 'BOT' if self.bot_mark == 1 else 'HUMAN'
                self.player_2_type = 'HUMAN' if self.bot_mark == 1 else 'BOT'
                self.difficulty_level = {self.bot_mark: diff_pack}
            elif self.game_mode == 'CvC':
                self.player_1_type = 'BOT'
                self.player_2_type = 'BOT'
                self.difficulty_level = diff_pack # diff_pack z GUI to już {1: trudnosc, -1: trudnosc}

            if self.selected_game == 'TicTacToe':
                self.board = MNKBitboard(3, 3, 3)
            elif self.selected_game == 'Gomoku19':
                self.board = MNKBitboard(19, 19, 5)
            elif self.selected_game == 'Gomoku15':
                self.board = MNKBitboard(15, 15, 5)
            elif self.selected_game == 'TicTacToe5':
                self.board = MNKBitboard(5, 5, 4)
            elif self.selected_game == 'Othello':
                self.board = OthelloBitboard()

            self.current_player_mark = 1
            self.move_history = []
            self.state = 'PLAYING'

    def handle_playing(self):
        # 1. Rysujemy najświeższą planszę
        score = None
        if self.selected_game == 'Othello':
            w_count = self.board.white_pieces.bit_count()
            b_count = self.board.black_pieces.bit_count()
            score = (b_count, w_count)

        self.interface.refresh_screen(
            self.board,
            self.board_color,
            self.show_possible_moves,
            self.current_player_mark,
            len(self.move_history) > 0,
            score,
            self.player_1_type,
            self.player_2_type
        )

        # 2. Nasłuchiwanie "globalnych" zdarzeń systemowych (Wyjście z gry)
        event_data = self.interface.get_playing_events(self.board, self.current_player_mark)
        if event_data is not None:
            if event_data == "QUIT":
                self.state = "QUIT"
                return
            elif event_data == "MAIN_MENU":
                self.state = "MAIN_MENU"
                return
            elif event_data == "UNDO":
                if len(self.move_history) > 0:
                    if self.game_mode == "PvE":
                        if len(self.move_history) >= 2:
                            self.move_history.pop()  
                            self.board = self.move_history.pop()  
                    else:
                        self.board = self.move_history.pop()
                        self.current_player_mark *= -1
                return
            elif event_data == "TOGGLE_HINT":
                self.show_possible_moves = not self.show_possible_moves
                return
            elif event_data == "CHANGE_COLOR":
                self.board_color = "MODERN" if self.board_color == "CLASSIC" else "CLASSIC"
                return
            elif isinstance(event_data, int):
                # To był prawidłowy ruch gracza zapisany jako liczba (indeks)
                # Wykonujemy go tylko, jeśli jest teraz tura człowieka
                current_type = self.player_1_type if self.current_player_mark == 1 else self.player_2_type
                if current_type == "HUMAN":
                    self.move_history.append(self.board.clone())
                    self.board.make_move(event_data, self.current_player_mark)
                    self.current_player_mark *= -1
                return # Zakończ klatkę i odśwież

        # 3. Sprawdzamy wygraną po ewentualnym ruchu
        result = self.board.check_winner()
        if result is not None:
            self.winner = result
            self.state = 'END_SCREEN'
            return

        # 4. Sprawdzanie zasady pasowania (tylko, jeśli nikt nie kliknął w HUD)
        if not self.board.get_legal_moves(self.current_player_mark):
            self.current_player_mark *= -1
            return

        # 5. Jeśli to tura bota, uruchamiamy jego mózg
        current_type = self.player_1_type if self.current_player_mark == 1 else self.player_2_type
        if current_type == "BOT":
            self._bot_move()


    # METODA _player_move JEST TERAZ ZBĘDNA - USUŃ JĄ CAŁKOWITĄ
    # def _player_move(self):
    #    ... usuń wszystko wewnątrz ...

    def handle_end_screen(self):
        # Tutaj też dopisujemy przekazywanie nazw graczy do ekranu końcowego
        action = self.interface.show_end_screen(
            self.winner, 
            self.board, 
            self.player_1_type, 
            self.player_2_type
        )

        if action == 'QUIT':
            self.state = 'QUIT'
        elif action == 'RESTART':
            self.state = 'SETUP_MENU'
        elif action == 'MAIN_MENU':
            self.state = 'MAIN_MENU'

    def _bot_move(self):
        # Opóźnienie czasowe TYLKO dla szybkich gier!
        if self.game_mode == "CvC" and self.selected_game in ["TicTacToe", "TicTacToe5"]:
            pygame.time.wait(500)
            pygame.event.pump()

        self.move_history.append(self.board.clone())

        if isinstance(self.board, MNKBitboard) and self.board.width == 3:
            active_bot = BotMinimax_3x3(self.current_player_mark)
        else:
            bot_diff = self.difficulty_level.get(self.current_player_mark, 2)
            sims = self.simulations_config.get(bot_diff, 50)
            active_bot = BotMonteCarlo(self.current_player_mark, sims)

        index = active_bot.find_best_move(self.board)
        
        if index is not None:
            self.board.make_move(index, self.current_player_mark)
            self.current_player_mark *= -1

    def _player_move(self):
        event_data = self.interface.get_playing_events(self.board, self.current_player_mark)
        
        if event_data == "QUIT":
            self.state = "QUIT"
        elif event_data == "UNDO":
            if len(self.move_history) > 0:
                if self.game_mode == "PvE":
                    if len(self.move_history) >= 2:
                        self.move_history.pop()  # Usuwa ruch bota
                        self.board = self.move_history.pop()  # Usuwa ruch człowieka
                else:
                    self.board = self.move_history.pop()
                    self.current_player_mark *= -1
        elif event_data == "TOGGLE_HINT":
            self.show_possible_moves = not self.show_possible_moves
        elif event_data == "CHANGE_COLOR":
            self.board_color = "MODERN" if self.board_color == "CLASSIC" else "CLASSIC"
        elif isinstance(event_data, int):  
            self.move_history.append(self.board.clone())
            self.board.make_move(event_data, self.current_player_mark)
            self.current_player_mark *= -1


if __name__ == "__main__":
    game = Game()
    game.run()