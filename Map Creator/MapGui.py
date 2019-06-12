import pygame
from InteractiveGui import InteractiveGui

class MapGui(InteractiveGui):
    def __init__(self, display, gui, x_pos, y_pos, length, height, grid_side, max_length = 32):  
        super().__init__(display, gui, x_pos, y_pos)
        self.length = length
        self.height = height
        self.grid_side = grid_side
        self.scroll = 0
        self.MAX_LENGTH = max_length
        
        self.grid = []
        for x in range(self.length):
            for y in range(self.height):
                self.grid.append((x, y))
                
        self.__create_blank_map()
        self.SYMBOL_TRANSLATION = {"=": pygame.transform.scale(pygame.image.load('./Blocks/Floor.png'), (grid_side, grid_side)), \
                           "-": pygame.transform.scale(pygame.image.load('./Blocks/Sky.png'), (grid_side, grid_side))}        
        
        
    def __convert_coor(self, coordinates):
        if coordinates[0] - self.scroll in range(self.MAX_LENGTH):
            if coordinates == (0,0):
                print("HELP")
            return (self.x_pos + self.grid_side * (coordinates[0] - self.scroll), self.y_pos + self.grid_side * coordinates[1])
        return (-1, -1)
    
    def __create_blank_map(self):
        self.grid_positions = {}
        for real_grid_loc in self.grid:
            symbol = "-"
            if real_grid_loc[1] in (12, 13):
                symbol = "="
            self.grid_positions[real_grid_loc] = symbol
            
    def get_map(self):
        return self.grid_positions
    
    def scroll_grid(self, direction):
        if (self.scroll + direction) in range(abs(self.length - self.MAX_LENGTH)):
            self.scroll += direction
    
    def select(self, pos):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)    
            button = InteractiveGui(None, None, grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
            if button.select(pos):
                print(real_grid_loc)
                self.grid_positions[real_grid_loc] = self.main_gui.get_icon()
            
        
    def draw(self):  
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)
            if grid_loc != (-1, -1):
                self.display.blit(self.SYMBOL_TRANSLATION.get(self.grid_positions.get(real_grid_loc, "-")), grid_loc)
                rect = pygame.Rect(grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
                pygame.draw.rect(self.display, (0,0,0), rect, 2)