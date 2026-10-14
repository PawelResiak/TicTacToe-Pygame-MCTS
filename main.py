import random
import time
import pygame
import sys



class GameView:
    def __init__(self):
        pygame.init()

        self.grid = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()


    def set_board_size(self, width, height):
        self.width = width
        self.height = height
        self.grid_size = (width * 100, height * 100)
        self.grid = pygame.display.set_mode(self.grid_size)

    def get_click(self) -> tuple:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                column = x // 100
                row = y // 100
                return (row, column)
        return None

    def refresh_screen(self, board):
        self.grid.fill((255, 255, 255))
        self.draw_board()
        self.draw_symbols(board)
        pygame.display.flip()
        self.clock.tick(60)


    def draw_board(self):
        for i in range(1, self.width):
            x = i * 100
            pygame.draw.line(self.grid, (0, 0, 0), (x, 0), (x, self.grid_size[1]), 3)

        for i in range(1, self.height):
            y = i * 100
            pygame.draw.line(self.grid, (0, 0, 0), (0, y), (self.grid_size[0], y), 3)

    def draw_o(self, row, column):
        middle_x = column * 100 + 50
        middle_y = row * 100 + 50
        pygame.draw.circle(self.grid, (0, 0, 255), (middle_x, middle_y), 35, 5)

    def draw_x(self, row, column):
        middle_x = column * 100 + 50
        middle_y = row * 100 + 50
        pygame.draw.line(self.grid, (255, 0, 0), (middle_x - 35, middle_y - 35), (middle_x + 35, middle_y + 35), 5)
        pygame.draw.line(self.grid, (255, 0, 0), (middle_x + 35, middle_y - 35), (middle_x - 35, middle_y + 35), 5)

    def draw_symbols(self, board):
        for y in range(self.height):
            for x in range(self.width):
                mark = board.grid[y * self.width + x]
                if mark == 'O':
                    self.draw_o(y, x)
                elif mark == 'X':
                    self.draw_x(y, x)





class Button:

    def __init__(self, x: int, y: int, width: int, height: int, text: str, color: tuple):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)

    def is_clicked(self, mouse_pos: tuple) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def draw(self, window: pygame.Surface) -> None:
        pygame.draw.rect(window, self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)



class Board:
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
        new_board = Board(self.width, self.height, self.win_streak)
        new_board.grid = self.grid.copy()
        return new_board
         


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

        movey = board_object.get_legal_moves()
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

        for move in board_object.get_legal_moves():
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
        self.opponent_mark = 'X' if bot_mark == 'O' else 'O'



    def _simulate_game(self, board_copy, current_player_mark):
        while True:
            random_move = random.choice(board_copy.get_legal_moves())
            board_copy.make_move(random_move, current_player_mark)
            result = board_copy.check_winner()
            if result == 'draw':
                return 0
            elif result == self.bot:
                return 1
            elif result is not None and result != self.bot:
                return -1
            current_player_mark = 'X' if current_player_mark == 'O' else 'O'



    def find_best_move(self, board_object):
        best_move = None
        best_result = -999999
        get_legal_moves = board_object.get_legal_moves()
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
        self.board = Board(self.width, self.height, self.win_streak)
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



if __name__ == '__main__':
    game_on = True
    while game_on:
        new_game = Game()
        game_on = new_game.start()
