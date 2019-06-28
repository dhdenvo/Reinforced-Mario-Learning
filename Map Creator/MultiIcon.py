from Icon import Icon

class MultiIcon(Icon):
    def __init__(self, x_pos, y_pos, icon_string, icon_image, relative_positions, relative = (True, True)):
        super().__init__(x_pos, y_pos, icon_string, icon_image)
        self.relative_positions = relative_positions
        self.relative = relative
        
    def remove(self, grid_positions):
        through_relatives = self.go_through_relatives()
        for rel_pos in through_relatives:
            if self.relative[0]:
                x_coor = self.x_pos + rel_pos[0]
            else:
                x_coor = rel_pos[0]
            if self.relative[1]:
                y_coor = self.y_pos + rel_pos[1]
            else:
                y_coor = rel_pos[1]
            pos = (x_coor, y_coor)
            grid_positions[pos] = Icon(pos[0], pos[1], '-')
        return True
    
    def get_coordinates(self):
        through_relatives = self.go_through_relatives()
        coordinates = []
        if self.icon_string and self.image_icon:
            coordinates.append([self.x_pos, self.y_pos])
        for rel_pos in through_relatives:
            if self.relative[0]:
                x_coor = self.x_pos + rel_pos[0]
            else:
                x_coor = rel_pos[0]
            if self.relative[1]:
                y_coor = self.y_pos + rel_pos[1]
            else:
                y_coor = rel_pos[1]
            coordinates.append([x_coor, y_coor])
        return coordinates
    
    def create(self, grid_position):
        if self.relative == (True, True): grid_position[(self.x_pos, self.y_pos)] = self
        through_relatives = self.go_through_relatives()
        for rel_pos in through_relatives:
            if self.relative[0]:
                x_coor = self.x_pos + rel_pos[0]
            else:
                x_coor = rel_pos[0]
            if self.relative[1]:
                y_coor = self.y_pos + rel_pos[1]
            else:
                y_coor = rel_pos[1]
            
            pos = (x_coor, y_coor)
            rel_positions = []
            if self.icon_string and self.image_icon:
                rel_positions = [[-rel_pos[0], -rel_pos[1], self.icon_string, self.image_icon]]
            for i in range(len(through_relatives)):
                if self.relative[0]:
                    pair_x_coor = through_relatives[i][0] - rel_pos[0]
                else:
                    pair_x_coor = through_relatives[i][0]
                if self.relative[1]:
                    pair_y_coor = through_relatives[i][1] - rel_pos[1]
                else:
                    pair_y_coor = through_relatives[i][1]
                rel_positions.append([pair_x_coor, pair_y_coor, through_relatives[i][2], through_relatives[i][3]])
            grid_position[pos] = MultiIcon(pos[0], pos[1], rel_pos[2], rel_pos[3], rel_positions, self.relative)
            
    def go_through_relatives(self):
        list_of_positions = []
        for pos in self.relative_positions: 
            if type(pos[0]) == list:
                for x_pos in pos[0]:
                    if type(pos[1]) == list:
                        for y_pos in pos[1]:
                            list_of_positions.append([x_pos, y_pos, pos[2], pos[3]])
                    else:
                        list_of_positions.append([x_pos, pos[1], pos[2], pos[3]])
            elif type(pos[1]) == list:
                for y_pos in pos[1]:
                    list_of_positions.append([pos[0], y_pos, pos[2], pos[3]])
            elif type(pos[1]) == str:
                for y_pos in range(self.y_pos + 1, int(pos[1]) + 1):
                    list_of_positions.append([pos[0], y_pos - self.y_pos, pos[2], pos[3]])
            else:
                list_of_positions.append(pos[:])
        return list_of_positions