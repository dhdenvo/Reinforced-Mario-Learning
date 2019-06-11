import pygame

class InteractiveGui:
    def __init__(self, display, gui, x_pos, y_pos, length = 0, width = 0):
        self.display = display
        self.main_gui = gui
        self.x_pos = x_pos
        self.y_pos = y_pos
        
    def select(self, pos):
        if pos[0] in range(self.x_pos, self.x_pos + length) and pos[1] in range(self.y_pos, self.y_pos + height):
            return True
        
    def draw(self):
        pass
        
    