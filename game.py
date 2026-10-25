import pygame
import sys

from gui import GameView, Button
from board import MNKBoard
from ai import BotMinimax_3x3, BotMonteCarlo
         



class Game:
    def __init__(self):
        self.interface = GameView()
        self.history = []

        mode = [
            ("player vs player", 1),
            ("player vs bot", 2)
        ]
        self.game_type = self.choice_menu(mode)

        if self.game_type == 2:
            mark_option = [("Play as a (O)", "O"), ("Play as a (X)", "X")]
            self.human_mark = self.choice_menu(mark_option)
            self.bot_mark = "X" if self.human_mark == "O" else "O"

            difficulty_options = [("Easy", 1), ("Medium", 2), ("Hard", 3)]
            self.difficulty_level = self.choice_menu(difficulty_options)

        board_size = [
            ("Classic 3x3 (win_streak: 3)", (3, 3, 3)),
            ("Expanded 5x5 (win_streak: 4)", (5, 5, 4)),
            ("Huge 10x10 (win_streak: 5)", (10, 10, 5)),
            ("Gomoku 19x19 (win_streak: 5)", (19, 19, 5))
        ]
        chosen_board = self.choice_menu(board_size)
        self.width = chosen_board[0]
        self.height = chosen_board[1]
        self.win_streak = chosen_board[2]

        self.interface.set_board_size(self.width, self.height)
        self.board = MNKBoard(self.width, self.height, self.win_streak)
        self.current_player_mark = 'X'
    
    
    
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
        elif self.game_type == 1:
            announcement = f"Player {result} won!"
        elif self.game_type == 2:
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

            self.interface.grid.fill((255, 255, 255))
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
                play_again = self.end_screen(result)
                return play_again

            if self.game_type == 2 and self.current_player_mark == self.bot_mark:
                index = self._bot_move(self.bot_mark)
                
                self.board.make_move(index, self.current_player_mark)
                self.history.append(index)
                self.current_player_mark = "O" if self.current_player_mark == "X" else "X"
                continue

            click = self.interface.get_click()
            if click is not None:
                row, column = click
                index = row * self.width + column

                if self.board.grid[index] == ' ':
                    self.board.make_move(index, self.current_player_mark)
                    self.history.append(index)
                    self.current_player_mark = "O" if self.current_player_mark == "X" else "X"
                else:
                    print("This field is already occupied. Please choose another field.")

    
    
    def _bot_move(self, bot_mark):
        
        if self.game_type == 2:
            difficulty_level = self.difficulty_level
        else:
            difficulty_level = self.difficulty_level_x if bot_mark == 'X' else self.difficulty_level_o
            
        possible_moves = len(self.board.get_legal_moves())
        time_configuration = {1: (0.2, 0.03), 2: (0.5, 0.05), 3: (2.0, 0.15)}
        base, multiplier = time_configuration[difficulty_level]
        time_for_move = base + (multiplier * possible_moves)

        active_bot = BotMonteCarlo(bot_mark, time_for_move)

        return active_bot.find_best_move(self.board)

