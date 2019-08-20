from Icon import Icon

#A class that couples multiple icons into a single system
class MultiIcon(Icon):
    def __init__(self, x_pos, y_pos, icon_string, icon_image, relative_positions, relative = (True, True)):
        super().__init__(x_pos, y_pos, icon_string, icon_image)
        self.relative_positions = relative_positions
        self.relative = relative
        
    #Remove the icon and all coupled icons from the map    
    def remove(self, grid_positions):
        through_relatives = self.go_through_relatives()
        #Go through all the coupled icons
        for rel_pos in through_relatives:
            #Calculate x and y coordinates based on whether the locations are relative or not
            if self.relative[0]:
                x_coor = self.x_pos + rel_pos[0]
            else:
                x_coor = rel_pos[0]
            if self.relative[1]:
                y_coor = self.y_pos + rel_pos[1]
            else:
                y_coor = rel_pos[1]
            pos = (x_coor, y_coor)
            #Set the locations to the sky
            grid_positions[pos] = Icon(pos[0], pos[1], '-')
        return True
    
    #Get a list of the coordinates of all the coupled icons
    def get_coordinates(self):
        through_relatives = self.go_through_relatives()
        coordinates = []
        #If the location clicked is a valid icon of the multi icon, add its location to the list
        if self.icon_string and self.image_icon:
            coordinates.append([self.x_pos, self.y_pos])
        #Generate the coordinates of each of the coupled icons
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
    
    #Add all of the coupled icons to the map grid (for each coupled icon, a new multi icon is created)
    def create(self, grid_position):
        if self.relative == (True, True): grid_position[(self.x_pos, self.y_pos)] = self
        through_relatives = self.go_through_relatives()
        #Cycle through each of the relative positions
        for rel_pos in through_relatives:
            #Get the coordinates of the coupled icons
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
            #If the location clicked is a valid icon of the multi icon, add its location to the list            
            if self.icon_string and self.image_icon:
                rel_positions = [[-rel_pos[0], -rel_pos[1], self.icon_string, self.image_icon]]
            #Recreate the relative positions for the new multi icon
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
            #Add the new multi icon to its new position
            grid_position[pos] = MultiIcon(pos[0], pos[1], rel_pos[2], rel_pos[3], rel_positions, self.relative)
    
    #Make a list of the positions of all of the coupled icons    
    def go_through_relatives(self):
        list_of_positions = []
        for pos in self.relative_positions: 
            #When the relative position is a list, each coordinate in the list is coupled
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
            #When the relative position is a string, the coordinate is different than a normal coordinate
            elif type(pos[1]) == str:
                for y_pos in range(self.y_pos + 1, int(pos[1]) + 1):
                    list_of_positions.append([pos[0], y_pos - self.y_pos, pos[2], pos[3]])
            else:
                list_of_positions.append(pos[:])
        return list_of_positions