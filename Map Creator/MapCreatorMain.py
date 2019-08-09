import pygame
import sys
import gc
import os
from MainGui import MainGui

pygame.init()
pygame.font.init()
display = pygame.display.set_mode((1400, 788))
pygame.display.set_caption('Mario World Creator')

clock = pygame.time.Clock()

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
    if not flag_check:
        gui.draw_flag(measurement[0] - 3)
    for y in range(measurement[1]):
        map_representation.append(["-"] * length)
        for x in range(length):
            map_representation[y][x] = map.get((x, y)).get_icon_string()
        map_representation[y] = "".join(map_representation[y])
    map_representation = "\n".join(map_representation)
    
    level_name = "map.txt"
    gen = 0
    if len(sys.argv) > 2:
        level_name = sys.argv[1]
    if len(sys.argv) > 3:
        gen = sys.argv[2]
        
    
    f = open("../Level Generator/" + level_name, "w")
    f.write(map_representation)
    f.close()
    os.system("cd ../Level\ Generator/; python VirtualAdditionOfLevels.py " + level_name)
    print("Rom File Created")
    os.system("cd ../Reinforced\ Mario\ Demo/; python RunDemoMain.py -rom Super Mario Bros - " + level_name.split(".")[0] + ".nes" + " -gen " + gen)
    quit()
    
def move_map(gui, direction):
    gui.scroll(direction)
    
def move_left(gui):
    move_map(gui, -1)
    
def move_right(gui):
    move_map(gui, 1)

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
        display.fill((182,213,251))
        gui.draw()
        pygame.display.update()
        gc.collect()        
        clock.tick(60)

game_loop()
pygame.quit()
sys.exit()