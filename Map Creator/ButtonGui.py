import pygame
from InteractiveGui import InteractiveGui

class ButtonGui(InteractiveGui):
    def __init__(self, display, gui, x_pos, y_pos, length, height, text, push_function, background_colour = (0,0,0), font_size = 20, colour = (0,0,0)):
        super().__init__(display, gui, x_pos, y_pos, length, height, background_colour, colour)
        self.text = text
        self.font_size = font_size
        self.push_function = push_function
        
    def select(self, pos):
        if super().select(pos):
            self.push_function()
            
    def draw(self):
        super().draw()
        font = pygame.font.Font('Fonts/SuperMario256.ttf', self.font_size)
        surface = font.render(self.text, False, self.colour)
        self.display.blit(surface, (self.x_pos + 6, self.y_pos + 6))        