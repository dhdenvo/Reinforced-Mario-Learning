import pygame
import sys
from MainGui import MainGui

pygame.init()
pygame.font.init()
display = pygame.display.set_mode((1400, 788))
pygame.display.set_caption('Mario World Creator')

clock = pygame.time.Clock()

def create_level(gui):
    print("Hello There")
    
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
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                gui.select(pos)
                
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()     
        display.fill((182,213,251))
        gui.draw()
        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
sys.exit()