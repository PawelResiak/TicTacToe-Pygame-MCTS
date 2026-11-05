import pygame

BG_COLOR = (30, 30, 30)
TEXT_COLOR = (240, 240, 240)
BUTTON_COLOR = (70, 130, 180)
BUTTON_HOVER = (100, 150, 200)
BUTTON_SELECTED = (40, 200, 100)

class Button:
    def __init__(self, x, y, width, height, text, value=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.value = value if value else text
        self.is_selected = False

    def draw(self, surface, font, mouse_pos):
        if self.is_selected:
            color = BUTTON_SELECTED
        elif self.rect.collidepoint(mouse_pos):
            color = BUTTON_HOVER
        else:
            color = BUTTON_COLOR

        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = font.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class GameView:
    def __init__(self):
        self.width = 1000
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Board Game Engine')

        self.font_large = pygame.font.SysFont(None, 64)
        self.font_medium = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 28)

    def show_main_menu(self):
        buttons = [
            Button(350, 200, 300, 60, "Othello", "Othello"),
            Button(350, 280, 300, 60, "Tic Tac Toe (3x3)", "TicTacToe"),
            Button(350, 360, 300, 60, "Tic Tac Toe (5x5)", "TicTacToe5"),
            Button(350, 440, 300, 60, "Gomoku(15x15)", "Gomoku15"),
            Button(350, 520, 300, 60, "Gomoku(19x19)", "Gomoku19"),
            Button(50, 50, 120, 40, "Exit", "QUIT")
        ]

        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BG_COLOR)

            title = self.font_large.render("CHOOSE GAME", True, TEXT_COLOR)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 80))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'QUIT'
                for btn in buttons:
                    if btn.is_clicked(event):
                        return btn.value

            for btn in buttons:
                btn.draw(self.screen, self.font_medium, mouse_pos)

            pygame.display.flip()


    def show_setup_menu(self, selected_game):
        modes = [
            Button(200, 200, 180, 50, "Player vs Player", "PvP"),
            Button(410, 200, 180, 50, "Player vs Bot", "PvE"),
            Button(620, 200, 180, 50, "Bot vs Bot", "CvC")
        ]
        modes[1].is_selected = True
        current_mode = "PvE"

        colors = [
            Button(250, 320, 220, 50, "You Start", "X"),
            Button(530, 320, 220, 50, "Bot Starts", "O")
        ]
        colors[1].is_selected = True
        current_color = "O"

        diffs = [
            Button(200, 440, 180, 50, "Easy", 1),
            Button(410, 440, 180, 50, "Medium", 2),
            Button(620, 440, 180, 50, "Hard", 3)
        ]
        diffs[1].is_selected = True 
        current_diff = 2

        diffs_b1 = [
            Button(200, 320, 180, 50, "Easy", 1),
            Button(410, 320, 180, 50, "Medium", 2),
            Button(620, 320, 180, 50, "Hard", 3)
        ]
        diffs_b1[1].is_selected = True
        current_diff_b1 = 2

        diffs_b2 = [
            Button(200, 440, 180, 50, "Easy", 1),
            Button(410, 440, 180, 50, "Medium", 2),
            Button(620, 440, 180, 50, "Hard", 3)
        ]
        diffs_b2[1].is_selected = True
        current_diff_b2 = 2

        start_btn = Button(400, 560, 200, 60, "Start game", "START")
        exit_btn = Button(50, 50, 120, 40, "Exit", "QUIT")
        back_btn = Button(50, 100, 120, 40, "Return", "BACK")

        while True:
            mouse_pos = pygame.mouse.get_pos()
            self.screen.fill(BG_COLOR)

            title = self.font_large.render(f"SETTINGS: {selected_game}", True, TEXT_COLOR)
            self.screen.blit(title, (self.width//2 - title.get_width()//2, 80))

            self.screen.blit(self.font_medium.render("Game Mode:", True, TEXT_COLOR), (420, 160))
            
            if current_mode == "PvE":
                self.screen.blit(self.font_medium.render("Staring Order:", True, TEXT_COLOR), (405, 280))
                self.screen.blit(self.font_medium.render("Difficulty:", True, TEXT_COLOR), (430, 400))
            elif current_mode == "CvC":
                self.screen.blit(self.font_medium.render("Bot 1 Level", True, TEXT_COLOR), (425, 280))
                self.screen.blit(self.font_medium.render("Bot 2 Level", True, TEXT_COLOR), (425, 400))

            for event in pygame.event.get():
                if event.type == pygame.QUIT or exit_btn.is_clicked(event):
                    return "QUIT"
                
                if back_btn.is_clicked(event):
                    return "BACK"
                    
                if start_btn.is_clicked(event):
                    bot_c = "O" if current_color == "X" else "X"
                
                    if current_mode == "CvC":
                        diff_pack = {1: current_diff_b1, -1: current_diff_b2}
                    elif current_mode == "PvE":
                        diff_pack = current_diff
                    else:
                        diff_pack = None

                    return (current_mode, bot_c, diff_pack, None)

                for btn in modes:
                    if btn.is_clicked(event):
                        for b in modes: b.is_selected = False
                        btn.is_selected = True
                        current_mode = btn.value
                
                if current_mode == "PvE":
                    for btn in colors:
                        if btn.is_clicked(event):
                            for b in colors: b.is_selected = False
                            btn.is_selected = True
                            current_color = btn.value
                    for btn in diffs:
                        if btn.is_clicked(event):
                            for b in diffs: b.is_selected = False
                            btn.is_selected = True
                            current_diff = btn.value
                    
                if current_mode in ["CvC"]:
                    for btn in diffs_b1:
                        if btn.is_clicked(event):
                            for b in diffs_b1: b.is_selected = False
                            btn.is_selected = True
                            current_diff_b1 = btn.value
                    for btn in diffs_b2:
                        if btn.is_clicked(event):
                            for b in diffs_b2: b.is_selected = False
                            btn.is_selected = True
                            current_diff_b2 = btn.value

            back_btn.draw(self.screen, self.font_medium, mouse_pos)
            start_btn.draw(self.screen, self.font_medium, mouse_pos)
            exit_btn.draw(self.screen, self.font_medium, mouse_pos)
            
            for btn in modes: btn.draw(self.screen, self.font_small, mouse_pos)
            
            if current_mode == "PvE":
                for btn in colors: btn.draw(self.screen, self.font_small, mouse_pos)
                for btn in diffs: btn.draw(self.screen, self.font_small, mouse_pos)
            if current_mode in ["CvC"]:
                for btn in diffs_b1: btn.draw(self.screen, self.font_small, mouse_pos)
                for btn in diffs_b2: btn.draw(self.screen, self.font_small, mouse_pos)

            pygame.display.flip()


    def _draw_board_grid(self, board, board_color_theme):
        themes = {
            "CLASSIC": ((34, 139, 34), (0, 0, 0)),
            "MODERN": ((200, 200, 200), (50, 50, 50))
        }
        bg_col, line_col = themes.get(board_color_theme, themes["CLASSIC"])

        board_rect = pygame.Rect(0, 0, 700, 700)
        pygame.draw.rect(self.screen, bg_col, board_rect)

        cols = getattr(board, 'width', 8)  
        rows = getattr(board, 'height', 8) 
        
        self.cell_w = 700 // cols
        self.cell_h = 700 // rows

        for x in range(cols):
            for y in range(rows):
                rect = pygame.Rect(x * self.cell_w, y * self.cell_h, self.cell_w, self.cell_h)
                pygame.draw.rect(self.screen, line_col, rect, 2)

    def _draw_pieces(self, board):
        cols = getattr(board, 'width', 8)
        grid = board.grid 

        for index, mark in enumerate(grid):
            if mark == ' ':
                continue
                
            x = (index % cols) * self.cell_w
            y = (index // cols) * self.cell_h
            center = (x + self.cell_w // 2, y + self.cell_h // 2)

            if mark == 'B':
                pygame.draw.circle(self.screen, (0, 0, 0), center, self.cell_w // 2 - 5)
            elif mark == 'W':
                pygame.draw.circle(self.screen, (255, 255, 255), center, self.cell_w // 2 - 5)
            elif mark == 'X':
                offset = 15
                pygame.draw.line(self.screen, (200, 50, 50), (x + offset, y + offset), (x + self.cell_w - offset, y + self.cell_h - offset), 5)
                pygame.draw.line(self.screen, (200, 50, 50), (x + offset, y + self.cell_h - offset), (x + self.cell_w - offset, y + offset), 5)
            elif mark == 'O':
                pygame.draw.circle(self.screen, (50, 50, 200), center, self.cell_w // 2 - 10, 5)

    def _draw_hud(self, score, current_player_mark, board, p1_type, p2_type):
        hud_rect = pygame.Rect(700, 0, 300, 700)
        pygame.draw.rect(self.screen, (40, 40, 40), hud_rect) 
        pygame.draw.line(self.screen, (100, 100, 100), (700, 0), (700, 700), 3)

        # Dynamiczne rozpoznawanie nazw symboli na podstawie typu planszy
        is_othello = hasattr(board, 'white_pieces')
        m1 = "Black" if is_othello else "X"
        m2 = "White" if is_othello else "O"

        # np. p1_type.capitalize() zmieni "HUMAN" na "Human", "BOT" na "Bot"
        p1_name = f"{p1_type.capitalize()} ({m1})"
        p2_name = f"{p2_type.capitalize()} ({m2})"

        active_name = p1_name if current_player_mark == 1 else p2_name
        turn_text = f"Turn: {active_name}"
        
        turn_surf = self.font_small.render(turn_text, True, (255, 215, 0))
        self.screen.blit(turn_surf, (720, 50))

        if score:
            score_text = f"{m1}: {score[0]} | {m2}: {score[1]}"
            score_surf = self.font_small.render(score_text, True, TEXT_COLOR)
            self.screen.blit(score_surf, (720, 100))

    def refresh_screen(self, board, board_color, show_possible_moves, current_player_mark, can_undo, score, p1_type, p2_type):
        self.screen.fill(BG_COLOR)
        
        self._draw_board_grid(board, board_color)
        
        # Sprawdzamy czy to Othello (tylko Othello ma białe pionki w logice)
        is_othello = hasattr(board, 'white_pieces')
        
        # Rysuj zielone kropki tylko, gdy włączone i gra to Othello
        if show_possible_moves and is_othello:
            legal = board.get_legal_moves(current_player_mark)
            cols = getattr(board, 'width', 8)
            for move in legal:
                cx = (move % cols) * self.cell_w + self.cell_w // 2
                cy = (move // cols) * self.cell_h + self.cell_h // 2
                pygame.draw.circle(self.screen, (0, 255, 0), (cx, cy), 8)

        self._draw_pieces(board)
        self._draw_hud(score, current_player_mark, board, p1_type, p2_type)

        # Buttons during the game
        self.hud_buttons = {
            "UNDO": Button(750, 400, 200, 50, "Undo"),
            "CHANGE_COLOR": Button(750, 470, 200, 50, "Color Theme"),
            "MAIN_MENU": Button(750, 540, 200, 50, "Menu")
        }

        # Buttons during othello game
        if is_othello:
            self.hud_buttons["TOGGLE_HINT"] = Button(750, 470, 200, 50, "Hints On/Off")
            self.hud_buttons["CHANGE_COLOR"].rect.y = 540
            self.hud_buttons["MAIN_MENU"].rect.y = 610

        if not can_undo:
            self.hud_buttons["UNDO"].is_selected = False

        mouse_pos = pygame.mouse.get_pos()
        for btn in self.hud_buttons.values():
            btn.draw(self.screen, self.font_small, mouse_pos)

        pygame.display.flip()

    def get_playing_events(self, board, current_player_mark):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
                
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for key, btn in self.hud_buttons.items():
                    if btn.rect.collidepoint(event.pos):
                        return key
                        
                x, y = event.pos
                if x < 700:
                    cols = getattr(board, 'width', 8)
                    col = x // self.cell_w
                    row = y // self.cell_h
                    index = row * cols + col
                    
                    if index in board.get_legal_moves(current_player_mark):
                        return index
        return None

    def show_end_screen(self, winner, board=None, p1_type="Human", p2_type="Bot"):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Dynamiczne przypisanie liter do zwycięzcy
        if board:
            is_othello = hasattr(board, 'white_pieces')
            m1 = "Black" if is_othello else "X"
            m2 = "White" if is_othello else "O"
        else:
            m1, m2 = "X", "O"

        p1_name = f"{p1_type.capitalize()} ({m1})"
        p2_name = f"{p2_type.capitalize()} ({m2})"

        if winner == 1: text = f"{p1_name} Won!"
        elif winner == -1: text = f"{p2_name} Won!"
        else: text = "DRAW!"
        
        title = self.font_large.render(text, True, (255, 215, 0))
        self.screen.blit(title, (self.width//2 - title.get_width()//2, 200))

        restart_btn = Button(300, 400, 180, 60, "Play Again", "RESTART")
        menu_btn = Button(520, 400, 180, 60, "Menu", "MAIN_MENU")

        while True:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: return "QUIT"
                if restart_btn.is_clicked(event): return "RESTART"
                if menu_btn.is_clicked(event): return "MAIN_MENU"

            restart_btn.draw(self.screen, self.font_medium, mouse_pos)
            menu_btn.draw(self.screen, self.font_medium, mouse_pos)
            pygame.display.flip()