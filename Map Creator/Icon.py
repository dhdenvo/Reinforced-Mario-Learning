import pygame
import MainGui

grid_side = 35

#A class that has stores information about icons on the map
class Icon:
    def __init__(self, x_pos, y_pos, icon_string, image_icon = None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.icon_string = icon_string
        self.image_icon = image_icon   
        
    #Give the coordinates of the icon
    def get_grid_loc(self):
        return (self.x_pos, self.y_pos)
    
    #Give the icon's string value
    def get_icon_string(self):
        return self.icon_string
    
    #Return a list of coordinates (one one coordinate since its not a multi icon)
    def get_coordinates(self):
        return [[self.x_pos, self.y_pos]]
    
    #Add the icon to the map grid
    def create(self, grid_positions):
        grid_positions[self.get_grid_loc()] = self
        
    #Remove the icon from the grid (required for multi icon but not for single icon)
    def remove(self, grid_positions = None):
        #For a multi icon, each coupled icon has to be removed
        #For a single icon, the act of adding a new icon automatically removes the icon (which is why it only returns true)
        return True
    
    #Get the image of the icon
    def get_icon_image(self):
        if not self.image_icon:
            return pygame.transform.scale(MainGui.SYMBOL_TRANSLATION.get(self.icon_string, MainGui.SYMBOL_TRANSLATION.get("-")), (grid_side, grid_side))
        return self.image_icon
 
 
