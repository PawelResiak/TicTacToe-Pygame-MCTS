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
