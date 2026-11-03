import pygame
import sys

from gui import GameView, Button
from board import MNKBoard, OthelloBoard
from ai import BotMinimax_3x3, BotMonteCarlo
         



class Game:
    def __init__(self):
        self.interface = GameView()
        self.history = []

        mode = [
            ("player vs player", 1),
            ("player vs bot", 2),
            ("bot vs bot", 3)
        ]

        games = [
            ("Tic Tac Toe / Gomoku", 1), 
            ("Othello", 2)
        ]

        difficulty_options = [
            ("Easy", 1), 
            ("Medium", 2), 
            ("Hard", 3)
        ]

        board_size = [
            ("Classic 3x3 (win_streak: 3)", (3, 3, 3)),
            ("Expanded 5x5 (win_streak: 4)", (5, 5, 4)),
            ("Huge 10x10 (win_streak: 5)", (10, 10, 5)),
            ("Gomoku 19x19 (win_streak: 5)", (19, 19, 5))
        ]

        self.game_choice = self.choice_menu(games)
        self.game_mode = self.choice_menu(mode)

        if self.game_choice == 1:
            if self.game_mode == 2:
                mark_option = [("Play as a (O)", "O"), ("Play as a (X)", "X")]
                self.human_mark = self.choice_menu(mark_option)
                self.bot_mark = "X" if self.human_mark == "O" else "O"
                self.difficulty_level = self.choice_menu(difficulty_options)
            elif self.game_mode == 3:
                self.difficulty_level_1 = self.choice_menu([("Easy", 1), ("Medium", 2), ("Hard", 3)])
                self.difficulty_level_2 = self.choice_menu([("Easy", 1), ("Medium", 2), ("Hard", 3)])

            chosen_board = self.choice_menu(board_size)
            self.width = chosen_board[0]
            self.height = chosen_board[1]
            self.win_streak = chosen_board[2]
            
            self.interface.set_board_size(self.width, self.height)
            self.board = MNKBoard(self.width, self.height, self.win_streak)
            self.current_player_mark = 'X'
        else:
            if self.game_mode == 2:
                mark_option = [("Play as a white", "W"), ("Play as a black", "B")]
                self.human_mark = self.choice_menu(mark_option)
                self.bot_mark = "W" if self.human_mark == "B" else "B"
                self.difficulty_level = self.choice_menu(difficulty_options)
            elif self.game_mode == 3:
                self.difficulty_level_1 = self.choice_menu([("Easy", 1), ("Medium", 2), ("Hard", 3)])
                self.difficulty_level_2 = self.choice_menu([("Easy", 1), ("Medium", 2), ("Hard", 3)])

            self.interface.set_board_size(8, 8)
            self.width = 8
            self.height = 8
            self.win_streak = 0
            self.board = OthelloBoard()
            self.current_player_mark = 'B'
            
    
    
    
    def choice_menu(self, opcje):
        buttons = []
        start_y = 100

        for tekst, value in opcje:
            new_button = Button(200, start_y, 400, 60, tekst, (100, 100, 200))
            buttons.append((new_button, value))
            start_y += 80
            
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button, value in buttons:
                        if button.is_clicked(event.pos):
                            return value

            self.interface.grid.fill((255, 255, 255))
            for button, _ in buttons:
                button.draw(self.interface.grid)
            pygame.display.flip()
            self.interface.clock.tick(60)
    
    
    
    def end_screen(self, result):
        if result == 'draw':
            announcement = "draw!"
        elif self.game_mode == 1:
            announcement = f"Player {result} won!"
        elif self.game_mode == 2:
            if result == self.human_mark:
                announcement = "You win!"
            else:
                announcement = "You lose!"
        else:
            announcement = f"Bot {result} won!"

        middle_x = self.interface.grid_size[0] // 2
        middle_y = self.interface.grid_size[1] // 2

        font = pygame.font.Font(None, 72)
        subtitle = font.render(announcement, True, (0, 0, 0), (255, 255, 255))
        subtitle_rect = subtitle.get_rect(center=(middle_x, middle_y - 50))

        button_restart = Button(middle_x - 150, middle_y + 20, 300, 60, "Play again", (100, 200, 100))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_restart.is_clicked(event.pos):
                        return True

            self.interface.grid.fill((120, 30, 0))
            self.interface.draw_board()
            self.interface.draw_symbols(self.board)
            
            self.interface.grid.blit(subtitle, subtitle_rect)
            button_restart.draw(self.interface.grid)
            
            pygame.display.flip()
            self.interface.clock.tick(15)


    
    def start(self):
        running = True
        while running:
            self.interface.refresh_screen(self.board)

            result = self.board.check_winner()

            if result is not None:
                return self.end_screen(result)

            if self.game_mode == 2 and self.current_player_mark == self.bot_mark:
                index = self._bot_move(self.bot_mark)
                
                self.board.make_move(index, self.current_player_mark)
                self.history.append(index)
                if self.game_choice == 1:
                    self.current_player_mark = "O" if self.current_player_mark == "X" else "X"
                else:
                    self.current_player_mark = "W" if self.current_player_mark == "B" else "B"
                continue

            click = self.interface.get_click()
            if click is not None:
                row, column = click
                index = row * self.width + column

                if index in self.board.get_legal_moves(self.current_player_mark):
                    self.board.make_move(index, self.current_player_mark)
                    self.history.append(index)
                    if self.game_choice == 1:
                        self.current_player_mark = "O" if self.current_player_mark == "X" else "X"
                    else:
                        self.current_player_mark = "W" if self.current_player_mark == "B" else "B"
                else:
                    print("Illegal move. Try again.")

    
    
    def _bot_move(self, bot_mark):
        
        if self.game_mode == 2:
            difficulty_level = self.difficulty_level
        else:
            if bot_mark in ['X', 'B']:
                difficulty_level = self.difficulty_level_1
            else:
                difficulty_level = self.difficulty_level_2
            
        possible_moves = len(self.board.get_legal_moves(bot_mark))
        simulations_configuration = {1: 20, 2: 70, 3: 150}

        active_bot = BotMonteCarlo(bot_mark, simulations_configuration[difficulty_level])

        return active_bot.find_best_move(self.board)

