import pygame
from InteractiveGui import InteractiveGui

#A class that makes creating buttons easy
class ButtonGui(InteractiveGui):
    def __init__(self, display, gui, x_pos, y_pos, length, height, text, push_function, background_colour = (0,0,0), font_size = 20, colour = (0,0,0)):
        super().__init__(display, gui, x_pos, y_pos, length, height, background_colour, colour)
        self.text = text
        self.font_size = font_size
        self.push_function = push_function
        self.changed = False
        
    #Change the background of the button by a set value
    def change_background(self, colour_change):
        self.background_colour = (self.background_colour[0] + colour_change[0], self.background_colour[1] + colour_change[1], self.background_colour[2] + colour_change[2])
    
    #Run the button's function when the button is pressed (selected)
    def select(self, pos):
        if super().select(pos):
            #Change the background colour to show that it is pressed
            if not self.changed:
                self.change_background((-50,-50,-50))                
            self.changed = True
            #Run the button's function
            self.push_function(self.main_gui)
            
    #Change the background back to normal when the mouse is released        
    def release(self, pos):
        if self.changed:
            self.change_background((50,50,50))                
        self.changed = False   
            
    #Draw the button using the default interactive gui drawing function and drawing the text
    def draw(self):
        #Draw the background and the outline (using default interactive gui drawing function)
        super().draw()
        #Draw the text of the button
        font = pygame.font.Font('Fonts/SuperMario256.ttf', self.font_size)
        surface = font.render(self.text, False, self.colour)
        self.display.blit(surface, (self.x_pos + 6, self.y_pos + 6))        