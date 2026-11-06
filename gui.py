import pygame
from ui import Button, BG_COLOR, TEXT_COLOR
from menus import Menus

class GameView:
    def __init__(self):
        self.width = 1000
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Board Game Engine')

        self.font_large = pygame.font.SysFont(None, 64)
        self.font_medium = pygame.font.SysFont(None, 40)
        self.font_small = pygame.font.SysFont(None, 28)

        self.menus = Menus(self.screen, self.width, self.height, self.font_large, self.font_medium, self.font_small)

        self.black_piece = None
        self.white_piece = None
        self._current_radius = 0

    def show_main_menu(self):
        return self.menus.show_main_menu()

    def show_setup_menu(self, selected_game):
        return self.menus.show_setup_menu(selected_game)

    def show_end_screen(self, winner, board=None, p1_type="Human", p2_type="Bot"):
        return self.menus.show_end_screen(winner, board, p1_type, p2_type)

    def _create_piece_surface(self, radius, base_color, highlight_color):
        size = radius * 2 + 8
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        
        center_x = size // 2 - 2
        center_y = size // 2 - 2

        pygame.draw.circle(surface, (0, 0, 0, 90), (center_x + 3, center_y + 4), radius)

        for i in range(radius):
            factor = i / radius 
            r = base_color[0] + (highlight_color[0] - base_color[0]) * factor
            g = base_color[1] + (highlight_color[1] - base_color[1]) * factor
            b = base_color[2] + (highlight_color[2] - base_color[2]) * factor
            
            offset = int(factor * (radius * 0.45))
            pygame.draw.circle(surface, (int(r), int(g), int(b)), 
                            (center_x - offset, center_y - offset), radius - i)
                            
        return surface

    def _draw_board_grid(self, board, board_color_theme):
        themes = {
            "CLASSIC": ((34, 139, 34), (0, 0, 0)),
            "MODERN": ((74, 18, 26), (10, 0, 10))
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
        
        radius = self.cell_w // 2 - 5

        if self._current_radius != radius:
            self._current_radius = radius
            self.black_piece = self._create_piece_surface(
                radius, 
                base_color=(71, 74, 81), 
                highlight_color=(150, 153, 160)
            )
            self.white_piece = self._create_piece_surface(
                radius, 
                base_color=(74, 4, 21), 
                highlight_color=(170, 50, 70)
            )

        for index, mark in enumerate(grid):
            if mark == ' ':
                continue
                
            x = (index % cols) * self.cell_w
            y = (index // cols) * self.cell_h
            center = (x + self.cell_w // 2, y + self.cell_h // 2)

            if mark == 'B':
                rect = self.black_piece.get_rect(center=center)
                self.screen.blit(self.black_piece, rect)
            elif mark == 'W':
                rect = self.white_piece.get_rect(center=center)
                self.screen.blit(self.white_piece, rect)
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

        is_othello = hasattr(board, 'white_pieces')
        m1 = "Black" if is_othello else "X"
        m2 = "White" if is_othello else "O"

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
        
        is_othello = hasattr(board, 'white_pieces')
        
        if show_possible_moves and is_othello:
            legal = board.get_legal_moves(current_player_mark)
            cols = getattr(board, 'width', 8)
            for move in legal:
                cx = (move % cols) * self.cell_w + self.cell_w // 2
                cy = (move // cols) * self.cell_h + self.cell_h // 2
                pygame.draw.circle(self.screen, (100, 100, 100), (cx, cy), 8)

        self._draw_pieces(board)
        self._draw_hud(score, current_player_mark, board, p1_type, p2_type)

        self.hud_buttons = {
            "UNDO": Button(750, 400, 200, 50, "Undo"),
            "CHANGE_COLOR": Button(750, 470, 200, 50, "Color Theme"),
            "MAIN_MENU": Button(750, 540, 200, 50, "Menu")
        }

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