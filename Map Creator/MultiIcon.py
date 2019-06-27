from Icon import Icon

class MultiIcon(Icon):
    def __init__(self, x_pos, y_pos, icon_string, relative_positions, relative = (True, True)):
        super().__init__(x_pos, y_pos, icon_string)
        self.relative_positions = relative_positions
        self.relative = relative
        
    def remove(self, grid_positions):
        for rel_pos in self.relative_positions:
            pos = (self.x_pos + rel_pos[0], self.y_pos + rel_pos[1])
            grid_positions[pos] = Icon(pos[0], pos[1], '-')
        return True
    
    def create(self, grid_position):
        grid_position[(self.x_pos, self.y_pos)] = self
        for rel_pos in self.relative_positions:
            pos = (self.x_pos + rel_pos[0], self.y_pos + rel_pos[1])
            rel_positions = [(-rel_pos[0], -rel_pos[1])]
            for i in range(len(self.relative_positions)):
                if rel_pos != self.relative_positions[i]:
                    rel_positions.append((self.relative_positions[i][0] - rel_pos[0], self.relative_positions[i][1] - rel_pos[1]))
            grid_position[pos] = MultiIcon(pos[0], pos[1], self.icon_string, rel_positions, self.relative)