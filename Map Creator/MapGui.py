import pygame

MAX_LENGTH = 28

class MapGui:
    def __init__(self, display, x_pos = 0, y_pos = 0, length = 40, height = 40, grid_side = 10):
        self.display = display
        self.length = length
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.grid_side = grid_side
        self.scroll = 0
        
        self.symbol_translation = {"=": pygame.transform.scale(pygame.image.load('./Blocks/Floor.png'), (grid_side, grid_side)), \
                                   "-": pygame.transform.scale(pygame.image.load('./Blocks/Sky.png'), (grid_side, grid_side))}
        
        self.grid = []
        for x in range(self.length):
            for y in range(self.height):
                self.grid.append((x, y))
                
        self.__create_blank_map()
        
        
    def __convert_coor(self, coordinates):
        if coordinates[0] < MAX_LENGTH:
            return (self.x_pos + self.grid_side * (coordinates[0] - self.scroll), self.y_pos + self.grid_side * coordinates[1])
        return (-1, -1)
    
    def select(self, pos):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)            
            if grid_loc != (-1, -1) and pos[0] in range(grid_loc[0], grid_loc[0] + self.grid_side) and \
               pos[1] in range(grid_loc[1], grid_loc[1] + self.grid_side):
                print(real_grid_loc)
              
      
    def __create_blank_map(self):
        self.grid_positions = {}
        for real_grid_loc in self.grid:
            symbol = "-"
            if real_grid_loc[1] in (10, 11):
                symbol = "="
            self.grid_positions[real_grid_loc] = symbol
            
        
    def draw(self):  
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)
            if grid_loc != (-1, -1):
                self.display.blit(self.symbol_translation.get(self.grid_positions.get(real_grid_loc, "-")), grid_loc)
                rect = pygame.Rect(grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
                pygame.draw.rect(self.display, (0,0,0), rect, 2)