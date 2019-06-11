import pygame

class InteractiveGui:
    def __init__(self, display, gui, x_pos, y_pos, length = 0, height = 0):
        self.display = display
        self.main_gui = gui
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        
    def select(self, pos):
        if (self.x_pos, self.y_pos) != (-1, -1) and pos[0] in range(self.x_pos, self.x_pos + self.length) \
           and pos[1] in range(self.y_pos, self.y_pos + self.height):
            return True
        
    def draw(self):
        pass
        
    