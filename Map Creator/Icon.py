import pygame
import MainGui

grid_side = 35

class Icon:
    def __init__(self, x_pos, y_pos, icon_string, image_icon = None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.icon_string = icon_string
        self.image_icon = image_icon   
        
    def get_grid_loc(self):
        return (self.x_pos, self.y_pos)
    
    def get_icon_string(self):
        return self.icon_string
    
    def get_coordinates(self):
        return [[self.x_pos, self.y_pos]]
    
    def create(self, grid_positions):
        grid_positions[self.get_grid_loc()] = self
        
    def remove(self, grid_positions = None):
        return True
    
    def get_icon_image(self):
        if not self.image_icon:
            return pygame.transform.scale(MainGui.SYMBOL_TRANSLATION.get(self.icon_string, MainGui.SYMBOL_TRANSLATION.get("-")), (grid_side, grid_side))
        return self.image_icon
 
 
