import pygame
import sys
from MainGui import MainGui

pygame.init()
display = pygame.display.set_mode((1400, 788))
pygame.display.set_caption('Mario World Creator')

clock = pygame.time.Clock()

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