import pygame
from InteractiveGui import InteractiveGui
import MainGui

#A class that creates a visible icon selection menu
class IconSelectGui(InteractiveGui):
    def __init__(self, display, gui, x_pos, y_pos, grid_side, icons):
        super().__init__(display, gui, x_pos, y_pos)
        self.grid_side = grid_side
        
        self.icons = icons
        self.length = 2
        self.height = 9
        
        #Create a list of coordinates for each icon        
        self.grid = []
        for x in range(self.length):
            for y in range(self.height):
                self.grid.append((x, y))  

    #Convert the map coordinates to coordinates on the gui
    def __convert_coor(self, coordinates):
        return (int(self.x_pos + ((1.6 * self.grid_side) * coordinates[0])), int(self.y_pos + ((1.6 * self.grid_side) * coordinates[1])))
    
    #Sets the current icon based on where the user is clicking (selecting)
    def select(self, pos):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)
            #Create a temp basic gui to make the selecting easier (using the gui's select function)            
            button = InteractiveGui(None, None, grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
            if button.select(pos):
                print(real_grid_loc)
                self.main_gui.set_icon(self.icons[real_grid_loc[1] + self.height * real_grid_loc[0]])
    
    #Draw the icon select menu and the icons in it
    def draw(self):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)
            if grid_loc != (-1, -1):
                #Draw the image for the icon                
                self.display.blit(pygame.transform.scale(MainGui.SYMBOL_TRANSLATION.get(self.icons[real_grid_loc[1] + self.height * real_grid_loc[0]]), (self.grid_side, self.grid_side)), grid_loc)
                #Draw the outline of the icon
                rect = pygame.Rect(grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
                pygame.draw.rect(self.display, (0,0,0), rect, 2)        