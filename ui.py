import pygame

BG_COLOR = (30, 30, 32)
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