from NeuralConstants import *
import pygame


class Cell:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

def create_gui():
    pygame.init()
    pygame.font.init()
    display = pygame.display.set_mode((1400, 788))
    pygame.display.set_caption('Mario World Creator')
    
    clock = pygame.time.Clock() 
    return display


def displayGenome(display, genome):
    display.fill((182,213,251))  
    
    network = genome.network
    cells = {}
    i = 1
    for dy in range(-BoxRadius, BoxRadius + 1):
        for dx in range(-BoxRadius, BoxRadius + 1):
            cell = Cell(50+5*dx, 70+5*dy, network.neurons[i].value)
            cells[i] = cell 
            i = i + 1
                
    biasCell = Cell(80, 110, network.neurons[Inputs].value)
    cells[Inputs] = biasCell

    for o in range(0,Outputs + 1):
        cell = Cell(220, 30 + 8 * o, network.neurons[MaxNodes + o].value)
        cells[MaxNodes+o] = cell
        color
        if cell.value > 0:
            color = 0xFF0000FF
        else:
            color = 0xFF000000
        font = pygame.font.Font('Comic Sans MS', 9)
        surface = font.render(ButtonNames[o], False, (0,0,0))
        display.blit(surface, (223, 24+8*o))   
        #gui.drawText(223, 24+8*o, ButtonNames[o], color, 9)

    for n,neuron in network.neurons.items():
        if n > Inputs and n <= MaxNodes:
            cell = Cell(140, 40,  neuron.value)           
            cells[n] = cell

    for n in range(1,5):
        for gene in genome.genes:
            if gene.enabled:
                c1 = cells[gene.into]
                c2 = cells[gene.out]
                if gene.into > Inputs and gene.into <= MaxNodes:
                    c1.x = 0.75*c1.x + 0.25*c2.x
                    if c1.x >= c2.x:
                        c1.x = c1.x - 40
                    if c1.x < 90:
                        c1.x = 90
                    if c1.x > 220:
                        c1.x = 220
                    
                    c1.y = 0.75*c1.y + 0.25*c2.y
                    
                if gene.out > Inputs and gene.out <= MaxNodes:
                    c2.x = 0.25*c1.x + 0.75*c2.x
                    if c1.x >= c2.x:
                        c2.x = c2.x + 40
                    if c2.x < 90:
                        c2.x = 90
                    if c2.x > 220:
                        c2.x = 220
                    c2.y = 0.25*c1.y + 0.75*c2.y

    pygame.draw.rect(display, (128, 128, 128), pygame.Rect(50-BoxRadius*5-3,70-BoxRadius*5-3,50+BoxRadius*5+2,70+BoxRadius*5+2), 3)
    #gui.drawBox(50-BoxRadius*5-3,70-BoxRadius*5-3,50+BoxRadius*5+2,70+BoxRadius*5+2,0xFF000000, 0x80808080)
    
    for n,cell in cells.items():
        if n > Inputs or cell.value != 0:
            color = math.floor((cell.value+1)/2*256)
            if color > 255: 
                color = 255
            if color < 0:
                color = 0
            opacity = 0xFF000000
            if cell.value == 0:
                opacity = 0x50000000
                
            color = opacity + color*0x10000 + color*0x100 + color
            pygame.draw.rect(display, pygame.Color(str(color)[-6:]), pygame.Rect(cell.x-2,cell.y-2,cell.x+2,cell.y+2), 3)
            #gui.drawBox(cell.x-2,cell.y-2,cell.x+2,cell.y+2,opacity,color)
        
    for gene in genome.genes:
        if gene.enabled:
            c1 = cells[gene.into]
            c2 = cells[gene.out]
            opacity = 0xA0000000
            if c1.value == 0:
                opacity = 0x20000000

            color = 0x80-math.floor(math.abs(sigmoid(gene.weight))*0x80)
            if gene.weight > 0:
                color = opacity + 0x8000 + 0x10000*color
            else:
                color = opacity + 0x800000 + 0x100*color
            pygame.draw.line(display, pygame.Color(str(color)[-6:]), (c1.x+1, c1.y), (c2.x-3, c2.y), 3)
            #gui.drawLine(c1.x+1, c1.y, c2.x-3, c2.y, color)

    #gui.drawBox(49,71,51,78,0x00000000,0x80FF0000)
