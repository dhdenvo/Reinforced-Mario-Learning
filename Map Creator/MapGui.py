import pygame
from InteractiveGui import InteractiveGui
from Icon import Icon
from MultiIcon import MultiIcon

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
                                   "-": pygame.transform.scale(pygame.image.load('./Blocks/Sky.png'), (grid_side, grid_side)), \
                                   "B": pygame.transform.scale(pygame.image.load('./Blocks/Brick.png'), (grid_side, grid_side)),\
                                   "G": pygame.transform.scale(pygame.image.load('./Blocks/Goomba.png'), (grid_side, grid_side)),\
                                   "?": pygame.transform.scale(pygame.image.load('./Blocks/Question.png'), (grid_side, grid_side)),\
                                   "FOne": pygame.transform.scale(pygame.image.load('./Blocks/Flag Ball.png'), (grid_side, grid_side)),\
                                   "FTwo": pygame.transform.scale(pygame.image.load('./Blocks/Flag Edge.png'), (grid_side, grid_side)),\
                                   "FThree": pygame.transform.scale(pygame.image.load('./Blocks/Flag Main.png'), (grid_side, grid_side)),\
                                   "T": pygame.transform.scale(pygame.image.load('./Blocks/Flag Terminus.png'), (grid_side, grid_side)),\
                                   "W": pygame.transform.scale(pygame.image.load('./Blocks/Wall.png'), (grid_side, grid_side))}       
        
        
    def __convert_coor(self, coordinates):
        if coordinates[0] - self.scroll in range(self.MAX_LENGTH):
            return (self.x_pos + self.grid_side * (coordinates[0] - self.scroll), self.y_pos + self.grid_side * coordinates[1])
        return (-1, -1)
    
    def __create_blank_map(self):
        self.grid_positions = {}
        for real_grid_loc in self.grid:
            symbol = "-"
            if real_grid_loc[1] in (12, 13):
                symbol = "="
            self.grid_positions[real_grid_loc] = Icon(real_grid_loc[0], real_grid_loc[1], symbol)
            
    def get_map(self):
        return self.grid_positions
    
    def scroll_grid(self, direction):
        if (self.scroll + direction) in range(abs(self.length - self.MAX_LENGTH)):
            self.scroll += direction
    
    def __add_flag(self, x_pos, add = True):
        icon = '-'
        if add: icon = 'FOne'
        self.grid_positions[(x_pos, 1)] = icon
        if add: icon = 'FThree'        
        self.grid_positions[(x_pos, 2)] = icon
        if add: icon = 'FTwo'        
        self.grid_positions[(x_pos - 1, 2)] = icon
        if add: icon = 'T'
        for y_pos in range(3, 11):
            self.grid_positions[(x_pos, y_pos)] = icon   
        if add: icon = 'W'
        self.grid_positions[(x_pos, 11)] = icon
    
    def add_icon(self, real_grid_loc):
        if self.main_gui.get_icon() in ["F"]:
            icon = MultiIcon(real_grid_loc[0], real_grid_loc[1], "FOne", [(0,-1), (0,1)]) 
        else:
            icon = Icon(real_grid_loc[0], real_grid_loc[1], self.main_gui.get_icon())
        if self.grid_positions[real_grid_loc].remove(self.grid_positions): icon.create(self.grid_positions)
        
    
    def select(self, pos):
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)    
            button = InteractiveGui(None, None, grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
            if button.select(pos):
                print(real_grid_loc)
                self.add_icon(real_grid_loc)

        
    def draw(self):  
        for real_grid_loc in self.grid:
            grid_loc = self.__convert_coor(real_grid_loc)
            if grid_loc != (-1, -1):
                try:
                    self.display.blit(self.SYMBOL_TRANSLATION.get(self.grid_positions.get(real_grid_loc).get_icon_string()), grid_loc)
                    rect = pygame.Rect(grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
                    pygame.draw.rect(self.display, (0,0,0), rect, 2)
                except TypeError:
                    print("Grid Loc", real_grid_loc)