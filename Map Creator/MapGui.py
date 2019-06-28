import pygame
from InteractiveGui import InteractiveGui
from Icon import Icon
from MultiIcon import MultiIcon
import sys

class MapGui(InteractiveGui):
    def __init__(self, display, gui, x_pos, y_pos, length, height, grid_side, max_length = 32):  
        super().__init__(display, gui, x_pos, y_pos)
        self.length = length
        self.height = height
        self.grid_side = grid_side
        self.scroll = 0
        self.MAX_LENGTH = max_length
        self.images = {}
        self.flag = None
        self.MULTIICONS = {"F": [[[0, 1, "F", "Flag Ball"], [0, 2, "F", "Flag Main"], [-1, 2, "F", "Flag Edge"], \
                                  [0, list(range(3, 11)), "T", "Flag Terminus"], [0, 11, "W", "Wall"]], (True, False)], 
                           "P": [[[0, 0, "P", "Pipe (2)"], [1, 0, "P", "Pipe (3)"], [0, "11", "P", "Pipe (4)"], [1, "11", "P", "Pipe (1)"]], (True, True)], 
                           "H": [[[0, -1, "H", "Hammer Bro Head"], [0, 0, "H", "Hammer Bro Body"]], (True, True)], \
                           "K": [[[0, -1, "K", "Koopa Head"], [0, 0, "K", "Koopa Body"]], (True, True)], \
                           "^": [[[0, -1, "^", "Spring Head"], [0, 0, "^", "Spring Body"]], (True, True)], \
                           "R": [[[0, -1, "R", "Mushroom"], [0, 0, "B", "Brick"]], (True, True)], \
                           "S": [[[0, -1, "S", "Star"], [0, 0, "B", "Brick"]], (True, True)], \
                           "U": [[[0, -1, "U", "1Up Mushroom"], [0, 0, "B", "Brick"]], (True, True)], \
                           "Y": [[[0, -2, "Y", "Piranha TL"], [1, -2, "Y", "Piranha TR"], [0, -1, "Y", "Piranha BL"], \
                                  [1, -1, "Y", "Piranha BR"], [0, 0, "P", "Pipe (2)"], [1, 0, "P", "Pipe (3)"], \
                                  [0, "11", "P", "Pipe (4)"], [1, "11", "P", "Pipe (1)"]], (True, True)]}
        
        self.grid = []
        for x in range(self.length):
            for y in range(self.height):
                self.grid.append((x, y))
                
        self.__create_blank_map()
        q = self.grid_positions[(0,0)]      
        
    def __convert_coor(self, coordinates):
        if coordinates[0] - self.scroll in range(self.MAX_LENGTH):
            return (self.x_pos + self.grid_side * (coordinates[0] - self.scroll), self.y_pos + self.grid_side * coordinates[1])
        return (-1, -1)
    
    def __create_blank_map(self):
        self.grid_positions = {}
        for real_grid_loc in self.grid:
            symbol = "-"
            file_name = "Sky"
            if real_grid_loc[1] in (12, 13):
                symbol = "="
                file_name = "Floor"
            if real_grid_loc == (4, 11):
                symbol = "M"
            self.grid_positions[real_grid_loc] = Icon(real_grid_loc[0], real_grid_loc[1], symbol)
            
    def get_map(self):
        return self.grid_positions
    
    def scroll_grid(self, direction):
        if (self.scroll + direction) in range(abs(self.length - self.MAX_LENGTH)):
            self.scroll += direction
            
    def get_image(self, file):
        return self.images.setdefault(file, pygame.transform.scale(pygame.image.load('./Blocks/' + file + ".png"), (self.grid_side, self.grid_side)))
    
    def add_icon(self, real_grid_loc):
        if self.main_gui.get_icon() in self.MULTIICONS.keys():
            icon = MultiIcon(real_grid_loc[0], real_grid_loc[1], None, None, self.MULTIICONS.get(self.main_gui.get_icon())[0], self.MULTIICONS.get(self.main_gui.get_icon())[1]) 
        elif self.main_gui.get_icon() == "~":
            if real_grid_loc[1] >= 12:
                icon = Icon(real_grid_loc[0], real_grid_loc[1], "=")
            else:
                icon = Icon(real_grid_loc[0], real_grid_loc[1], "-")
        else:
            icon = Icon(real_grid_loc[0], real_grid_loc[1], self.main_gui.get_icon())      
        check = True
        for coor in icon.get_coordinates():
            if self.grid_positions[tuple(coor)].get_icon_string() in ["F", "T"] or self.grid_positions[(coor[0], coor[1] - 1)].get_icon_string() == "T":
                self.flag = None            
            if self.grid_positions[tuple(coor)].get_icon_string() == "M" or \
               not self.grid_positions[tuple(coor)].remove(self.grid_positions): 
                check = False
        if (self.main_gui.get_icon() != "-" and self.main_gui.get_icon() != "~") and real_grid_loc[1] >= 12:
            check = False
        if check: 
            if self.main_gui.get_icon() == "F":
                if self.flag: self.flag.remove(self.grid_positions)
                self.flag = icon              
            icon.create(self.grid_positions)
    
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
                    icon_image = self.grid_positions.get(real_grid_loc).get_icon_image()
                    if type(icon_image) == str:
                        icon_image = self.get_image(icon_image)
                    self.display.blit(icon_image, grid_loc)
                    rect = pygame.Rect(grid_loc[0], grid_loc[1], self.grid_side, self.grid_side)
                    pygame.draw.rect(self.display, (0,0,0), rect, 2)
                except TypeError:
                    print("Grid Loc", real_grid_loc)