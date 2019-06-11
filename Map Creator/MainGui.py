from MapGui import MapGui

class MainGui:
    
    def __init__(self, display):
        self.map = MapGui(display, 40, 80, 115, 12, 40)
        
    def select(self, pos):
        self.map(select)
    
    def draw(self):
        self.map.draw()
        
        