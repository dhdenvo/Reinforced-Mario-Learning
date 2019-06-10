import pygame

class MapGui:
    def __init__(self, display, x_pos = 0, y_pos = 0, width = 40, length = 40, grid_side = 10):
        self.display = display
        self.length = length
        self.height = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.grid_side = grid_side
        
        self.grid = []
        for x in range(self.length):
            for y in range(self.height):
                self.grid.append((self.x_pos + self.grid_side * x, self.y_pos + self.grid_side * y))
        
    def select(self, pos):
        for grid_loc in self.grid:
            if pos[0] in range(grid_loc[0], grid_loc[0] + self.grid_side) and \
               pos[1] in range(grid_loc[1], grid_loc[1] + self.grid_side):
                print(grid_loc)
            
        
    def draw(self):
        #rect = pygame.Rect(self.x_pos, self.y_pos, self.grid_side, self.grid_side)
        #pygame.draw.rect(self.display, (0,0,0), rect, 4)        
        for grid_loc in self.grid:
            rect = pygame.Rect(grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
            pygame.draw.rect(self.display, (0,0,0), rect, 2)