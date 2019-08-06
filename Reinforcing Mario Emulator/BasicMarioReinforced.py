from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from MarioNESRomEnv import MarioNESRomEnv
import cv2
import math
from time import sleep
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
env = MarioNESRomEnv("/home/DavidDaghelian/Programs/Pie-Thon/Super Mario Bros Programs/Super Mario Bros Details/Final Products/Super Mario Bros (Machine Learned).nes")
env = JoypadSpace(env, SIMPLE_MOVEMENT)

BoxRadius = 6
done = True
frame = 0


def stuffs(state, ram, dx, dy, marioX, marioY):
    x = marioX + dx + 8
    y = marioY + dy - 16
    #cv2.imshow("img", state)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    page = math.floor(x/256)%2

    subx = math.floor((x%256)/16)
    suby = math.floor((y - 32)/16)
    addr = 0x500 + page*13*16+suby*16+subx

    if suby >= 13 or suby < 0:
        return 0

    if ram[addr] != 0:
        return 1
    else:
        return 0    
    
def get_inputs(state, ram, marioX, marioY):
    inputs = []
    
    state = cv2.rectangle(state, (marioX, marioY), (marioX + 16, marioY + 16), (0, 255, 0), 3)    
    
    for dy in range(-BoxRadius * 16, (BoxRadius + 1) * 16, 16):
        for dx in range(-BoxRadius * 16, (BoxRadius + 1) * 16, 16):
            inputs.append(0)

            #If the area is a block
            tile = stuffs(state, ram, dx, dy, marioX, marioY)
            if tile == 1 and marioY+dy < 0x1B0:
                inputs[-1] = 1
                screenX = ram[0x03AD]
                screenY = ram[0x03B8]                
                x = screenX + dx + 8
                y = screenY + dy - 16
                state = cv2.rectangle(state, (x, y), (x + 16, y + 16), (0, 255, 0), 3)
                #print(marioX, marioY, dx, dy)
            #x = marioX + dx - marioX % 16
            #y = marioY + dy - marioY % 16
            #state = cv2.rectangle(state, (x, y), (x + 16, y + 16), (0, 255, 0), 3)
            #print("HELLO")

            sprites = []
            #If the area is in range of a monster its a monster
            for i in range(0,len(sprites)):
                distx = abs(sprites[i]["x"] - (marioX+dx))
                disty = abs(sprites[i]["y"] - (marioY+dy))
                if distx <= 8 and disty <= 8:
                    inputs[-1] = -1
    return inputs, state

while True:
       
    if done:
        state = env.reset()
        frame = 0
        
    x = 6
    if frame % 100 == 0:
        x = 1
    
    state, reward, done, info = env.step(env.action_space.sample())
    #print("\n\n\n\nBLLLLLLLLLLLLLLLLLAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHH")
    #print(list(state))
    #print(reward)
    #print(done)
    #print(info)
    #print(reward, info["x_pos"], info["y_pos"]) 
    
    #marioX = info["x_pos"]
    #marioY = info["y_pos"]
    
    ram = info["ram"]
    
    marioX = ram[0x6D] * 0x100 + ram[0x86]
    marioY = ram[0x03B8]+16

    screenX = ram[0x03AD]
    screenY = ram[0x03B8]     
    
    #for i, x in enumerate(env.ram):
        #if i in range(1280, 1695):
            #print(x)
    inputs, state = get_inputs(state, ram, marioX, marioY)
    #print(inputs)
    y = False
    for i, x in enumerate(inputs):
        if x == 1:
            #print(i, x)
            y = True
    '''if y or 1 == 1:
        frame_pic = cv2.cvtColor(state, cv2.COLOR_RGB2BGR)        
        cv2.imshow("img", frame_pic)
        #cv2.waitKey(0)
        cv2.destroyAllWindows()        
        #sleep(10)
    
    print(id(ram))'''
    
    if frame % 1000 == 0:
        print("HI")
    
    #sleep(5)
    
    #if marioX % 16 == 0:
    #    frame_pic = cv2.cvtColor(state, cv2.COLOR_RGB2BGR)
    #    cv2.imwrite("Stuffs.png", frame_pic)    
    
    
    env.render()
    frame += 1
    #if (info["time"] == 393):
    #    print(info)
    #    frame_pic = cv2.cvtColor(state, cv2.COLOR_RGB2BGR)
    #    cv2.imwrite("Stuffs.png", frame_pic)
    #    env.reset()
    #    frame = 0

env.close()