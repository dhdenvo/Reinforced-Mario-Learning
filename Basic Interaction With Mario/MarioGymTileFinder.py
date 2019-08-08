import cv2

BoxRadius = 6

def stuffs(state, dx, dy, marioX, marioY, displacement_x, displacement_y):
    x = marioX + dx - displacement_x
    y = marioY + dy - displacement_y
    if x >= 0 and y >= 0 and x + 16 <= 240 and y + 16 <= 256:   
        crop_state = state[x:x+16, y:y+16]    
        cv2.imshow("img", crop_state)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
def get_inputs(state, marioX, marioY):
    inputs = []
    displacement_x = marioX % 16
    displacement_y = marioY % 16
    
    for dy in range(-BoxRadius * 16, (BoxRadius + 1) * 16, 16):
        for dx in range(-BoxRadius * 16, (BoxRadius + 1) * 16, 16):
            inputs.append(0)

            #If the area is a block
            tile = stuffs(state, dx, dy,marioX, marioY, displacement_x, displacement_y)
            if tile == 1 and marioY+dy < 0x1B0:
                inputs[-1] = 1

            sprites = []
            #If the area is in range of a monster its a monster
            for i in range(0,len(sprites)):
                distx = abs(sprites[i]["x"] - (marioX+dx))
                disty = abs(sprites[i]["y"] - (marioY+dy))
                if distx <= 8 and disty <= 8:
                    inputs[-1] = -1
    return inputs


info = {'coins': 0, 'flag_get': False, 'life': 2, 'score': 0, 'stage': 1, 'status': 'small', 'time': 393, 'world': 1, 'x_pos': 259, 'y_pos': 79}
marioX = info["x_pos"]
marioY = info["y_pos"]

frame = cv2.imread("Stuffs.png")

#cv2.imshow("img", frame)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

get_inputs(frame, marioX, marioY)

