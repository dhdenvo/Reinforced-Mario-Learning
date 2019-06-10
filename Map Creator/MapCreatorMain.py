import pygame
import sys

pygame.init()
displaysurf = pygame.display.set_mode((1400, 788))
pygame.display.set_caption('Mario World Creator')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()     
    pygame.display.update()

        