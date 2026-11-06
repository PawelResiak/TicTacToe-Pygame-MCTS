import pygame
from ui import Button, BG_COLOR, TEXT_COLOR

class Menus:
    def __init__(self, screen, width, height, font_large, font_medium, font_small):
        self.screen = screen
        self.width = width
        self.height = height
        self.font_large = font_large
        self.font_medium = font_medium
        self.font_small = font_small

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

    def show_end_screen(self, winner, board=None, p1_type="Human", p2_type="Bot"):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

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