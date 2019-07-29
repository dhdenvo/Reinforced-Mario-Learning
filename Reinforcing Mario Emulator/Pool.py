import math
import random

ButtonNames = ["A","B","up","down","left","right",]

class Pool:
    def __init__(self):
        self.species = []
        self.globals = []
        self.controller = {}
        self.rightmost = 0
        self.timeout = 0
        self.marioX = 0
        self.marioY = 0
        self.generation = 0
        self.innovation = Outputs
        self.currentSpecies = 1
        self.currentGenome = 1
        self.currentFrame = 0
        self.maxFitness = 0
        
    def clearJoypad(self):
        for b in ButtonNames:
            self.controller[b] = False
        
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
            if species.staleness < StaleSpecies or species.topFitness >= pool.maxFitness:
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
        for s in range(0,len(pool.species)):
            species = self.species[s]
            if not foundSpecies and sameSpecies(child, species.genomes[1]):
                species.genomes.append(child)
                foundSpecies = True
    
        if not foundSpecies:
            childSpecies = newSpecies()
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
            species = pool.species[random.randint(1, len(pool.species))]
            children.append(species.breedChild())
        
        for c in range(0,len(children)):
            child = children[c]
            self.addToSpecies(child)
    
        self.generation = self.generation + 1

        #writeFile("backup." .. pool.generation .. "." .. forms.gettext(saveLoadFile))
        ###########Add write file / make able to be accessed
        #writeFile("backup." .. pool.generation .. ".")	
        
        
    def evaluateCurrent(self):
        species = self.species[pool.currentSpecies]
        genome = species.genomes[pool.currentGenome]

        inputs = getInputs()
        self.controller = genome.network.evaluateNetwork(inputs)

        if self.controller["Left"] and self.controller["Right"]:
            self.controller["Left"] = False
            self.controller["Right"] = False
        if self.controller["Up"] and self.controller["Down"]:
            self.controller["Up"] = False
            self.controller["Down"] = False
            
    
    def initializeRun(self):
        #savestate.load(Filename);
        #env.reset()
        self.rightmost = 0
        self.currentFrame = 0
        self.timeout = TimeoutConstant
        clearJoypad()
    
        species = self.species[self.currentSpecies]
        genome = species.genomes[self.currentGenome]
        self.network = Network(genome)
        self.evaluateCurrent()    
        
    def nextGenome(self):
        self.currentGenome = self.currentGenome + 1
        if self.currentGenome > len(self.species[self.currentSpecies].genomes):
            self.currentGenome = 1
            self.currentSpecies = self.currentSpecies+1
            if self.currentSpecies > len(self.species):
                self.newGeneration()
                self.currentSpecies = 1
                
    def fitnessAlreadyMeasured(self):
        species = self.species[self.currentSpecies]
        genome = species.genomes[pool.currentGenome]
    
        return genome.fitness != 0  
    
    def playTop():
        maxfitness = 0
        maxs, maxg = 0,0
        for s,species in enumerate(self.species):
            for g,genome in enumerate(species.genomes):
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
    
    '''def writeFile(filename)
        local file = io.open(filename, "w")
        file:write(pool.generation .. "\n")
        file:write(pool.maxFitness .. "\n")
        file:write(len(pool.species) .. "\n")
                       for n,species in pairs(pool.species) do
            file:write(species.topFitness .. "\n")
                    file:write(species.staleness .. "\n")
                    file:write(len(species.genomes) .. "\n")
                               for m,genome in pairs(species.genomes) do
                    file:write(genome.fitness .. "\n")
                            file:write(genome.maxneuron .. "\n")
                            for mutation,rate in pairs(genome.mutationRates) do
                            file:write(mutation .. "\n")
                                    file:write(rate .. "\n")
                                    end
                            file:write("done\n")
    
                            file:write(len(genome.genes) .. "\n")
                                       for l,gene in pairs(genome.genes) do
                            file:write(gene.into .. " ")
                                    file:write(gene.out .. " ")
                                    file:write(gene.weight .. " ")
                                    file:write(gene.innovation .. " ")
                                    if(gene.enabled) then
                                    file:write("1\n")
                                            else
                                    file:write("0\n")
                                            end
                                    end
                            end
                    end
            file:close()
    end '''    
    
    '''def loadFile(filename):
        local file = io.open(filename, "r")
        pool = newPool()
        pool.generation = file:read("*number")
        pool.maxFitness = file:read("*number")
        #forms.settext(maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
        gui.settext(5, 8, maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
        local numSpecies = file:read("*number")
        for s=1,numSpecies do
            local species = newSpecies()
            table.insert(pool.species, species)
            species.topFitness = file:read("*number")
            species.staleness = file:read("*number")
            local numGenomes = file:read("*number")
            for g=1,numGenomes do
                local genome = newGenome()
                table.insert(species.genomes, genome)
                genome.fitness = file:read("*number")
                genome.maxneuron = file:read("*number")
                local line = file:read("*line")
                while line ~= "done" do
                    genome.mutationRates[line] = file:read("*number")
                    line = file:read("*line")
                end
                local numGenes = file:read("*number")
                for n=1,numGenes do
                    local gene = newGene()
                    table.insert(genome.genes, gene)
                    local enabled
                    gene.into, gene.out, gene.weight, gene.innovation, enabled = file:read("*number", "*number", "*number", "*number", "*number")
                    if enabled == 0 then
                        gene.enabled = false
                    else
                        gene.enabled = true
                    end
                end
            end
        end
        file:close()
    
        while fitnessAlreadyMeasured() do
            nextGenome()
        end
        initializeRun()
        pool.currentFrame = pool.currentFrame + 1
    end'''    