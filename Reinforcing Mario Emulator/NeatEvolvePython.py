'''MarI/O by SethBling
   Feel free to use this code, but please do not redistribute it.
   Intended for use with the BizHawk emulator and Super Mario World or Super Mario Bros. ROM.
   For SMW, make sure you have a save state named "DP1.state" at the beginning of a level,
   and put a copy in both the Lua folder and the root directory of BizHawk.
   Modified by David Daghelian for use with python's gym_super_mario_bros
'''

import random

gameinfo = {}
gameinfo.getromname = "Super Mario Bros."

ButtonNames = [
    "A",
    "B",
    "up",
    "down",
    "left",
    "right",
]

BoxRadius = 6
InputSize = (BoxRadius*2+1)*(BoxRadius*2+1)

Inputs = InputSize+1
Outputs = len(ButtonNames)

Population = 300
DeltaDisjoint = 2.0
DeltaWeights = 0.4
DeltaThreshold = 1.0
pool = None

StaleSpecies = 15

MutateConnectionsChance = 0.25
PerturbChance = 0.90
CrossoverChance = 0.75
LinkMutationChance = 2.0
NodeMutationChance = 0.50
BiasMutationChance = 0.40
StepSize = 0.1
DisableMutationChance = 0.4
EnableMutationChance = 0.2

TimeoutConstant = 20

MaxNodes = 1000000

def getPositions():
    marioX = memory.readbyte(0x6D) * 0x100 + memory.readbyte(0x86)
    marioY = memory.readbyte(0x03B8)+16

    screenX = memory.readbyte(0x03AD)
    screenY = memory.readbyte(0x03B8)


def getTile(dx, dy):
    x = marioX + dx + 8
    y = marioY + dy - 16
    page = math.floor(x/256)%2

    subx = math.floor((x%256)/16)
    suby = math.floor((y - 32)/16)
    addr = 0x500 + page*13*16+suby*16+subx

    if suby >= 13 or suby < 0:
        return 0

    if memory.readbyte(addr) != 0:
        return 1
    else:
        return 0

def getSprites():
    sprites = {}
    for slot in range(0,4):
        enemy = memory.readbyte(0xF+slot)
        if enemy != 0:
            ex = memory.readbyte(0x6E + slot)*0x100 + memory.readbyte(0x87+slot)
            ey = memory.readbyte(0xCF + slot)+24
            sprites[len(sprites)+1] = {"x":ex, "y":ey}

    return sprites


def getExtendedSprites():
    return {}

def getInputs():
    getPositions()

    sprites = getSprites()
    extended = getExtendedSprites()

    inputs = {}

    for dy in range(-BoxRadius*16, BoxRadius*16, 16):
        for dx in range(-BoxRadius*16, BoxRadius*16, 16):
            inputs[len(inputs)+1] = 0

            tile = getTile(dx, dy)
            if tile == 1 and marioY+dy < 0x1B0:
                inputs[len(inputs)] = 1

            for i in range(0,len(sprites)):
                distx = math.abs(sprites[i]["x"] - (marioX+dx))
                disty = math.abs(sprites[i]["y"] - (marioY+dy))
                if distx <= 8 and disty <= 8:
                    inputs[len(inputs)] = -1


            for i in range(0,len(extended)):
                distx = math.abs(extended[i]["x"] - (marioX+dx))
                disty = math.abs(extended[i]["y"] - (marioY+dy))
                if distx < 8 and disty < 8:
                    inputs[len(inputs)] = -1

        --mariovx = memory.read_s8(0x7B)
        --mariovy = memory.read_s8(0x7D)

    return inputs

def sigmoid(x):
    return 2/(1+math.exp(-4.9*x))-1

def newInnovation():
    pool["innovation"] += 1
    return pool["innovation"]

def newPool():
    pool = {}
    pool["species"] = []
    pool["generation"] = 0
    pool["innovation"] = Outputs
    pool["currentSpecies"] = 1
    pool["currentGenome"] = 1
    pool["currentFrame"] = 0
    pool["maxFitness"] = 0

    return pool

def newSpecies():
    species = {}
    species["topFitness"] = 0
    species["staleness"] = 0
    species["genomes"] = []
    species["averageFitness"] = 0

    return species

def newGenome():
    genome = {}
    genome["genes"] = []
    genome["fitness"] = 0
    genome["adjustedFitness"] = 0
    genome["network"] = {}
    genome["maxneuron"] = 0
    genome["globalRank"] = 0
    genome["mutationRates"] = {}
    genome["mutationRates"]["connections"] = MutateConnectionsChance
    genome["mutationRates"]["link"] = LinkMutationChance
    genome["mutationRates"]["bias"] = BiasMutationChance
    genome["mutationRates"]["node"] = NodeMutationChance
    genome["mutationRates"]["enable"] = EnableMutationChance
    genome["mutationRates"]["disable"] = DisableMutationChance
    genome["mutationRates"]["step"] = StepSize

    return genome

def copyGenome(genome):
    genome2 = newGenome()
    for g in range(0,len(genome["genes"])):
        genome2["genes"].append(copyGene(genome["genes"][g]))
    genome2["maxneuron"] = genome["maxneuron"]
    genome2["mutationRates"]["connections"] = genome["mutationRates"]["connections"]
    genome2["mutationRates"]["link"] = genome["mutationRates"]["link"]
    genome2["mutationRates"]["bias"] = genome["mutationRates"]["bias"]
    genome2["mutationRates"]["node"] = genome["mutationRates"]["node"]
    genome2["mutationRates"]["enable"] = genome["mutationRates"]["enable"]
    genome2["mutationRates"]["disable"] = genome["mutationRates"]["disable"]

    return genome2

def basicGenome():
    genome = newGenome()
    innovation = 1

    genome["maxneuron"] = Inputs
    mutate(genome)

    return genome

def newGene():
    gene = {}
    gene["into"] = 0
    gene["out"] = 0
    gene["weight"] = 0.0
    gene["enabled"] = True
    gene["innovation"] = 0

    return gene

def copyGene(gene):
    gene2 = newGene()
    gene2["into"] = gene["into"]
    gene2["out"] = gene["out"]
    gene2["weight"] = gene["weight"]
    gene2["enabled"] = gene["enabled"]
    gene2["innovation"] = gene["innovation"]

    return gene2

def newNeuron():
    neuron = {}
    neuron["incoming"] = {}
    neuron["value"] = 0.0

    return neuron

def generateNetwork(genome):
    network = {}
    network["neurons"] = {}

    for i in range(0,Inputs):
        network["neurons"][i] = newNeuron()
        #network["neurons"].append(newNeuron())

    for o in range(0,Outputs):
        network["neurons"][MaxNodes + o] = newNeuron()
        #network["neurons"].append(newNeuron())

    genomes["genes"] = sorted(genomes["genes"], key=lambda k: k["out"])    
    '''table.sort(genome.genes, def (a,b)
        return (a.out < b.out)
    end)'''

    for i in range(0, len(genome["genes"])):
        gene = genome["genes"][i]
        if gene["enabled"]:
            neuron = network["neurons"].setdefault(gene["out"], newNeuron())
            neuron["incoming"].append(gene)
            network["neurons"].setdefault(gene["into"], newNeuron())

    genome["network"] = network

def evaluateNetwork(network, inputs):
    inputs.append(1)
    if len(inputs) != Inputs:
        print("Incorrect number of neural network inputs.")
        return {}

    for i in range(0,Inputs):
        network["neurons"][i]["value"] = inputs[i]

    for _,neuron in network["neurons"].items():
        sum = 0
        for j in range(0,len(neuron["incoming"])):
            incoming = neuron.incoming[j]
            other = network.neurons[incoming.into]
            sum = sum + incoming.weight * other.value

        if len(neuron["incoming"]) > 0:
            neuron["value"] = sigmoid(sum)

    outputs = {}
    for o in range(0,Outputs):
        button = ButtonNames[o]
        if network["neurons"][MaxNodes+o]["value"] > 0:
            outputs[button] = True
        else:
            outputs[button] = False

    return outputs

def crossover(g1, g2):
    #Make sure g1 is the higher fitness genome
    if g2["fitness"] > g1["fitness"]:
        tempg = g1
        g1 = g2
        g2 = tempg

    child = newGenome()

    innovations2 = {}
    for i in range(0, len(g2["genes"])):
        gene = g2["genes"][i]
        innovations2[gene["innovation"]] = gene

    for i in range(0, len(g1["genes"])):
        gene1 = g1["genes"][i]
        gene2 = innovations2.get(gene1["innovation"], None)
        if gene2 != None and random.randint(1,2) == 1 and gene2["enabled"]:
            table.insert(child.genes, copyGene(gene2))
        else:
            table.insert(child.genes, copyGene(gene1))

    child["maxneuron"] = max(g1["maxneuron"], g2["maxneuron"])

    for mutation,rate in g1["mutationRates"].items():
        child["mutationRates"][mutation] = rate

    return child

def randomNeuron(genes, nonInput):
    neurons = {}
    if not nonInput:
        for i in range(0, Inputs):
            neurons[i] = True

    for o in range(0,Outputs):
        neurons[MaxNodes+o] = True

    for i in range(0,len(genes)):
        if (not nonInput) or genes[i]["into"] > Inputs:
            neurons[genes[i]["into"]] = True
        if (not nonInput) or genes[i]["out"] > Inputs:
            neurons[genes[i]["out"]] = True

    count = 0
    for _,_ in neurons.items():
        count = count + 1

    n = random.randint(0, count - 1)

    for k,v in pairs(neurons):
        n -= 1
        if n == -1:
            return k

    return 0

def containsLink(genes, link):
    for i in range(0, len(genes)):
        gene = genes[i]
        if gene["into"] == link["into"] and gene["out"] == link["out"]:
            return True
    return False

def pointMutate(genome):
    step = genome["mutationRates"]["step"]

    for i in range(0, len(genome.genes)):
        gene = genome["genes"][i]
        rand = random.random()
        if rand < PerturbChance:
            gene["weight"] = gene["weight"] + rand * step * 2 - step
        else:
            gene["weight"] = rand * 4 - 2

def linkMutate(genome, forceBias):
    neuron1 = randomNeuron(genome.genes, False)
    neuron2 = randomNeuron(genome.genes, True)

    newLink = newGene()
    if neuron1 <= Inputs and neuron2 <= Inputs:
        #Both input nodes
        return
    if neuron2 <= Inputs:
        #Swap output and input
        temp = neuron1
        neuron1 = neuron2
        neuron2 = temp

    newLink["into"] = neuron1
    newLink["out"] = neuron2
    if forceBias:
        newLink["into"] = Inputs

    if containsLink(genome["genes"], newLink):
        return
    newLink["innovation"] = newInnovation()
    newLink["weight"] = random.random() * 4 - 2

    genome["genes"].append(newLink)

def nodeMutate(genome):
    if len(genome["genes"]) == 0:
        return

    genome["maxneuron"] += 1

    gene = genome["genes"][random.randint(0, len(genome["genes"]) - 1)]
    if not gene["enabled"]:
        return
    gene["enabled"] = False

    gene1 = copyGene(gene)
    gene1["out"] = genome["maxneuron"]
    gene1["weight"] = 1.0
    gene1["innovation"] = newInnovation()
    gene1["enabled"] = true
    genome["genes"].append(gene1)

    gene2 = copyGene(gene)
    gene2["into"] = genome["maxneuron"]
    gene2["innovation"] = newInnovation()
    gene2["enabled"] = true
    genome["genes"].append(gene2)

def enableDisableMutate(genome, enable):
    candidates = []
    for gene in genome["genes"]:
        if gene["enabled"] == not enable:
            candidates.append(gene)

    if len(candidates) == 0:
        return

    gene = candidates[random.randint(0,len(candidates) - 1)]
    gene["enabled"] = not gene["enabled"]

def mutate(genome):
    for mutation,rate in genome["mutationRates"].items():
        if random.randint(1,2) == 1:
            genome["mutationRates"][mutation] = 0.95 * rate
        else:
            genome["mutationRates"][mutation] = 1.05263 * rate

    if random.random() < genome["mutationRates"]["connections"]:
        pointMutate(genome)

    p = genome["mutationRates"]["link"]
    while p > 0:
        if random.random() < p:
            linkMutate(genome, False)
        p -= 1

    p = genome["mutationRates"]["bias"]
    while p > 0:
        if random.random() < p:
            linkMutate(genome, True)
        p -= 1

    p = genome["mutationRates"]["node"]
    while p > 0:
        if random.random() < p:
            nodeMutate(genome)
        p -= 1

    p = genome["mutationRates"]["enable"]
    while p > 0:
        if random.random() < p:
            enableDisableMutate(genome, True)
        p -= 1

    p = genome["mutationRates"]["disable"]
    while p > 0:
        if random.random() < p:
            enableDisableMutate(genome, False)
        p -= 1

def disjoint(genes1, genes2):
    i1 = {}
    for i in range(0, len(genes1)):
        gene = genes1[i]
        i1[gene["innovation"]] = True

    i2 = {}
    for i in range(0, len(genes2)):
        gene = genes2[i]
        i2[gene["innovation"]] = True

    disjointGenes = 0
    for i in range(0,len(genes1)):
        gene = genes1[i]
        if not i2[gene["innovation"]]:
            disjointGenes += 1

    for i in range(0, len(genes2)):
        gene = genes2[i]
        if not i1[gene["innovation"]]:
            disjointGenes += 1

    n = max(len(genes1), len(genes2))

    return disjointGenes / n

def weights(genes1, genes2):
    i2 = {}
    for i in range(0,len(genes2)):
        gene = genes2[i]
        i2[gene["innovation"]] = gene

    sum = 0
    coincident = 0
    for i in range(0, len(genes1)):
        gene = genes1[i]
        if i2.get(gene["innovation"], None) != None:
            gene2 = i2[gene["innovation"]]
            sum = sum + abs(gene["weight"] - gene2["weight"])
            coincident += 1

    return sum / coincident

def sameSpecies(genome1, genome2):
    dd = DeltaDisjoint * disjoint(genome1["genes"], genome2["genes"])
    dw = DeltaWeights * weights(genome1["genes"], genome2["genes"]) 
    return dd + dw < DeltaThreshold

def rankGlobally():
    globals = []
    for s in range(0, len(pool.species)):
        species = pool.species[s]
        for g in range(0, len(species.genomes)):
            globals.append(species["genomes"][g])

    globals = sorted(globals, key=lambda k: k["fitness"])        
    '''table.sort(globals, def (a,b)
        return (a.fitness < b.fitness)
    end)'''

    for g in range(0,len(globals)):
        globals[g].globalRank = g

def calculateAverageFitness(species):
    total = 0

    for g in range(0, len(species.genomes)):
        genome = species["genomes"][g]
        total += genome["globalRank"]

    species["averageFitness"] = total / len(species["genomes"])

def totalAverageFitness():
    total = 0
    for s in range(0, len(pool["species"])):
        species = pool["species"][s]
        total = total + species["averageFitness"]

    return total

def cullSpecies(cutToOne):
    for s in range(0, len(pool["species"])):
        species = pool["species"][s]

        species["genomes"] = sorted(species["genomes"], key=lambda k: k["fitness"])[::-1]     
        '''table.sort(species.genomes, def (a,b)
            return (a.fitness > b.fitness)
        end)'''

        remaining = math.ceil(len(species["genomes"])/2)
        if cutToOne:
            remaining = 1
        while len(species["genomes"]) > remaining:
            species["genomes"].pop(-1)

def breedChild(species):
    child = {}
    if random.random() < CrossoverChance:
        g1 = species["genomes"][random.randint(0, len(species["genomes"]) - 1)]
        g2 = species["genomes"][random.randint(0, len(species["genomes"]) - 1)]
        child = crossover(g1, g2)
    else:
        g = species["genomes"][random.randint(0, len(species["genomes"]) - 1)]
        child = copyGenome(g)

    mutate(child)

    return child

def removeStaleSpecies():
    survived = []

    for s in range(0, len(pool["species"])):
        species = pool["species"][s]

        species["genomes"] = sorted(species["genomes"], key=lambda k: k["fitness"])[::-1]
        '''table.sort(species.genomes, def (a,b)
            return (a.fitness > b.fitness)
        end)'''

        if species["genomes"][0]["fitness"] > species["topFitness"]:
            species["topFitness"] = species["genomes"][0]["fitness"]
            species["staleness"] = 0
        else:
            species["staleness"] += 1

        if species["staleness"] < StaleSpecies or species["topFitness"] >= pool["maxFitness"]:
            survived.append(species)

    pool["species"] = survived

def removeWeakSpecies():
    survived = []

    sum = totalAverageFitness()
    for s in range(0, len(pool["specie"])):
        species = pool["species"][s]
        breed = math.floor(species["averageFitness"] / sum * Population)
        if breed >= 1:
            survived.append(species)

    pool["species"] = survived


def addToSpecies(child):
    foundSpecies = False
    for s in range(0, len(pool["species"])):
        species = pool["species"][s]
        if not foundSpecies and sameSpecies(child, species["genomes"][1]):
            species["genomes"].append(child)
            foundSpecies = True

    if not foundSpecies:
        childSpecies = newSpecies()
        childSpecies["genomes"].append(child)
        pool["species"].append(childSpecies)

def newGeneration():
    cullSpecies(false) #Cull the bottom half of each species
    rankGlobally()
    removeStaleSpecies()
    rankGlobally()
    for s in range(0, len(pool["species"])):
        species = pool["species"][s]
        calculateAverageFitness(species)
    removeWeakSpecies()
    sum = totalAverageFitness()
    children = []
    for s in range(0, len(pool["species"])):
        species = pool["species"][s]
        breed = math.floor(species["averageFitness"] / sum * Population) - 1
        for i in range(0, breed):
            children.append(breedChild(species))

    cullSpecies(true) #Cull all but the top member of each species
    while len(children) + len(pool.species) < Population:
        species = pool["species"][random.randint(0, len(pool.species) - 1)]
        children.append(breedChild(species))

    for c in range(0, len(children)):
        child = children[c]
        addToSpecies(child)

    pool["generation"] += 1

    #writeFile("backup." .. pool.generation .. "." .. forms.gettext(saveLoadFile))
    writeFile("backup." + pool.generation + ".txt")


def initializePool():
    pool = newPool()

    for i in range(0,Population):
        basic = basicGenome()
        addToSpecies(basic)

    initializeRun()

def clearJoypad():
    controller = {}
    for b in range(0, len(ButtonNames)):
        controller[ButtonNames[b]] = False
    #Write To Joypad
    joypad.write(1, controller)

def initializeRun():
    savestate.load(Filename);
    rightmost = 0
    pool.currentFrame = 0
    timeout = TimeoutConstant
    clearJoypad()

    species = pool["species"][pool["currentSpecies"]]
    genome = species["genomes"][pool["currentGenome"]]
    generateNetwork(genome)
    evaluateCurrent()


def evaluateCurrent():
    species = pool["species"][pool["currentSpecies"]]
    genome = species["genomes"][pool["currentGenome"]]

    inputs = getInputs()
    controller = evaluateNetwork(genome["network"], inputs)

    if controller["Left"] and controller["Right"]:
        controller["Left"] = False
        controller["Right"] = False
    if controller["Up"] and controller["Down"]:
        controller["Up"] = False
        controller["Down"] = False

    joypad.write(1, controller)

if pool == None:
    initializePool()


def nextGenome():
    pool["currentGenome"] += 1
    if pool["currentGenome"] > len(pool["species"][pool["currentSpecies"]]["genomes"]):
        pool["currentGenome"] = 1
        pool["currentSpecies"] += 1
        if pool["currentSpecies"] > len(pool["species"]):
            newGeneration()
            pool.currentSpecies = 1

def fitnessAlreadyMeasured():
    species = pool["species"][pool["currentSpecies"]]
    genome = species["genomes"][pool["currentGenome"]]

    return genome.fitness != 0

def displayGenome(genome):
    network = genome["network"]
    cells = {}
    i = 1
    cell = {}
    for dy in range(-BoxRadius, BoxRadius):
        for dx in range(-BoxRadius, BoxRadius):
            cell = {}
            cell["x"] = 50 + 5 * dx
            cell["y"] = 70 + 5 * dy
            cell["value"] = network["neurons"][i]["value"]
            cells[i] = cell
            i += 1

    biasCell = {}
    biasCell["x"] = 80
    biasCell["y"] = 110
    biasCell["value"] = network["neurons"][Inputs]["value"]
    cells[Inputs] = biasCell

    for o in range(0,Outputs):
        cell = {}
        cell["x"] = 220
        cell["y"] = 30 + 8 * o
        cell["value"] = network["neurons"][MaxNodes + o]["value"]
        cells[MaxNodes + o] = cell
        color
        if cell["value"] > 0:
            color = 0xFF0000FF
        else:
            color = 0xFF000000
        #Draw Stuff
        #gui.drawText(223, 24+8*o, ButtonNames[o], color, 9)

    for n,neuron in pairs(network["neurons"]):
        cell = {}
        if n > Inputs and n <= MaxNodes:
            cell["x"] = 140
            cell["y"] = 40
            cell["value"] = neuron["value"]
            cells[n] = cell

    for n in range(0,4):
        for gene in genome["genes"]:
            if gene["enabled"]:
                c1 = cells[gene["into"]]
                c2 = cells[gene["out"]]
                if gene["into"] > Inputs and gene["into"] <= MaxNodes:
                    c1["x"] = 0.75 * c1["x"] + 0.25 * c2["x"]
                    if c1["x"] >= c2["x"]:
                        c1["x"] = c1["x"] - 40
                    if c1["x"] < 90:
                        c1["x"] = 90

                    if c1["x"] > 220:
                        c1["x"] = 220

                    c1["y"] = 0.75*c1["y"] + 0.25*c2["y"]

                if gene["out"] > Inputs and gene["out"] <= MaxNodes:
                    c2["x"] = 0.25*c1["x"] + 0.75*c2["x"]
                    if c1["x"] >= c2["x"]:
                        c2["x"] = c2["x"] + 40
                    if c2["x"] < 90:
                        c2["x"] = 90
                    if c2["x"] > 220:
                        c2["x"] = 220
                    c2["y"] = 0.25*c1["y"] + 0.75*c2["y"]

    #Draw Stuff
    #gui.drawBox(50-BoxRadius*5-3, 70-BoxRadius*5-3, 50+BoxRadius*5+2, 70+BoxRadius*5+2, 0xFF000000, 0x80808080)
    for n,cell in cells.items():
        if n > Inputs or cell["value"] != 0:
            color = math.floor((cell["value"]+1)/2*256)
            if color > 255:
                color = 255
            if color < 0: 
                color = 0
            opacity = 0xFF000000
            if cell["value"] == 0:
                opacity = 0x50000000
            color = opacity + color*0x10000 + color*0x100 + color
            #Draw Stuff
            #gui.drawBox(cell["x"] - 2, cell["y"] - 2, cell["x"] + 2, cell["y"] + 2, opacity, color)

    for gene in genome["genes"]:
        if gene["enabled"]:
            c1 = cells[gene["into"]]
            c2 = cells[gene["out"]]
            opacity = 0xA0000000
            if c1["value"] == 0:
                opacity = 0x20000000

            color = 0x80 - math.floor(abs(sigmoid(gene.weight)) * 0x80)
            if gene.weight > 0:
                color = opacity + 0x8000 + 0x10000 * color
            else:
                color = opacity + 0x800000 + 0x100 * color
            #Draw Stuff
            #gui.drawLine(c1["x"] + 1, c1["y"], c2["x"] - 3, c2["y"], color)

    #Draw Stuff
    #gui.drawBox(49,71,51,78,0x00000000,0x80FF0000)

    #Draw Stuff
    #Forms Stuff
    '''if forms.ischecked(showMutationRates):
    	pos = 100
    	for mutation,rate in pairs(genome.mutationRates) do
    		gui.drawText(100, pos, mutation .. ": " .. rate, 0xFF000000, 10)
    		pos += 8
    	end
    end'''

def writeFile(filename):
    file = open(filename, "w")
    file.write(pool["generation"] + "\n")
    file.write(pool["maxFitness"] + "\n")
    file.write(len(pool["species"]) + "\n")
    for species in pool["species"]:
        file.write(species["topFitness"] + "\n")
        file.write(species["staleness"] + "\n")
        file.write(len(species["genomes"]) + "\n")
        for m,genome in species["genomes"].items():
            file.write(genome.fitness + "\n")
            file.write(genome.maxneuron + "\n")
            for mutation,rate in pairs(genome.mutationRates):
                file.write(mutation + "\n")
                file:write(rate + "\n")
            file:write("done\n")
            file:write(len(genome["genes"]) + "\n")
            for gene in genome["genes"]:
                file.write(gene["into"] + " ")
                file.write(gene["out"] + " ")
                file.write(gene["weight"] + " ")
                file.write(gene["innovation"] + " ")
                if gene["enabled"]:
                    file.write("1\n")
                else:
                    file.write("0\n")

    file.close()


def savePool():
    #Forms Stuff
    #filename = forms.gettext(saveLoadFile)
    writeFile(filename)

def loadFile(filename):
    file = open(filename, "r")
    pool = newPool()
    pool["generation"] = int(file.readline())
    pool["maxFitness"] = int(file.readline())
    #Forms Stuff
    #forms.settext(maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
    numSpecies = int(file.readline())
    for s in range(0, numSpecies):
        species = newSpecies()
        pool["species"].append(species)
        species["topFitness"] = int(file.readline())
        species["staleness"] = int(file.readline())
        numGenomes = int(file.readline())
        for g in range(0,numGenomes):
            genome = newGenome()
            species["genomes"].append(genome)
            genome["fitness"] = int(file.readline())
            genome["maxneuron"] = int(file.readline())
            line = file.readline()
            while line != "done":
                genome["mutationRates"][line] = int(file.readline())
                line = file.readline()
            numGenes = int(file.readline())
            for n in range(0, numGenes):
                gene = newGene()
                genome["genes"].append(gene)
                enabled = -1
                gene["into"], gene["out"], gene["weight"], gene["innovation"], enabled = [int(x) for x in file.readline().split(" ")]
                gene.enabled = enabled == 1
    file.close()

    while fitnessAlreadyMeasured():
        nextGenome()

    initializeRun()
    pool["currentFrame"] += 1


def loadPool():
    #Forms Stuff
    #filename = forms.gettext(saveLoadFile)
    loadFile(filename)

def playTop():
    maxfitness = 0
    maxs = 0
    maxg = 0
    for s,species in pairs(pool["species"]):
        for g,genome in pairs(species.genomes):
            if genome["fitness"] > maxfitness:
                maxfitness = genome["fitness"]
                maxs = s
                maxg = g

    pool["currentSpecies"] = maxs
    pool["currentGenome"] = maxg
    pool["maxFitness"] = maxfitness
    #Forms Stuff
    #forms.settext(maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
    initializeRun()
    pool["currentFrame"] += 1
    return

#def onExit():
#	forms.destroy(form)
#end

writeFile("temp.pool")

#Emulator Things
#emu.registerexit(onExit)

#Forms Stuff
#maxFitnessLabel = gui.text(5, 8, "Max Fitness: " .. math.floor(pool.maxFitness))
#form = forms.newform(200, 260, "Fitness")
#maxFitnessLabel = forms.label(form, "Max Fitness: " .. math.floor(pool.maxFitness), 5, 8)
#showNetwork = forms.checkbox(form, "Show Map", 5, 30)
#showMutationRates = forms.checkbox(form, "Show M-Rates", 5, 52)
#restartButton = forms.button(form, "Restart", initializePool, 5, 77)
#saveButton = forms.button(form, "Save", savePool, 5, 102)
#loadButton = forms.button(form, "Load", loadPool, 80, 102)
#saveLoadFile = forms.textbox(form, Filename .. ".pool", 170, 25, nil, 5, 148)
#saveLoadLabel = forms.label(form, "Save/Load:", 5, 129)
#playTopButton = forms.button(form, "Play Top", playTop, 5, 170)
#hideBanner = forms.checkbox(form, "Hide Banner", 5, 190)


while True:
    backgroundColor = 0xD0FFFFFF
    #Draw Stuff
    #if not forms.ischecked(hideBanner) then
    #	gui.drawBox(0, 0, 300, 26, backgroundColor, backgroundColor)
    #end

    species = pool.species[pool.currentSpecies]
    genome = species.genomes[pool.currentGenome]

    #Forms Stuff
    #if forms.ischecked(showNetwork) then
    #	displayGenome(genome)
    #end

    if pool.currentFrame%5 == 0:
        evaluateCurrent()

    #Write To Joypad
    joypad.write(1, controller)

    getPositions()
    if marioX > rightmost:
        rightmost = marioX
        timeout = TimeoutConstant

    timeout = timeout - 1

    timeoutBonus = pool["currentFrame"] / 4
    if timeout + timeoutBonus <= 0:
        fitness = rightmost - pool["currentFrame"] / 2
        if gameinfo.getromname == "Super Mario Bros." and rightmost > 3186:
            fitness = fitness + 1000
        if fitness == 0:
            fitness = -1
        genome.fitness = fitness

        if fitness > pool["maxFitness"]:
            pool.maxFitness = fitness
            #Forms Stuff
            #forms.settext(maxFitnessLabel, "Max Fitness: " .. math.floor(pool.maxFitness))
            writeFile("backup." + pool.generation + ".txt")
            #writeFile("backup." .. pool.generation .. "." .. forms.gettext(saveLoadFile))

    print("Gen:", pool.generation, "species:", pool.currentSpecies, "genome:", pool.currentGenome, " fitness:", fitness)
    pool["currentSpecies"] = 1
    pool["currentGenome"] = 1
    while fitnessAlreadyMeasured():
        nextGenome()
    initializeRun()

    measured = 0
    total = 0
    for species in pool["species"]:
        for genome in species["genomes"]:
            total += 1
            if genome["fitness"] != 0:
                measured += 1

    #Forms Stuff
    #Draw Stuff
    #if not forms.ischecked(hideBanner) then
    #	gui.drawText(0, 0, "Gen " .. pool.generation .. " species " .. pool.currentSpecies .. " genome " .. pool.currentGenome .. " (" .. math.floor(measured/total*100) .. "%)", 0xFF000000, 11)
    #	gui.drawText(0, 12, "Fitness: " .. math.floor(rightmost - (pool.currentFrame) / 2 - (timeout + timeoutBonus)*2/3), 0xFF000000, 11)
    #	gui.drawText(100, 12, "Max Fitness: " .. math.floor(pool.maxFitness), 0xFF000000, 11)
    #end

    pool["currentFrame"] += 1

    emu.frameadvance();