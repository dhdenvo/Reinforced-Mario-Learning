import pygame
from MapGui import MapGui
from IconSelectGui import IconSelectGui
from ButtonGui import ButtonGui

grid_side = 50
#Load and scale an image by the file (icon) name
def get_image(file):
    return pygame.transform.scale(pygame.image.load('./Blocks/' + file + ".png"), (grid_side, grid_side))

SYMBOL_TRANSLATION = {"=": get_image("Floor"), "-": get_image("Sky"), "B": get_image("Brick"), "G": get_image("Goomba"),\
                           "?": get_image("Question"), "W": get_image("Wall"), "M": get_image("Mario"), "<": get_image("Bullet"), \
                           "P": get_image("Pipe"), "F": get_image("Flag"), "C": get_image("Coin"), "E": get_image("Buzzy Beetle"), \
                           "X": get_image("Spiny"), "K": get_image("Koopa"), "H": get_image("Hammer Bro"), "^": get_image("Spring Head"), \
                           "S": get_image("Star"), "R": get_image("Mushroom"), "U": get_image("1Up Mushroom"), \
                           "Y": get_image("Piranha"), "~": get_image("Eraser")}

#A class that combines all the other guis into one
class MainGui:
    def __init__(self, display):
        from MapCreatorMain import create_level  
        from MapCreatorMain import move_left
        from MapCreatorMain import move_right
        
        #All options of icons for the icon select gui
        icons = ["-", "B", "P", "G", "?", "U", "^", "Y", "F", "S", "C", "<", "E", "X", "R", "H", "K", "~"]
        self.selected_icon = "-"   
        self.display = display
        
        self.map_height = 14
        self.map_length = 200
        
        #A dictionary of the different types of guis
        self.guis = {}
        self.guis["map"] = MapGui(display, self, 40, 80, self.map_length, self.map_height, 35)
        self.guis["icon_select"] = IconSelectGui(display, self, 1240, 80, 50, icons)
        self.guis["create_button"] = ButtonGui(display, self, 40, 680, 215, 50, "Create", create_level, (155,181,204), 50)  
        self.guis["left_button"] = ButtonGui(display, self, 40, 590, 64, 64, "<", move_left, (155,181,204), 64)
        self.guis["right_button"] = ButtonGui(display, self, 1100, 590, 64, 64, ">", move_right, (155,181,204), 64)        
        
    #For each gui, run their select function which checks if the gui is pushed
    def select(self, pos):
        for gui in self.guis.values():
            gui.select(pos)
    
    #For each gui, run their select function which checks if the gui is released        
    def release(self, pos):
        for gui in self.guis.values():
            gui.release(pos)
    
    #Get the currently selected icon
    def get_icon(self):
        return self.selected_icon
    
    #Set the currently selected icon
    def set_icon(self, icon):
        self.selected_icon = icon
        
    #Draw the flag at the specified x location
    def draw_flag(self, x):
        old_icon = self.get_icon()
        self.set_icon("F")
        self.guis["map"].add_icon((x, 4))
        self.set_icon(old_icon)
        
    #Return the map dictionary
    def get_map(self):
        return self.guis["map"].get_map()
    
    #Get the size of the map
    def get_map_measurements(self):
        return (self.map_length, self.map_height)
    
    #Scroll the map left or right
    def scroll(self, direction):
        self.guis["map"].scroll_grid(direction)
    
    #Draw text on the gui (makes it easier to mass draw text)
    def __create_text(self, text, x, y, size):
        font = pygame.font.Font('Fonts/SuperMario256.ttf', size)
        surface = font.render(text, False, (0, 0, 0))
        self.display.blit(surface, (x, y))
    
    #Draw all the guis
    def draw(self):
        #Decorative Stuff (Mario Image and Floor)
        self.display.blit(pygame.transform.scale(pygame.image.load('./DecorativeImage.jpg'), (337, 211)), (650, 584))        
        x = 0
        while x < 1200:
            self.display.blit(pygame.transform.scale(pygame.image.load('./Blocks/Floor.png'), (32, 32)), (x, 756))
            x += 32
            
        #Basic Rectangles For Visuals and Separation
        pygame.draw.rect(self.display, (155,181,204), pygame.Rect(1200, 0, 200, 788), 0)
        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(1200, 0, 10, 788), 0)
        pygame.draw.rect(self.display, (0,0,0), pygame.Rect(36, 76, 1128, 498), 0)
        
        #Headers
        self.__create_text("Blocks", 1226, 20, 40)
        self.__create_text("Super Mario Bros - Mario Maker NES", 40, 20, 40)    
        
        #Drawing classes
        for gui in self.guis.values():
            gui.draw()
        
        
        