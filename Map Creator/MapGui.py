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
            self.grid_positions[real_grid_loc] = Icon(real_grid_loc[0], real_grid_loc[1], symbol)
            
    def get_map(self):
        return self.grid_positions
    
    def scroll_grid(self, direction):
        if (self.scroll + direction) in range(abs(self.length - self.MAX_LENGTH)):
            self.scroll += direction
            
    def get_image(self, file):
        return self.images.setdefault(file, pygame.transform.scale(pygame.image.load('./Blocks/' + file + ".png"), (self.grid_side, self.grid_side)))
    
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
            icon = MultiIcon(real_grid_loc[0], real_grid_loc[1], None, None, \
                             [[0, 1, "F", "Flag Ball"], [0, 2, "F", "Flag Main"], [-1, 2, "F", "Flag Edge"], \
                              [0, list(range(3, 11)), "T", "Flag Terminus"], [0, 11, "W", "Wall"]], (True, False)) 
        else:
            icon = Icon(real_grid_loc[0], real_grid_loc[1], self.main_gui.get_icon())
        if self.main_gui.get_icon() == "F":
            if self.flag: self.flag.remove(self.grid_positions)
            self.flag = icon        
        check = True
        for coor in icon.get_coordinates():
            if not self.grid_positions[tuple(coor)].remove(self.grid_positions): 
                check = False
        if check: icon.create(self.grid_positions)

    
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