import pygame

class IconSelectGui:
    def __init__(self, display, gui, icons, x_pos, y_pos, grid_side):
        self.display = display
        self.main_gui = gui
        self.grid_side = grid_side
        self.x_pos = x_pos
        self.y_pos = y_pos
        
        self.icons = icons
        self.length = 1
        self.height = len(self.icons)
        
        self.grid = []
        for x in range(self.length):
            for y in range(self.height):
                self.grid.append((x, y))  
        
        
    def __convert_coor(self, coordinates):
        return (self.x_pos + (2 * self.grid_side * coordinates[0]), self.y_pos + (2 * self.grid_side * coordinates[1]))
    
    def select(self, pos):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)            
            if grid_loc != (-1, -1) and pos[0] in range(grid_loc[0], grid_loc[0] + self.grid_side) and \
                   pos[1] in range(grid_loc[1], grid_loc[1] + self.grid_side):
                print(real_grid_loc)
                #self.main_gui.set_icon(self.icons[real_grid_loc[1] * (real_grid_loc[0] + 1)])
    
    def draw(self):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)
            if grid_loc != (-1, -1):
                self.display.blit(self.icons[real_grid_loc[1] * (real_grid_loc[0] + 1)], grid_loc)
                rect = pygame.Rect(grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
                pygame.draw.rect(self.display, (0,0,0), rect, 2)        