class Icon:
    def __init__(self, x_pos, y_pos, icon_string):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.icon_string = icon_string
        
    def get_grid_loc(self):
        return (self.x_pos, self.y_pos)
    
    def get_icon_string(self):
        return self.icon_string
    
    def create(self, grid_positions):
        grid_positions[self.get_grid_loc()] = self
        
    def remove(self, grid_positions = None):
        return True
        