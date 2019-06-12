import pygame
from MapGui import MapGui
from IconSelectGui import IconSelectGui
from ButtonGui import ButtonGui

class MainGui:
    def __init__(self, display):
        from MapCreatorMain import create_level  
        from MapCreatorMain import move_left
        from MapCreatorMain import move_right
        
        icons = ["=", "-", "B", "G", "?", "-", "-", "=", "-", "-", "-", "-", "-", "-", "-", "-", "=", "-"]
        self.selected_icon = "-"   
        self.display = display
        
        self.map_height = 14
        self.map_length = 115
        
        self.guis = {}
        self.guis["map"] = MapGui(display, self, 40, 80, self.map_length, self.map_height, 35)
        self.guis["icon_select"] = IconSelectGui(display, self, 1240, 80, 50, icons)
        self.guis["create_button"] = ButtonGui(display, self, 40, 680, 215, 50, "Create", create_level, (155,181,204), 50)  
        self.guis["left_button"] = ButtonGui(display, self, 40, 590, 64, 64, "<", move_left, (155,181,204), 64)
        self.guis["right_button"] = ButtonGui(display, self, 1100, 590, 64, 64, ">", move_right, (155,181,204), 64)        
        
    def select(self, pos):
        for gui in self.guis.values():
            gui.select(pos)
        
    def get_icon(self):
        return self.selected_icon
    
    def set_icon(self, icon):
        self.selected_icon = icon
        
    def get_map(self):
        return self.guis["map"].get_map()
    
    def get_map_measurements(self):
        return (self.map_length, self.map_height)
    
    def scroll(self, direction):
        self.guis["map"].scroll_grid(direction)
    
    def __create_text(self, text, x, y, size):
        font = pygame.font.Font('Fonts/SuperMario256.ttf', size)
        surface = font.render(text, False, (0, 0, 0))
        self.display.blit(surface, (x, y))
    
    def draw(self):
        #Decorative Stuff (Mario Image and Floor)
        self.display.blit(pygame.transform.scale(pygame.image.load('./DecorativeImage.jpg'), (337, 211)), (650, 584))        
        x = 0
        while x < 1200:
            self.display.blit(pygame.transform.scale(pygame.image.load('./Blocks/Floor.png'), (32, 32)), (x, 756))
            x += 32
            
        #Basic Rectangles For Visuals and Separation
        pygame.draw.rect(self.display, (155,181,204), pygame.Rect(1200, 0, 200, 788), 0)
        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(1200, 0, 10, 788), 0)
        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(36, 76, 1128, 498), 0)
        
        #Headers
        self.__create_text("Blocks", 1226, 20, 40)
        self.__create_text("Super Mario Bros - Mario Maker NES", 40, 20, 40)    
        
        #Drawing classes
        for gui in self.guis.values():
            gui.draw()
        
        
        