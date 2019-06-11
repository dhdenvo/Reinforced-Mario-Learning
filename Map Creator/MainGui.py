import pygame
from MapGui import MapGui
from IconSelectGui import IconSelectGui

class MainGui:
    def __init__(self, display):
        self.map = MapGui(display, self, 40, 80, 115, 12, 40)
        icons = ["-", "="]
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
        
    def get_map(self):
        return self.map.get_map
    
    def draw(self):
        self.display.blit(pygame.transform.scale(pygame.image.load('./DecorativeImage.jpg'), (337, 211)), (650, 584))        
        x = 0
        while x < 1200:
            self.display.blit(pygame.transform.scale(pygame.image.load('./Blocks/Floor.png'), (32, 32)), (x, 756))
            x += 32
        pygame.draw.rect(self.display, (155,181,204), pygame.Rect(1200, 0, 200, 788), 0)
        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(1200, 0, 10, 788), 0)
        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(36, 76, 1128, 488), 0)        
        self.map.draw()
        self.icon_select.draw()
        
        