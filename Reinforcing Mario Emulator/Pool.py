import math
import random
from Species import Species
from Network import Network
from Genome import Genome
from Gene import Gene
from NeuralConstants import *


def getSprites(ram):
    sprites = []
    for slot in range(0,5):
        enemy = ram[0xF+slot]
        if enemy != 0:
            ex = ram[0x6E + slot]*0x100 + ram[0x87+slot]
            ey = ram[0xCF + slot]+24
            sprites.append({"x":ex,"y":ey})

    return sprites

class Pool:
    def __init__(self, env):
        self.env = env
        self.species = []
        self.globals = []
        self.controller = {}
        self.clearJoypad()
        self.rightmost = 0
        self.timeout = 0
        self.marioX = 0
        self.marioY = 0
        self.ram = env.ram
        self.screenX = 0
        self.screenY = 0
        self.generation = 0
        self.innovation = Outputs
        self.currentSpecies = 0
        self.currentGenome = 0
        self.currentFrame = 0
        self.maxFitness = 0
        
    def clearJoypad(self):
        for b in ButtonNames:
            self.controller[b] = False
        
    def getTile(self, ram, dx, dy):
        x = self.marioX + dx + 8
        y = self.marioY + dy - 16
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
        
    def getInputs(self):
        marioX = self.marioX
        marioY = self.marioY
        ram = self.ram
    
        sprites = getSprites(ram)
    
        inputs = {}
    
        for dy in range(-BoxRadius * 16, (BoxRadius + 1) * 16, 16):
            for dx in range(-BoxRadius * 16, (BoxRadius + 1) * 16, 16):
                inputs[len(inputs) + 1] = 0
    
                tile = self.getTile(ram, dx, dy)
                if tile == 1 and marioY+dy < 0x1B0:
                    inputs[len(inputs)] = 1
    
                for i in range(0,len(sprites)):
                    distx = abs(sprites[i]["x"] - (marioX+dx))
                    disty = abs(sprites[i]["y"] - (marioY+dy))
                    if distx <= 8 and disty <= 8:
                        inputs[len(inputs)] = -1
    
        #mariovx = ram[0x7B]
        #mariovy = ram[0x7D]
    
        return inputs        
        
    def new_innovation(self):
        self.innovation = self.innovation + 1
        return self.innovation    
    
    def rankGlobally(self):
        self.globals = []
        for s in range(0,len(self.species)):
            species = self.species[s]
            for g in range(0,len(species.genomes)):
                self.globals.append(species.genomes[g])
        
        self.globals = sorted(self.globals, key=lambda k: k.fitness)                
        #table.sort(globals, def (a,b)
        #    return (a.fitness < b.fitness)
        #end)
    
        for g in range(0,len(globals)):
            self.globals[g].globalRank = g
            
    def totalAverageFitness(self):
        total = 0
        for s in range(0,len(self.species)):
            species = self.species[s]
            total = total + species.averageFitness
    
        return total  
         
    def cullSpecies(self, cutToOne):
        for s in range(0,len(self.species)):
            species = self.species[s]
    
            species.genomes = sorted(species.genomes, key=lambda k: k.fitness)[::-1]                 
            #table.sort(species.genomes, def (a,b)
            #    return (a.fitness > b.fitness)
            #end)
    
            remaining = math.ceil(len(species.genomes)/2)
            if cutToOne:
                remaining = 1
            while len(species.genomes) > remaining:
                species.genomes.pop(-1)
                
    def removeStaleSpecies(self):
        survived = []
    
        for s in range(0, len(self.species)):
            species = self.species[s]
    
            species.genomes = sorted(species.genomes, key=lambda k: k.fitness)[::-1]        
            #table.sort(species.genomes, def (a,b)
            #    return (a.fitness > b.fitness)
            #end)
    
            if species.genomes[1].fitness > species.topFitness:
                species.topFitness = species.genomes[1].fitness
                species.staleness = 0
            else:
                species.staleness = species.staleness + 1
            if species.staleness < StaleSpecies or species.topFitness >= self.maxFitness:
                survived.append(species)
    
        self.species = survived 
        
    def removeWeakSpecies(self):
        survived = []
    
        sum = totalAverageFitness()
        for s in range(0,len(self.species)):
            species = self.species[s]
            breed = math.floor(species.averageFitness / sum * Population)
            if breed >= 1:
                survived.append(species)
    
        self.species = survived
        
    def addToSpecies(self, child):
        foundSpecies = False
        for s in range(0,len(self.species)):
            species = self.species[s]
            if not foundSpecies and child.sameSpecies(species.genomes[0]):
                species.genomes.append(child)
                foundSpecies = True
    
        if not foundSpecies:
            childSpecies = Species()
            childSpecies.genomes.append(child)
            self.species.append(childSpecies)
            
    def newGeneration(self):
        self.cullSpecies(False) # Cull the bottom half of each species
        self.rankGlobally()
        self.removeStaleSpecies()
        self.rankGlobally()
        for s in range(0,len(self.species)):
            species = self.species[s]
            species.calculateAverageFitness()
        self.removeWeakSpecies()
        sum = totalAverageFitness()
        children = []
        
        for s in range(0,len(self.species)):
            species = self.species[s]
            breed = math.floor(species.averageFitness / sum * Population) - 1
            for i in range(0,breed):
                children.append(species.breedChild())
                
        cullSpecies(True) # Cull all but the top member of each species
        
        while len(children) + len(self.species) < Population:
            species = self.species[random.randint(1, len(self.species))]
            children.append(species.breedChild())
        
        for c in range(0,len(children)):
            child = children[c]
            self.addToSpecies(child)
    
        self.generation = self.generation + 1

        #writeFile("backup." .. pool.generation .. "." .. forms.gettext(saveLoadFile))
        ###########Add write file / make able to be accessed
        #self.writeFile("backup." + str(self.generation) + ".")	
        
        
    def evaluateCurrent(self):
        species = self.species[self.currentSpecies]
        genome = species.genomes[self.currentGenome]

        inputs = self.getInputs()
        self.controller = genome.network.evaluateNetwork(inputs)
        for b in ButtonNames:
            self.controller.setdefault(b, False)

        if self.controller["left"] and self.controller["right"]:
            self.controller["left"] = False
            self.controller["right"] = False
        if self.controller["up"] and self.controller["down"]:
            self.controller["up"] = False
            self.controller["down"] = False
            
    
    def initializeRun(self):
        #savestate.load(Filename);
        self.env.reset()
        self.rightmost = 0
        self.currentFrame = 0
        self.timeout = TimeoutConstant
        self.clearJoypad()
    
        species = self.species[self.currentSpecies]
        genome = species.genomes[self.currentGenome]
        genome.network = Network(genome)
        self.evaluateCurrent()    
        
    def nextGenome(self):
        self.currentGenome = self.currentGenome + 1
        if self.currentGenome > len(self.species[self.currentSpecies].genomes) - 1:
            self.currentGenome = 0
            self.currentSpecies = self.currentSpecies + 1
            if self.currentSpecies > len(self.species):
                self.newGeneration()
                self.currentSpecies = 0
                
    def fitnessAlreadyMeasured(self):
        species = self.species[self.currentSpecies]
        genome = species.genomes[self.currentGenome]
    
        return genome.fitness != 0  
    
    def playTop():
        maxfitness = 0
        maxs, maxg = 0,0
        for s,species in enumerate(self.species):
            for g,genome in enumerate(species.genomes):
                print(s, g)
                if genome.fitness > maxfitness:
                    maxfitness = genome.fitness
                    maxs = s
                    maxg = g
    
        self.currentSpecies = maxs
        self.currentGenome = maxg
        self.maxFitness = maxfitness
        #gui.text(5, 8, "Max Fitness: " .. math.floor(pool.maxFitness))
        #forms.settext(maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
        self.initializeRun()
        self.currentFrame = self.currentFrame + 1
    
    def writeFile(self, filename):
        file = open(filename, "w")
        file.write(str(self.generation) + "\n")
        file.write(str(self.maxFitness) + "\n")
        file.write(str(len(self.species)) + "\n")
        for n,species in enumerate(self.species):
            file.write(str(species.topFitness) + "\n")
            file.write(str(species.staleness) + "\n")
            file.write(str(len(species.genomes)) + "\n")
            for m,genome in enumerate(species.genomes):
                file.write(str(genome.fitness) + "\n")
                file.write(str(genome.maxneuron) + "\n")
                for mutation,rate in genome.mutationRates.items():
                    file.write(str(mutation) + "\n")
                    file.write(str(rate) + "\n")
                file.write("done\n")

                file.write(str(len(genome.genes)) + "\n")
                for l,gene in enumerate(genome.genes):
                    file.write(str(gene.into) + " ")
                    file.write(str(gene.out) + " ")
                    file.write(str(gene.weight) + " ")
                    file.write(str(gene.innovation) + " ")
                    if gene.enabled:
                        file.write("1\n")
                    else:
                        file.write("0\n")
        file.close()
    
    def loadFile(self, filename, env):
        file = open(filename, "r")
        self.__init__(env)
        self.generation = int(file.readline().replace("\n", ""))
        self.maxFitness = int(file.readline().replace("\n", ""))
        #gui.settext(5, 8, maxFitnessLabel, "Max Fitness. " .. math.floor(pool.maxFitness))
        numSpecies = int(file.readline().replace("\n", ""))
        for s in range(0, numSpecies):
            species = Species()
            self.species.append(species)
            species.topFitness = float(file.readline().replace("\n", ""))
            species.staleness = int(file.readline().replace("\n", ""))
            numGenomes = int(file.readline().replace("\n", ""))
            for g in range(0, numGenomes):
                genome = Genome(self)
                species.genomes.append(genome)
                genome.fitness = float(file.readline().replace("\n", ""))
                genome.maxneuron = int(file.readline().replace("\n", ""))
                line = file.readline().replace("\n", "")
                while line != "done":
                    genome.mutationRates[line] = float(file.readline().replace("\n", ""))
                    line = file.readline().replace("\n", "")
                numGenes = int(file.readline().replace("\n", ""))
                for n in range(0,numGenes):
                    gene = Gene()
                    genome.genes.append(gene)
                    enabled = 0
                    line = file.readline()
                    data = []
                    for x in [x for i, x in enumerate(line.split(" "))]:
                        try:
                            data.append(int(x))
                        except ValueError:
                            data.append(float(x))
                    gene.into, gene.out, gene.weight, gene.innovation, enabled = data
                    
                    gene.enabled = enabled == 1
        file.close()
    
        while self.fitnessAlreadyMeasured():
            self.nextGenome()
        self.initializeRun()
        self.currentFrame = self.currentFrame + 1