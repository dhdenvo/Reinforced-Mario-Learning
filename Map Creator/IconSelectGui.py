import pygame
from InteractiveGui import InteractiveGui

class IconSelectGui(InteractiveGui):
    def __init__(self, display, gui, x_pos, y_pos, grid_side, icons):
        super().__init__(display, gui, x_pos, y_pos)
        self.grid_side = grid_side
        
        self.icons = icons
        self.length = 2
        self.height = 9
        
        self.grid = []
        for x in range(self.length):
            for y in range(self.height):
                self.grid.append((x, y))  
                
        self.SYMBOL_TRANSLATION = {"=": pygame.transform.scale(pygame.image.load('./Blocks/Floor.png'), (grid_side, grid_side)), \
                                   "-": pygame.transform.scale(pygame.image.load('./Blocks/Sky.png'), (grid_side, grid_side))}           
        
        
    def __convert_coor(self, coordinates):
        return (int(self.x_pos + ((1.6 * self.grid_side) * coordinates[0])), int(self.y_pos + ((1.6 * self.grid_side) * coordinates[1])))
    
    def select(self, pos):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)
            button = InteractiveGui(None, None, grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
            if button.select(pos):
                print(real_grid_loc)
                self.main_gui.set_icon(self.icons[real_grid_loc[1] + self.height * real_grid_loc[0]])
    
    def draw(self):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)
            if grid_loc != (-1, -1):
                self.display.blit(self.SYMBOL_TRANSLATION.get(self.icons[real_grid_loc[1] + self.height * real_grid_loc[0]]), grid_loc)
                rect = pygame.Rect(grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
                pygame.draw.rect(self.display, (0,0,0), rect, 2)        