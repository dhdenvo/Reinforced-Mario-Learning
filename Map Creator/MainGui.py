import pygame
from MapGui import MapGui
from IconSelectGui import IconSelectGui

class MainGui:
    def __init__(self, display):
        self.map = MapGui(display, 40, 80, 115, 12, 40)
        icons = [pygame.transform.scale(pygame.image.load('./Blocks/Sky.png'), (40, 40)), pygame.transform.scale(pygame.image.load('./Blocks/Floor.png'), (40, 40))]
        self.icon_select = IconSelectGui(display, self, icons, 1250, 40, 40)
        self.display = display
        self.selected_icon = pygame.transform.scale(pygame.image.load('./Blocks/Sky.png'), (40, 40))
        
    def select(self, pos):
        self.map.select(pos)
        self.icon_select.select(pos)
        
    def get_icon(self):
        return self.selected_icon
    
    def set_icon(self, icon):
        self.selected_icon = icon
    
    def draw(self):
        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(1200, 0, 10, 788), 0)        
        self.map.draw()
        self.icon_select.draw()
        
        