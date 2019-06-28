import pygame

grid_side = 35
SYMBOL_TRANSLATION = {"=": pygame.transform.scale(pygame.image.load('./Blocks/Floor.png'), (grid_side, grid_side)), \
                           "-": pygame.transform.scale(pygame.image.load('./Blocks/Sky.png'), (grid_side, grid_side)), \
                           "B": pygame.transform.scale(pygame.image.load('./Blocks/Brick.png'), (grid_side, grid_side)),\
                           "G": pygame.transform.scale(pygame.image.load('./Blocks/Goomba.png'), (grid_side, grid_side)),\
                           "?": pygame.transform.scale(pygame.image.load('./Blocks/Question.png'), (grid_side, grid_side)),\
                           "W": pygame.transform.scale(pygame.image.load('./Blocks/Wall.png'), (grid_side, grid_side)), \
                           "M": pygame.transform.scale(pygame.image.load('./Blocks/Mario.png'), (grid_side, grid_side))}     

class Icon:
    def __init__(self, x_pos, y_pos, icon_string, image_icon = None):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.icon_string = icon_string
        self.image_icon = image_icon   
        
    def get_grid_loc(self):
        return (self.x_pos, self.y_pos)
    
    def get_icon_string(self):
        return self.icon_string
    
    def get_coordinates(self):
        return [[self.x_pos, self.y_pos]]
    
    def create(self, grid_positions):
        grid_positions[self.get_grid_loc()] = self
        
    def remove(self, grid_positions = None):
        return True
    
    def get_icon_image(self):
        if not self.image_icon:
            return SYMBOL_TRANSLATION.get(self.icon_string, SYMBOL_TRANSLATION.get("-"))
        return self.image_icon
 
 
