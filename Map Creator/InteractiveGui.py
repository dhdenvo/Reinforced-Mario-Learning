import pygame

#A class that has all the basics for a gui
class InteractiveGui:
    def __init__(self, display, gui, x_pos, y_pos, length = 0, height = 0, background_colour = (0,0,0), colour = (0,0,0)):
        self.display = display
        self.main_gui = gui
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.length = length
        self.height = height
        self.background_colour = background_colour
        self.colour = colour
        
    #Check if a location is in the gui
    def __in_gui(self, pos):
        if (self.x_pos, self.y_pos) != (-1, -1) and pos[0] in range(self.x_pos, self.x_pos + self.length) \
           and pos[1] in range(self.y_pos, self.y_pos + self.height):
            return True        
    
    #Check if the gui is selected by the mouse
    def select(self, pos):
        return self.__in_gui(pos)
        
    #Check if the gui is released by the mouse
    def release(self, pos):
        return self.__in_gui(pos)
        
    #Draw the gui (Basic rectangle with an outline)
    def draw(self):
        pygame.draw.rect(self.display, self.background_colour, pygame.Rect(self.x_pos, self.y_pos, self.length, self.height))        
        pygame.draw.rect(self.display, self.colour, pygame.Rect(self.x_pos, self.y_pos, self.length, self.height), 4)
        
        
    