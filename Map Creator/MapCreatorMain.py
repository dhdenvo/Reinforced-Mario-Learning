import pygame
import sys
import gc
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
    for y in range(measurement[1]):
        map_representation.append(["-"] * measurement[0])
        for x in range(measurement[0]):
            map_representation[y][x] = map.get((x, y)).get_icon_string()
        map_representation[y] = "".join(map_representation[y])
    map_representation = "\n".join(map_representation)
    
    f = open("map.txt", "w")
    f.write(map_representation)
    f.close()
    
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