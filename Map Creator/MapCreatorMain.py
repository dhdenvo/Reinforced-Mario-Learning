import pygame
import sys
import gc
import os
from MainGui import MainGui

#Prepare the pygame gui
pygame.init()
pygame.font.init()
display = pygame.display.set_mode((1400, 788))
pygame.display.set_caption('Mario World Creator')

clock = pygame.time.Clock()

MULTIICONS = ['H', 'K', '^', 'R', 'S', 'U', 'Y']

#Save the level as a rom file
def create_level(gui):
    map = gui.get_map()
    measurement = gui.get_map_measurements()
    map_representation = []
    length = measurement[0]
    flag_check = False
    for x in range(measurement[0]):
        if map.get((x, 4)).get_icon_string() == "T":
            flag_check = True
            length = x + 3
            break
    #If no flag is drawn, draw a flag at the end of the map
    if not flag_check:
        gui.draw_flag(measurement[0] - 3)
    
    #Convert the map into a text file
    for y in range(measurement[1]):
        map_representation.append(["-"] * length)
        for x in range(length):
            try:
                if map.get((x, y)).get_icon_string() in MULTIICONS and map.get((x, y)).get_icon_string() == map.get((x, y + 1)).get_icon_string():
                    map_representation[y][x] = '-'
                else:
                    map_representation[y][x] = map.get((x, y)).get_icon_string()     
            except AttributeError:
                map_representation[y][x] = map.get((x, y)).get_icon_string()    
        map_representation[y] = "".join(map_representation[y])
    map_representation = "\n".join(map_representation)
    
    #Use the command line arguments to adjust options for the demo
    level_name = "map.txt"
    gen = 0
    if len(sys.argv) > 1:
        level_name = sys.argv[1]
    if len(sys.argv) > 2:
        gen = sys.argv[2]
        print("Gen:" + gen)
        
    #Save the map as a text file
    f = open("../Level Generator/" + level_name, "w")
    f.write(map_representation)
    f.close()
    #Convert the text file into a rom (using the VirtualAdditionOfLevels python program)
    os.system("cd ../Level\ Generator/; python VirtualAdditionOfLevels.py " + level_name)
    print("Rom File Created")
    #print("cd ../Reinforced\ Mario\ Demo/; python RunDemoMain.py -rom Super Mario Bros - " + level_name.split(".")[0] + ".nes" + " -gen " + str(gen) + " -uni True")
    #Run the demo with the newly created rom and gen option from the command line arguments (using the RunDemoMain python program)
    os.system("cd ../Reinforced\ Mario\ Demo/; python RunDemoMain.py -rom 'Super Mario Bros - " + level_name.split(".")[0] + ".nes'" + " -gen " + str(gen) + " -uni True")
    quit()
    
#Move the map either left or right
def move_map(gui, direction):
    gui.scroll(direction)
    
#Move the map's view left
def move_left(gui):
    move_map(gui, -1)
    
#Move the map's view right
def move_right(gui):
    move_map(gui, 1)

#The loop that runs all the aspects of the gui
def game_loop():
    gui = MainGui(display)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                gui.select(pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                gui.release(pos)
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()     
        #Reset the appearance of the view
        display.fill((182,213,251))
        #Draw the map creator gui
        gui.draw()
        pygame.display.update()
        gc.collect()        
        clock.tick(60)

#Start the application's loop
game_loop()
pygame.quit()
sys.exit()
